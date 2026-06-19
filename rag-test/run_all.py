"""
Full RAG retrieval test — runs all 16 questions from questions.json.

Output:
  rag-test/results/run_XXX/
    ├── results.json
    └── logs/
        ├── exploration_log_Q01.json
        ├── exploration_log_Q02.json
        └── ...
"""

import httpx
import json
import time
from datetime import datetime
from pathlib import Path

DEBUG_URL = "http://localhost:8001/tools/rag_debug"
USER_ID = "sherlock-rag-test"
TOP_K = 5
RATE_LIMIT_S = 5

BASE_DIR = Path(__file__).parent
QUESTIONS_FILE = BASE_DIR / "questions.json"
RESULTS_DIR = BASE_DIR / "results"


def next_run_id() -> str:
    RESULTS_DIR.mkdir(exist_ok=True)
    existing = sorted(p.name for p in RESULTS_DIR.iterdir() if p.is_dir() and p.name.startswith("run_"))
    if not existing:
        return "run_001"
    last_num = int(existing[-1].split("_")[1])
    return f"run_{last_num + 1:03d}"


def load_questions() -> list[dict]:
    return json.loads(QUESTIONS_FILE.read_text(encoding="utf-8"))


def call_debug(query: str) -> dict:
    r = httpx.post(
        DEBUG_URL,
        json={"query": query, "user_id": USER_ID, "top_k": TOP_K},
        timeout=120.0,
    )
    if r.status_code != 200:
        return {"error": f"HTTP {r.status_code}: {r.text[:300]}"}
    return r.json()


def extract_result(q: dict, data: dict) -> dict:
    if "error" in data:
        return {
            "q_id": q["q_id"],
            "category": q["category"],
            "error": data["error"],
            "correct_chunk_found": None,
            "rank_before_rerank": None,
            "rank_after_rerank": None,
            "rerank_improved": None,
            "correct_chunk_score_dense": None,
            "correct_chunk_score_rerank": None,
            "top1_score_dense": None,
            "top1_score_rerank": None,
            "pre_rerank_top5": [],
            "post_rerank_top5": [],
        }

    breakdown = data.get("search_breakdown", {})
    pre_rerank = breakdown.get("pre_rerank", [])
    post_rerank = data.get("post_rerank") or []

    expected_idx = q.get("chunk_index")
    if expected_idx is None:
        expected_set = set()
    elif isinstance(expected_idx, list):
        expected_set = set(expected_idx)
    else:
        expected_set = {expected_idx}

    pre_indices = [e.get("chunk_index") for e in pre_rerank]
    post_indices = [e.get("chunk_index") for e in post_rerank]

    rank_before = None
    correct_dense = None
    for i, entry in enumerate(pre_rerank):
        if entry.get("chunk_index") in expected_set:
            rank_before = i + 1
            correct_dense = entry.get("cosine_similarity")
            break

    rank_after = None
    correct_rerank = None
    for i, entry in enumerate(post_rerank):
        if entry.get("chunk_index") in expected_set:
            rank_after = i + 1
            correct_rerank = entry.get("rerank_score")
            break

    found = rank_before is not None or rank_after is not None

    rerank_improved = None
    if rank_before is not None and rank_after is not None:
        rerank_improved = rank_after < rank_before

    top1_dense = pre_rerank[0].get("cosine_similarity") if pre_rerank else None
    top1_rerank = post_rerank[0].get("rerank_score") if post_rerank else None

    return {
        "q_id": q["q_id"],
        "category": q["category"],
        "correct_chunk_found": found,
        "rank_before_rerank": rank_before,
        "rank_after_rerank": rank_after,
        "rerank_improved": rerank_improved,
        "correct_chunk_score_dense": correct_dense,
        "correct_chunk_score_rerank": correct_rerank,
        "top1_score_dense": top1_dense,
        "top1_score_rerank": top1_rerank,
        "pre_rerank_top5": pre_indices[:5],
        "post_rerank_top5": post_indices[:5],
    }


def main():
    questions = load_questions()
    run_id = next_run_id()
    run_dir = RESULTS_DIR / run_id
    logs_dir = run_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    print(f"Run: {run_id}")
    print(f"Questions: {len(questions)}")
    print(f"Output: {run_dir}")
    print("=" * 70)

    run_meta = {
        "run_id": run_id,
        "timestamp": datetime.now().isoformat(),
        "config": {},
        "results": [],
    }
    results_file = run_dir / "results.json"

    total = len(questions)
    for i, q in enumerate(questions):
        q_id = q["q_id"]
        print(f"\n[{i+1}/{total}] {q_id} ({q['category']})")
        print(f"  Q: {q['question'][:70]}...")
        print(f"  Expected chunk_index: {q.get('chunk_index')}")

        t0 = time.monotonic()
        data = call_debug(q["question"])
        duration = round(time.monotonic() - t0, 1)

        # Save exploration log
        log_file = logs_dir / f"exploration_log_{q_id}.json"
        log_file.write_text(
            json.dumps({"question": q, "debug_response": data}, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        # Update config from first successful response
        if not run_meta["config"] and "config" in data:
            run_meta["config"] = data["config"]

        # Extract summary
        result = extract_result(q, data)
        run_meta["results"].append(result)

        # Save after every question
        results_file.write_text(
            json.dumps(run_meta, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # Print summary line
        found = result["correct_chunk_found"]
        rb = result["rank_before_rerank"]
        ra = result["rank_after_rerank"]
        improved = result["rerank_improved"]
        err = result.get("error")
        if err:
            print(f"  ERROR: {err}")
        else:
            print(f"  found={found}  rank_before={rb}  rank_after={ra}  rerank_improved={improved}  ({duration}s)")

        # Rate limit between questions
        if i < total - 1:
            time.sleep(RATE_LIMIT_S)

    # Final summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    results = run_meta["results"]
    total_q = len(results)
    found_count = sum(1 for r in results if r["correct_chunk_found"] is True)
    not_found = sum(1 for r in results if r["correct_chunk_found"] is False)
    no_expected = sum(1 for r in results if r["correct_chunk_found"] is None)
    rerank_helped = sum(1 for r in results if r["rerank_improved"] is True)
    rerank_same = sum(1 for r in results if r["rerank_improved"] is False)
    errors = sum(1 for r in results if "error" in r)

    print(f"  Total questions  : {total_q}")
    print(f"  Chunk found      : {found_count}/{total_q}")
    print(f"  Chunk not found  : {not_found}/{total_q}")
    print(f"  No expected chunk: {no_expected}/{total_q}")
    print(f"  Rerank improved  : {rerank_helped}")
    print(f"  Rerank same/worse: {rerank_same}")
    print(f"  Errors           : {errors}")
    print(f"\n  Results: {results_file}")


if __name__ == "__main__":
    main()
