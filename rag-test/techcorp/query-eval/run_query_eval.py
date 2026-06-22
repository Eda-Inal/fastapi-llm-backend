"""
Query Quality Eval
==================
For each question, calls the chat API with the configured MODEL, extracts the
RAG query the routing model generated, runs that query through /tools/rag_debug,
and compares retrieval metrics against the modelsiz baseline (baseline.json).

MODES
-----
1. Build baseline (one-time, already done):
   python run_query_eval.py --build-baseline

2. Run eval (primary usage):
   python run_query_eval.py [--range Q01-Q10]
   Change MODEL at the top to switch routing models.

3. Side-by-side comparison of two eval runs:
   python run_query_eval.py --side-by-side run_001,run_002

OUTPUT
------
  baseline.json                 ← canonical modelsiz retrieval metrics (fixed)
  results/run_XXX/results.json  ← per-run results
  results/run_XXX/logs/         ← per-question debug logs
  comparison_table.md           ← appended after each run
"""

import argparse
import httpx
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
MODEL        = "llama-3.3-70b-versatile"  # routing model to test
USER_ID      = "techcorp-test"
RATE_LIMIT_S = 30           # seconds between questions (~1/min for LLM calls)
CHAT_URL     = "http://localhost:8000/api/v1/chat/stream"
DEBUG_URL    = "http://localhost:8001/tools/rag_debug"
DB_CONTAINER = "groq_stream_db"
TOP_K        = 5
# ─────────────────────────────────────────────────────────────────────────────

BASE_DIR       = Path(__file__).parent
QUESTIONS_FILE = BASE_DIR.parent / "questions.json"
RUNALL_DIR     = BASE_DIR.parent / "results"
RESULTS_DIR    = BASE_DIR / "results"
BASELINE_FILE  = BASE_DIR / "baseline.json"
TABLE_FILE     = BASE_DIR / "comparison_table.md"
SIDE_BY_SIDE_FILE = BASE_DIR / "side_by_side.md"


# ── Helpers ───────────────────────────────────────────────────────────────────

def _trunc(s: str | None, n: int) -> str:
    if not s:
        return "—"
    s = s.replace("\n", " ").replace("|", "\\|")
    return s[:n] + ("…" if len(s) > n else "")


def next_run_id() -> str:
    RESULTS_DIR.mkdir(exist_ok=True)
    existing = sorted(
        p.name for p in RESULTS_DIR.iterdir()
        if p.is_dir() and p.name.startswith("run_")
    )
    if not existing:
        return "run_001"
    return f"run_{int(existing[-1].split('_')[1]) + 1:03d}"


def load_questions(q_range: str | None = None) -> list[dict]:
    all_qs = json.loads(QUESTIONS_FILE.read_text(encoding="utf-8"))
    if not q_range:
        return all_qs
    if "-" in q_range:
        lo, hi = q_range.split("-", 1)
        lo_n, hi_n = int(lo.lstrip("Qq")), int(hi.lstrip("Qq"))
        return [q for q in all_qs if lo_n <= int(q["q_id"].lstrip("Q")) <= hi_n]
    n = int(q_range.lstrip("Qq"))
    return [q for q in all_qs if int(q["q_id"].lstrip("Q")) == n]


# ── Chat API + query extraction ───────────────────────────────────────────────

def call_chat(question: str, conversation_id: str) -> tuple[str, float]:
    payload = {
        "messages": [{"role": "user", "content": question}],
        "user_id": USER_ID,
        "conversation_id": conversation_id,
        "model": MODEL,
    }
    parts: list[str] = []
    t0 = time.monotonic()
    with httpx.Client(timeout=180.0) as client:
        with client.stream("POST", CHAT_URL, json=payload) as resp:
            resp.raise_for_status()
            for line in resp.iter_lines():
                if not line.startswith("data: "):
                    continue
                data = line[6:].strip()
                if data == "[DONE]":
                    break
                try:
                    chunk = json.loads(data)
                    content = (
                        chunk.get("choices", [{}])[0]
                        .get("delta", {})
                        .get("content") or ""
                    )
                    parts.append(content)
                except (json.JSONDecodeError, IndexError, KeyError):
                    pass
    return "".join(parts), round(time.monotonic() - t0, 1)


