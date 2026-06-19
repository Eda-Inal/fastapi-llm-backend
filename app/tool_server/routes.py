import time
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel
import structlog

from app.core.config import settings
from app.db.repositories.document import debug_search
from app.db.session import AsyncSessionLocal
from app.services.embeddings import EmbeddingService
from app.services.reranker import RerankerService
from app.services.rag_metrics import rag_metrics
from app.tool_server.tools.registry import ToolRegistry

logger = structlog.get_logger()

router = APIRouter()
registry = ToolRegistry()

_embed_service = EmbeddingService()
_reranker = RerankerService()


class ToolCallRequest(BaseModel):
    name: str
    arguments: dict


class RagDebugRequest(BaseModel):
    query: str
    user_id: str
    top_k: Optional[int] = 5
    similarity_threshold: Optional[float] = 0.7


@router.get("/tools")
async def list_tools():
    tools = registry.openai_tools()
    return {"tools": tools}


@router.get("/metrics")
async def get_metrics() -> dict:
    """Expose in-process RAG metrics so the API can proxy them."""
    return rag_metrics.snapshot()


@router.post("/tools/call")
async def call_tool(payload: ToolCallRequest):
    name = payload.name
    args = payload.arguments or {}

    log = logger.bind(tool=name)
    log.info("tool_call_started", name=name)

    tool = registry.get(name)
    if tool is None:
        return {"success": False, "result": "Tool not found"}

    try:
        result = await tool.execute(args)
        return {"success": result.ok, "result": result.content}
    except Exception:
        log.error("tool_call_failed", exc_info=True)
        return {"success": False, "result": "Tool execution failed"}


# --- RAG test endpoint (used by rag-test/run_all.py) ---
# Exposes full retrieval pipeline internals: per-leg scores, RRF breakdown,
# rerank before/after comparison, latency breakdown. Not for production use.
@router.post("/tools/rag_debug")
async def rag_debug(payload: RagDebugRequest):
    """Full RAG retrieval breakdown: embedding, per-leg scores, reranking."""
    t0 = time.perf_counter()

    # 1. Embedding
    embed_t0 = time.perf_counter()
    emb = await _embed_service.embed_text(
        "Represent this sentence for searching relevant passages: " + payload.query.strip()
    )
    embedding_ms = round((time.perf_counter() - embed_t0) * 1000, 1)
    if emb is None:
        return {"error": "Embedding failed"}

    # 2. DB search with full debug breakdown
    search_t0 = time.perf_counter()
    is_hybrid = settings.hybrid_search_enabled
    fetch_k = (
        payload.top_k * settings.reranker_overfetch_multiplier
        if _reranker.enabled
        else payload.top_k
    )
    async with AsyncSessionLocal() as session:
        breakdown = await debug_search(
            session,
            query_vector=emb.vector,
            query_text=payload.query.strip() if is_hybrid else None,
            top_k=fetch_k if _reranker.enabled else payload.top_k,
            metadata_filter={"user_id": payload.user_id},
            embedding_model=settings.embedding_model_name,
        )
    search_ms = round((time.perf_counter() - search_t0) * 1000, 1)

    # 3. Reranking (if enabled)
    rerank_result = None
    post_rerank = None
    if _reranker.enabled and breakdown["pre_rerank"]:
        candidate_texts = [
            entry["text_full"] for entry in breakdown["pre_rerank"]
            if "text_full" in entry
        ]
        rerank_t0 = time.perf_counter()
        rerank_pairs = await _reranker.rerank(
            query=payload.query.strip(),
            documents=candidate_texts,
            top_n=payload.top_k,
        )
        rerank_ms = round((time.perf_counter() - rerank_t0) * 1000, 1)

        post_rerank = []
        for new_rank, (orig_idx, rerank_score) in enumerate(rerank_pairs, 1):
            if orig_idx < len(breakdown["pre_rerank"]):
                entry = {**breakdown["pre_rerank"][orig_idx]}
                entry["rerank_score"] = round(rerank_score, 5)
                entry["pre_rerank_position"] = orig_idx + 1
                entry["post_rerank_position"] = new_rank
                entry.pop("text_full", None)
                post_rerank.append(entry)

        rerank_result = {
            "enabled": True,
            "latency_ms": rerank_ms,
            "input_count": len(candidate_texts),
            "output_count": len(post_rerank),
        }
    else:
        rerank_result = {"enabled": False}

    # Strip text_full from pre_rerank (too large for JSON response)
    for entry in breakdown["pre_rerank"]:
        entry.pop("text_full", None)

    total_ms = round((time.perf_counter() - t0) * 1000, 1)

    return {
        "query": payload.query,
        "user_id": payload.user_id,
        "config": {
            "embedding_model": settings.embedding_model_name,
            "hybrid_search": is_hybrid,
            "grep_search": settings.grep_search_enabled,
            "reranker_enabled": _reranker.enabled,
            "rrf_k": settings.hybrid_rrf_k,
            "requested_top_k": payload.top_k,
            "fetch_k": fetch_k,
        },
        "latency": {
            "embedding_ms": embedding_ms,
            "search_ms": search_ms,
            "rerank_ms": rerank_result.get("latency_ms"),
            "total_ms": total_ms,
        },
        "search_breakdown": breakdown,
        "reranker": rerank_result,
        "post_rerank": post_rerank,
    }