def fetch_rag_query_from_db(conversation_id: str) -> str | None:
    safe = conversation_id.replace("'", "''")
    sql = (
        f"SELECT messages::text FROM chat_logs "
        f"WHERE conversation_id = '{safe}' "
        f"ORDER BY created_at DESC LIMIT 1;"
    )
    result = subprocess.run(
        ["docker", "exec", DB_CONTAINER,
         "psql", "-U", "app", "-d", "app", "-t", "-A", "-c", sql],
        capture_output=True, text=True, timeout=15, encoding="utf-8",
    )
    raw = result.stdout.strip()
    lines = [l for l in raw.splitlines() if not l.startswith("WARNING")]
    clean = "\n".join(lines).strip()
    if not clean:
        return None
    # The output IS the messages JSON (single column, no | separator)
    try:
        messages = json.loads(clean)
    except json.JSONDecodeError:
        return None
    for m in messages:
        if m.get("role") != "assistant":
            continue
        for tc in m.get("tool_calls") or []:
            fn = tc.get("function", {})
            if fn.get("name") == "rag_search":
                raw_args = fn.get("arguments", "{}")
                try:
                    args = json.loads(raw_args) if isinstance(raw_args, str) else raw_args
                    return args.get("query")
                except (json.JSONDecodeError, AttributeError):
                    return str(raw_args)
    return None


# ── RAG debug ─────────────────────────────────────────────────────────────────

def call_debug(query: str) -> dict:
    r = httpx.post(
        DEBUG_URL,
        json={"query": query, "user_id": USER_ID, "top_k": TOP_K},
        timeout=120.0,
    )
    if r.status_code != 200:
        return {"error": f"HTTP {r.status_code}: {r.text[:300]}"}
    return r.json()


def extract_retrieval_metrics(q: dict, data: dict) -> dict:
    if "error" in data:
        return {"error": data["error"], "correct_chunk_found": None}

    bd   = data.get("search_breakdown", {})
    pre  = bd.get("pre_rerank", [])
    post = data.get("post_rerank") or []

    expected_idx = q.get("chunk_index")
    exp_list = (
        [] if expected_idx is None else
        expected_idx if isinstance(expected_idx, list) else [expected_idx]
    )
    exp_set = set(exp_list)

    pre_idx  = [e.get("chunk_index") for e in pre]
    post_idx = [e.get("chunk_index") for e in post]

    dense_idxs  = {e.get("chunk_index") for e in bd.get("dense_leg", [])}
    sparse_idxs = {e.get("chunk_index") for e in bd.get("sparse_leg", [])}
    grep_idxs: set = set()
    for e in pre:
        if e.get("grep_contrib", 0) > 0:
            grep_idxs.add(e.get("chunk_index"))

    all_retrieved = set(pre_idx) | set(post_idx)
    found_chunks  = sorted(c for c in exp_list if c in all_retrieved)
    chunk_recall  = len(found_chunks) / len(exp_list) if exp_list else None

    rank_before = correct_dense = None
    for i, e in enumerate(pre):
        if e.get("chunk_index") in exp_set:
            rank_before   = i + 1
            correct_dense = e.get("cosine_similarity")
            break

    rank_after = correct_rerank = None
    for i, e in enumerate(post):
        if e.get("chunk_index") in exp_set:
            rank_after    = i + 1
            correct_rerank = e.get("rerank_score")
            break

    rerank_improved = (
        rank_after < rank_before
        if rank_before is not None and rank_after is not None else None
    )

    return {
        "correct_chunk_found":       len(found_chunks) > 0,
        "expected_chunks":           exp_list,
        "found_chunks":              found_chunks,
        "dense_found":               sorted(c for c in exp_list if c in dense_idxs),
        "sparse_found":              sorted(c for c in exp_list if c in sparse_idxs),
        "grep_found":                sorted(c for c in exp_list if c in grep_idxs),
        "chunk_recall":              chunk_recall,
        "rank_before_rerank":        rank_before,
        "rank_after_rerank":         rank_after,
        "rerank_improved":           rerank_improved,
        "correct_chunk_score_dense": correct_dense,
        "correct_chunk_score_rerank":correct_rerank,
        "top1_score_dense":          pre[0].get("cosine_similarity") if pre else None,
        "top1_score_rerank":         post[0].get("rerank_score")     if post else None,
        "pre_rerank_top5":           pre_idx[:5],
        "post_rerank_top5":          post_idx[:5],
    }


# ── Verdict ───────────────────────────────────────────────────────────────────

def compute_verdict(m: dict, b: dict | None, q: dict) -> str:
    if m.get("error"):
        return "error"
    if b is None:
        return "no_baseline"
    is_absent = q.get("chunk_index") is None
    if is_absent:
        ms = m.get("top1_score_dense")
        bs = b.get("top1_score_dense")
        if ms is None or bs is None:
            return "no_data"
        if ms < bs - 0.02:
            return "improved"
        if ms > bs + 0.02:
            return "worse"
        return "same"
    mf = m.get("correct_chunk_found")
    bf = b.get("correct_chunk_found")
    if not mf and not bf:
        return "both_missed"
    if not mf and bf:
        return "regression"
    if mf and not bf:
        return "recovered"
    mr = m.get("rank_after_rerank") or m.get("rank_before_rerank")
    br = b.get("rank_after_rerank") or b.get("rank_before_rerank")
    if mr is None or br is None:
        return "no_data"
    if mr < br:
        return "improved"
    if mr > br:
        return "worse"
    return "same"


VERDICT_EMOJI = {
    "improved":    "⬆️",
    "same":        "➡️",
    "worse":       "⬇️",
    "regression":  "🔴",
    "recovered":   "🟢",
    "both_missed": "⬜",
    "no_baseline": "—",
    "no_data":     "❓",
    "error":       "💥",
    "skipped":     "⏭️",
}


# ── Summary ───────────────────────────────────────────────────────────────────

def compute_summary(results: list[dict]) -> dict:
    with_exp = [r for r in results
                if not r.get("rag_not_called")
                and r["q"].get("chunk_index") is not None
                and not r["model_query_retrieval"].get("error")]
    found    = [r for r in with_exp if r["model_query_retrieval"].get("correct_chunk_found")]
    recall   = round(len(found) / len(with_exp), 3) if with_exp else None

    rr_pre   = [1.0 / r["model_query_retrieval"]["rank_before_rerank"]
                for r in with_exp if r["model_query_retrieval"].get("rank_before_rerank")]
    rr_post  = [1.0 / r["model_query_retrieval"]["rank_after_rerank"]
                for r in with_exp if r["model_query_retrieval"].get("rank_after_rerank")]
    mrr_pre  = round(sum(rr_pre)  / len(with_exp), 3) if with_exp else None
    mrr_post = round(sum(rr_post) / len(with_exp), 3) if with_exp else None

    verdicts = [r["verdict"] for r in results]
    return {
        "model":             MODEL,
        "total":             len(results),
        "rag_called":        sum(1 for r in results if not r.get("rag_not_called")),
        "rag_not_called":    sum(1 for r in results if r.get("rag_not_called")),
        "recall_at_5":       recall,
        "mrr_pre_rerank":    mrr_pre,
        "mrr_post_rerank":   mrr_post,
        "verdict_counts": {
            "improved":    verdicts.count("improved"),
            "same":        verdicts.count("same"),
            "worse":       verdicts.count("worse"),
            "regression":  verdicts.count("regression"),
            "recovered":   verdicts.count("recovered"),
            "both_missed": verdicts.count("both_missed"),
            "rag_not_called": verdicts.count("rag_not_called"),
        },
    }


# ── Comparison table ──────────────────────────────────────────────────────────

def _fmt_rank(r: int | None) -> str:
    return str(r) if r is not None else "—"


def _fmt_score(s: float | None) -> str:
    return f"{s:.3f}" if s is not None else "—"


def _fmt_delta(d: int | float | None, absent: bool = False) -> str:
    if d is None:
        return "—"
    if absent:
        if d > 0.02:
            return f"⬇️ +{d:.3f}"
        if d < -0.02:
            return f"⬆️ {d:.3f}"
        return "➡️ ~0"
    if d < 0:
        return f"⬆️ {d}"
    if d > 0:
        return f"⬇️ +{d}"
    return "➡️ 0"


def append_to_table(run_id: str, results: list[dict], summary: dict) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    model     = summary["model"]
    vc        = summary["verdict_counts"]

    verdict_line = (
        f"⬆️ {vc['improved']} improved | ➡️ {vc['same']} same | "
        f"⬇️ {vc['worse']} worse | 🔴 {vc['regression']} regression | "
        f"🟢 {vc['recovered']} recovered | ⏭️ {vc['rag_not_called']} rag_not_called"
    )

    header = [
        f"\n## {run_id} — {timestamp}",
        f"**Model:** `{model}`  ",
        f"**recall@5:** {summary['recall_at_5']} | "
        f"**MRR_pre:** {summary['mrr_pre_rerank']} | "
        f"**MRR_post:** {summary['mrr_post_rerank']}  ",
        f"**{verdict_line}**\n",
        "| Q | Diff | Category | User Question | Model Query | "
        "B.Pre | B.Post | B.Cos | "
        "M.Pre | M.Post | M.Cos | "
        "Δ Pre | Δ Post | Verdict |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]

    rows: list[str] = []
    for r in results:
        q_id      = r["q_id"]
        diff      = r["q"].get("difficulty", "—")
        cat       = r["q"].get("category", "—")
        user_q    = _trunc(r["user_question"], 50)
        model_q   = _trunc(r.get("model_query"), 50)
        verdict   = VERDICT_EMOJI.get(r["verdict"], r["verdict"])
        is_absent = r["q"].get("chunk_index") is None

        if r.get("rag_not_called"):
            rows.append(
                f"| {q_id} | {diff} | {cat} | {user_q} | *(RAG not called)* "
                f"| — | — | — | — | — | — | — | — | {verdict} |"
            )
            continue

        m = r["model_query_retrieval"]
        b = r.get("baseline_retrieval") or {}

        if is_absent:
            b_pre  = _fmt_score(b.get("top1_score_dense"))
            b_post = _fmt_score(b.get("top1_score_rerank"))
            b_cos  = "—"
            m_pre  = _fmt_score(m.get("top1_score_dense"))
            m_post = _fmt_score(m.get("top1_score_rerank"))
            m_cos  = "—"
            d_pre  = (
                round((m.get("top1_score_dense") or 0) - (b.get("top1_score_dense") or 0), 3)
                if m.get("top1_score_dense") and b.get("top1_score_dense") else None
            )
            d_post = (
                round((m.get("top1_score_rerank") or 0) - (b.get("top1_score_rerank") or 0), 3)
                if m.get("top1_score_rerank") and b.get("top1_score_rerank") else None
            )
            dps = _fmt_delta(d_pre,  absent=True)
            dqs = _fmt_delta(d_post, absent=True)
        else:
            b_pre  = _fmt_rank(b.get("rank_before_rerank"))
            b_post = _fmt_rank(b.get("rank_after_rerank"))
            b_cos  = _fmt_score(b.get("correct_chunk_score_dense"))
            m_pre  = _fmt_rank(m.get("rank_before_rerank"))
            m_post = _fmt_rank(m.get("rank_after_rerank"))
            m_cos  = _fmt_score(m.get("correct_chunk_score_dense"))
            bp_i   = b.get("rank_before_rerank")
            mp_i   = m.get("rank_before_rerank")
            ba_i   = b.get("rank_after_rerank")
            ma_i   = m.get("rank_after_rerank")
            d_pre  = (mp_i - bp_i) if mp_i and bp_i else None
            d_post = (ma_i - ba_i) if ma_i and ba_i else None
            dps    = _fmt_delta(d_pre)
            dqs    = _fmt_delta(d_post)

        rows.append(
            f"| {q_id} | {diff} | {cat} | {user_q} | {model_q} "
            f"| {b_pre} | {b_post} | {b_cos} "
            f"| {m_pre} | {m_post} | {m_cos} "
            f"| {dps} | {dqs} | {verdict} |"
        )

    if not TABLE_FILE.exists():
        TABLE_FILE.write_text(
            "# TechCorp — Query Quality Eval\n\n"
            "Compares routing model's generated query vs modelsiz baseline.\n"
            "**B** = baseline (user question direct to RAG). "
            "**M** = model-generated query.\n"
            "**Pre/Post** = rank before/after reranker (lower is better).\n"
            "**Cos** = cosine similarity of correct chunk.\n"
            "For `absent_plausible`: Pre/Post = top1 score (lower = less false-positive risk).\n"
            "**Δ** = M − B. ⬆️ improved | ⬇️ worse | 🔴 chunk dropped out of top-5.\n",
            encoding="utf-8",
        )

    with open(TABLE_FILE, "a", encoding="utf-8") as f:
        f.write("\n".join(header + rows) + "\n")


# ── Build baseline ────────────────────────────────────────────────────────────

def build_baseline() -> None:
    all_questions = load_questions()
    q_ids = {q["q_id"] for q in all_questions}

    run_dirs = sorted(
        p for p in RUNALL_DIR.iterdir()
        if p.is_dir() and p.name.startswith("run_")
    )

    baseline: dict[str, dict] = {}
    source_map: dict[str, str] = {}

    for run_dir in run_dirs:
        results_file = run_dir / "results.json"
        if not results_file.exists():
            continue
        data   = json.loads(results_file.read_text(encoding="utf-8"))
        run_id = data.get("run_id", run_dir.name)
        for r in data.get("results", []):
            q_id = r.get("q_id")
            if q_id:
                baseline[q_id]    = r
                source_map[q_id]  = run_id

    print(f"Loaded {len(baseline)} questions from {len(run_dirs)} runs.")
    missing = [qid for qid in q_ids if qid not in baseline]
    if missing:
        print(f"WARNING: No retrieval data for: {missing}")

    out = {
        "generated_at": datetime.now().isoformat(),
        "source_runs":  sorted(set(source_map.values())),
        "questions":    {},
    }
    for q_id in sorted(baseline, key=lambda x: int(x.lstrip("Q"))):
        r = baseline[q_id]
        out["questions"][q_id] = {
            "source_run":                source_map.get(q_id),
            "category":                  r.get("category"),
            "correct_chunk_found":       r.get("correct_chunk_found"),
            "expected_chunks":           r.get("expected_chunks"),
            "rank_before_rerank":        r.get("rank_before_rerank"),
            "rank_after_rerank":         r.get("rank_after_rerank"),
            "correct_chunk_score_dense": r.get("correct_chunk_score_dense"),
            "correct_chunk_score_rerank":r.get("correct_chunk_score_rerank"),
            "top1_score_dense":          r.get("top1_score_dense"),
            "top1_score_rerank":         r.get("top1_score_rerank"),
            "pre_rerank_top5":           r.get("pre_rerank_top5"),
            "post_rerank_top5":          r.get("post_rerank_top5"),
            "chunk_recall":              r.get("chunk_recall"),
            "dense_found":               r.get("dense_found"),
            "sparse_found":              r.get("sparse_found"),
        }

    BASELINE_FILE.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Baseline written → {BASELINE_FILE}")
    print(f"  Questions: {len(out['questions'])}/34  Source runs: {out['source_runs']}")


# ── Side-by-side ──────────────────────────────────────────────────────────────

def make_side_by_side(run_ids: list[str]) -> None:
    runs: list[dict] = []
    for rid in run_ids:
        path = RESULTS_DIR / rid / "results.json"
        if not path.exists():
            print(f"WARNING: {path} not found, skipping")
            continue
        runs.append(json.loads(path.read_text(encoding="utf-8")))

    if not runs:
        print("No valid runs found.")
        return

    all_q_ids = sorted(
        {r["q_id"] for run in runs for r in run["results"]},
        key=lambda x: int(x.lstrip("Q"))
    )
    run_lookup = {run["run_id"]: {r["q_id"]: r for r in run["results"]} for run in runs}

    def short_model(m: str) -> str:
        m = m.split("/")[-1]
        return m[:18] + "…" if len(m) > 18 else m

    labels    = {run["run_id"]: short_model(run["summary"]["model"]) for run in runs}
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    model_header = " | ".join(f"{labels[r['run_id']]} M.Post | Δ Post" for r in runs)
    model_sep    = " | ".join("|---|---" for _ in runs)

    lines = [
        "# TechCorp — Query Eval Side-by-Side\n",
        f"*{timestamp} | Runs: {', '.join(run_ids)}*\n",
        f"| Q | Category | B.Post | {model_header} | Verdict |",
        f"|---|---|---| {model_sep} |---|",
    ]

    for q_id in all_q_ids:
        cat = b_post_str = "—"
        for run in runs:
            row = run_lookup[run["run_id"]].get(q_id)
            if row:
                cat       = row.get("q", {}).get("category", "—")
                bm        = row.get("baseline_retrieval") or {}
                is_absent = row.get("q", {}).get("chunk_index") is None
                b_post_str = (_fmt_score(bm.get("top1_score_rerank"))
                              if is_absent else _fmt_rank(bm.get("rank_after_rerank")))
                break

        cells = []
        worst = "same"
        for run in runs:
            row = run_lookup[run["run_id"]].get(q_id)
            if not row:
                cells.append("— | —")
                continue
            if row.get("rag_not_called"):
                cells.append("skip | —")
                continue
            m   = row.get("model_query_retrieval") or {}
            b   = row.get("baseline_retrieval") or {}
            v   = row.get("verdict", "—")
            is_absent = row.get("q", {}).get("chunk_index") is None
            if is_absent:
                mps = _fmt_score(m.get("top1_score_rerank"))
                d   = (round((m.get("top1_score_rerank") or 0) -
                             (b.get("top1_score_rerank") or 0), 3)
                       if m.get("top1_score_rerank") and b.get("top1_score_rerank") else None)
                ds  = _fmt_delta(d, absent=True)
            else:
                mps = _fmt_rank(m.get("rank_after_rerank"))
                ma  = m.get("rank_after_rerank")
                ba  = b.get("rank_after_rerank")
                d   = (ma - ba) if ma and ba else None
                ds  = _fmt_delta(d)
            if v in ("regression", "worse"):
                worst = v
            cells.append(f"{mps} | {ds}")

        lines.append(
            f"| {q_id} | {cat} | {b_post_str} | {' | '.join(cells)} "
            f"| {VERDICT_EMOJI.get(worst, worst)} |"
        )

    SIDE_BY_SIDE_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Side-by-side written → {SIDE_BY_SIDE_FILE}")


# ── Main eval loop ────────────────────────────────────────────────────────────

def main(args: argparse.Namespace) -> None:
    if not BASELINE_FILE.exists():
        print(f"ERROR: baseline.json not found. Run --build-baseline first.")
        sys.exit(1)

    baseline_qs = json.loads(BASELINE_FILE.read_text(encoding="utf-8")).get("questions", {})
    questions   = load_questions(args.range)

    run_id   = next_run_id()
    run_dir  = RESULTS_DIR / run_id
    logs_dir = run_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    print(f"Run:       {run_id}")
    print(f"Model:     {MODEL}")
    print(f"Questions: {len(questions)}")
    print(f"Output:    {run_dir}")
    print("=" * 70)

    run_meta: dict = {
        "run_id":    run_id,
        "timestamp": datetime.now().isoformat(),
        "model":     MODEL,
        "results":   [],
    }
    results_file = run_dir / "results.json"
    all_results: list[dict] = []

    total = len(questions)
    for i, q in enumerate(questions):
        q_id      = q["q_id"]
        conv_id   = f"qeval-{run_id}-{q_id}"
        is_absent = q.get("chunk_index") is None
        b_metrics = baseline_qs.get(q_id)

        print(f"\n[{i+1}/{total}] {q_id} ({q.get('difficulty','?')} / {q.get('category','?')})")
        print(f"  Q: {q['question'][:80]}")

        # 1. Call chat API
        try:
            answer, latency = call_chat(q["question"], conv_id)
        except Exception as exc:
            print(f"  ERROR (chat): {exc}")
            answer, latency = f"[ERROR: {exc}]", 0.0

        # 2. Wait briefly for DB commit, then extract RAG query
        time.sleep(2.0)
        model_query = fetch_rag_query_from_db(conv_id)

        if model_query is None:
            print("  RAG not called (or DB not found)")
            (logs_dir / f"query_log_{q_id}.json").write_text(
                json.dumps({
                    "question":    q,
                    "model_query": None,
                    "model_answer": answer,
                }, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            result_row = {
                "q_id":                  q_id,
                "q":                     q,
                "user_question":         q["question"],
                "model_answer":          answer,
                "model_query":           None,
                "rag_not_called":        True,
                "model_query_retrieval": {},
                "baseline_retrieval":    b_metrics,
                "rank_delta_before":     None,
                "rank_delta_after":      None,
                "verdict":               "rag_not_called",
            }
        else:
            print(f"  model_query: {model_query[:80]}")

            # 3. Call rag_debug with model's query
            t0        = time.monotonic()
            debug_out = call_debug(model_query)
            rag_lat   = round(time.monotonic() - t0, 1)

            m_metrics = extract_retrieval_metrics(q, debug_out)
            v         = compute_verdict(m_metrics, b_metrics, q)

            # Deltas
            if is_absent:
                d_pre  = (round((m_metrics.get("top1_score_dense") or 0) -
                                (b_metrics.get("top1_score_dense") or 0), 3)
                          if b_metrics and m_metrics.get("top1_score_dense") else None)
                d_post = (round((m_metrics.get("top1_score_rerank") or 0) -
                                (b_metrics.get("top1_score_rerank") or 0), 3)
                          if b_metrics and m_metrics.get("top1_score_rerank") else None)
            else:
                bp = b_metrics.get("rank_before_rerank") if b_metrics else None
                mp = m_metrics.get("rank_before_rerank")
                ba = b_metrics.get("rank_after_rerank") if b_metrics else None
                ma = m_metrics.get("rank_after_rerank")
                d_pre  = (mp - bp) if mp and bp else None
                d_post = (ma - ba) if ma and ba else None

            if is_absent:
                print(
                    f"  absent → M.top1={m_metrics.get('top1_score_dense')}  "
                    f"B.top1={b_metrics.get('top1_score_dense') if b_metrics else '—'}  "
                    f"verdict={v}  ({rag_lat}s)"
                )
            else:
                mr = m_metrics.get("rank_after_rerank") or m_metrics.get("rank_before_rerank")
                br = (b_metrics.get("rank_after_rerank") or b_metrics.get("rank_before_rerank")) if b_metrics else "—"
                print(
                    f"  found={m_metrics.get('correct_chunk_found')}  "
                    f"M.rank={mr}  B.rank={br}  Δpost={d_post}  "
                    f"verdict={v}  ({rag_lat}s)"
                )

            (logs_dir / f"query_log_{q_id}.json").write_text(
                json.dumps({
                    "question":              q,
                    "model_query":           model_query,
                    "model_answer":          answer,
                    "model_query_retrieval": m_metrics,
                    "baseline_retrieval":    b_metrics,
                    "debug_response":        debug_out,
                }, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

            result_row = {
                "q_id":                  q_id,
                "q":                     q,
                "user_question":         q["question"],
                "model_answer":          answer,
                "model_query":           model_query,
                "rag_not_called":        False,
                "model_query_retrieval": m_metrics,
                "baseline_retrieval":    b_metrics,
                "rank_delta_before":     d_pre,
                "rank_delta_after":      d_post,
                "verdict":               v,
            }

        all_results.append(result_row)
        run_meta["results"].append(result_row)
        results_file.write_text(
            json.dumps(run_meta, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        if i < total - 1:
            print(f"\n  Waiting {RATE_LIMIT_S}s...")
            time.sleep(RATE_LIMIT_S)

    summary = compute_summary(all_results)
    run_meta["summary"] = summary
    results_file.write_text(
        json.dumps(run_meta, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    append_to_table(run_id, all_results, summary)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Model:           {MODEL}")
    print(f"  RAG called:      {summary['rag_called']}/{summary['total']}")
    print(f"  recall@5:        {summary['recall_at_5']}")
    print(f"  MRR_pre:         {summary['mrr_pre_rerank']}")
    print(f"  MRR_post:        {summary['mrr_post_rerank']}")
    print(f"  Verdicts:        {summary['verdict_counts']}")
    print(f"\n  Results : {results_file}")
    print(f"  Table   : {TABLE_FILE}")


# ── Merge runs by model ───────────────────────────────────────────────────────

MERGED_TABLE_FILE = BASE_DIR / "merged_table.md"


def merge_runs_by_model() -> None:
    """
    Reads all results/run_XXX/results.json files, groups them by model,
    and writes a consolidated merged_table.md — one section per model,
    with all 34 questions combined (latest run wins on duplicates).
    """
    run_dirs = sorted(
        p for p in RESULTS_DIR.iterdir()
        if p.is_dir() and p.name.startswith("run_")
    )

    # model → {q_id: (run_id, result_row)}
    model_data: dict[str, dict[str, tuple[str, dict]]] = {}
    model_runs: dict[str, list[str]] = {}

    for run_dir in run_dirs:
        rf = run_dir / "results.json"
        if not rf.exists():
            continue
        data = json.loads(rf.read_text(encoding="utf-8"))
        model = data.get("model", "unknown")
        run_id = data.get("run_id", run_dir.name)
        if model not in model_data:
            model_data[model] = {}
            model_runs[model] = []
        model_runs[model].append(run_id)
        for row in data.get("results", []):
            q_id = row.get("q_id")
            if q_id:
                model_data[model][q_id] = (run_id, row)

    lines = [
        "# TechCorp — Query Quality Eval (Merged per Model)\n",
        "One section per model. Same-model runs are merged (latest run wins on duplicate questions).\n",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n",
    ]

    for model in sorted(model_data.keys()):
        q_map   = model_data[model]
        run_ids = model_runs[model]
        rows    = sorted(q_map.values(), key=lambda x: int(x[1]["q_id"].lstrip("Q")))
        all_results = [r for _, r in rows]

        summary = compute_summary(all_results)
        vc      = summary["verdict_counts"]
        verdict_line = (
            f"⬆️ {vc['improved']} improved | ➡️ {vc['same']} same | "
            f"⬇️ {vc['worse']} worse | 🔴 {vc['regression']} regression | "
            f"🟢 {vc['recovered']} recovered | ⏭️ {vc['rag_not_called']} rag_not_called"
        )

        lines += [
            f"\n## {model}",
            f"**Runs merged:** {', '.join(run_ids)}  ",
            f"**Questions:** {len(all_results)}/34  ",
            f"**recall@5:** {summary['recall_at_5']} | "
            f"**MRR_pre:** {summary['mrr_pre_rerank']} | "
            f"**MRR_post:** {summary['mrr_post_rerank']}  ",
            f"**{verdict_line}**\n",
            "| Q | Diff | Category | User Question | Model Query | "
            "B.Pre | B.Post | B.Cos | "
            "M.Pre | M.Post | M.Cos | "
            "Δ Pre | Δ Post | Verdict |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
        ]

        for run_id, r in rows:
            q_id      = r["q_id"]
            diff      = r.get("q", {}).get("difficulty", "—")
            cat       = r.get("q", {}).get("category", "—")
            user_q    = _trunc(r.get("user_question"), 50)
            model_q   = _trunc(r.get("model_query"), 50)
            verdict   = VERDICT_EMOJI.get(r.get("verdict", ""), r.get("verdict", "—"))
            is_absent = r.get("q", {}).get("chunk_index") is None

            if r.get("rag_not_called"):
                lines.append(
                    f"| {q_id} | {diff} | {cat} | {user_q} | *(RAG not called)* "
                    f"| — | — | — | — | — | — | — | — | {verdict} |"
                )
                continue

            m = r.get("model_query_retrieval") or {}
            b = r.get("baseline_retrieval") or {}

            if is_absent:
                b_pre  = _fmt_score(b.get("top1_score_dense"))
                b_post = _fmt_score(b.get("top1_score_rerank"))
                b_cos  = "—"
                m_pre  = _fmt_score(m.get("top1_score_dense"))
                m_post = _fmt_score(m.get("top1_score_rerank"))
                m_cos  = "—"
                d_pre  = r.get("rank_delta_before")
                d_post = r.get("rank_delta_after")
                dps    = _fmt_delta(d_pre,  absent=True)
                dqs    = _fmt_delta(d_post, absent=True)
            else:
                b_pre  = _fmt_rank(b.get("rank_before_rerank"))
                b_post = _fmt_rank(b.get("rank_after_rerank"))
                b_cos  = _fmt_score(b.get("correct_chunk_score_dense"))
                m_pre  = _fmt_rank(m.get("rank_before_rerank"))
                m_post = _fmt_rank(m.get("rank_after_rerank"))
                m_cos  = _fmt_score(m.get("correct_chunk_score_dense"))
                d_pre  = r.get("rank_delta_before")
                d_post = r.get("rank_delta_after")
                dps    = _fmt_delta(d_pre)
                dqs    = _fmt_delta(d_post)

            lines.append(
                f"| {q_id} | {diff} | {cat} | {user_q} | {model_q} "
                f"| {b_pre} | {b_post} | {b_cos} "
                f"| {m_pre} | {m_post} | {m_cos} "
                f"| {dps} | {dqs} | {verdict} |"
            )

    MERGED_TABLE_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Merged table written → {MERGED_TABLE_FILE}")
    for model, run_ids in model_runs.items():
        q_count = len(model_data[model])
        print(f"  {model}: {q_count}/34 questions from {run_ids}")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if "--build-baseline" in sys.argv:
        build_baseline()
    elif "--merge" in sys.argv:
        merge_runs_by_model()
    elif "--side-by-side" in sys.argv:
        idx = sys.argv.index("--side-by-side")
        if idx + 1 >= len(sys.argv):
            print("Usage: --side-by-side run_001,run_002,...")
            sys.exit(1)
        make_side_by_side([r.strip() for r in sys.argv[idx + 1].split(",")])
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("--range", default=None,
                            help="Question range e.g. Q01-Q10 or Q05")
        main(parser.parse_args())
