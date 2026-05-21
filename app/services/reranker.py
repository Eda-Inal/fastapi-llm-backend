from __future__ import annotations

import time
from typing import Any

import httpx
import structlog

from app.core.config import settings

logger = structlog.get_logger()


class RerankerService:
    """
    Optional reranker that re-scores retrieved chunks using a cross-encoder
    model (e.g. Jina Reranker).  When disabled, the original retrieval order
    is preserved.

    API contract follows the Jina / Cohere ``POST /rerank`` format:
      Request:  {model, query, documents: [str], top_n?}
      Response: {results: [{index, relevance_score, document: {text}}]}
    """

    def __init__(self) -> None:
        self._client: httpx.AsyncClient | None = None

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=settings.reranker_base_url,
                headers={
                    "Authorization": f"Bearer {settings.reranker_api_key}",
                    "Content-Type": "application/json",
                },
                timeout=httpx.Timeout(settings.reranker_timeout),
            )
        return self._client

    @property
    def enabled(self) -> bool:
        return settings.reranker_enabled and bool(settings.reranker_api_key)

    async def rerank(
        self,
        query: str,
        documents: list[str],
        top_n: int | None = None,
    ) -> list[tuple[int, float]]:
        """
        Rerank *documents* by relevance to *query*.

        Returns a list of (original_index, relevance_score) tuples sorted by
        descending relevance.  On failure, returns the original order with
        score 0.0 so the caller can fall back gracefully.
        """
        if not self.enabled or not documents:
            return [(i, 0.0) for i in range(len(documents))]

        effective_top_n = top_n or settings.reranker_top_n or len(documents)

        payload: dict[str, Any] = {
            "model": settings.reranker_model,
            "query": query,
            "documents": documents,
            "top_n": effective_top_n,
        }

        started = time.perf_counter()
        try:
            r = await self._get_client().post("/rerank", json=payload)
            latency_ms = int((time.perf_counter() - started) * 1000)

            if r.status_code >= 400:
                logger.error(
                    "reranker_http_error",
                    status=r.status_code,
                    latency_ms=latency_ms,
                )
                return [(i, 0.0) for i in range(len(documents))]

            data = r.json()
            results = data.get("results") if isinstance(data, dict) else None
            if not isinstance(results, list):
                logger.error("reranker_invalid_response", latency_ms=latency_ms)
                return [(i, 0.0) for i in range(len(documents))]

            ranked: list[tuple[int, float]] = []
            for item in results:
                if not isinstance(item, dict):
                    continue
                idx = item.get("index")
                score = item.get("relevance_score", 0.0)
                if isinstance(idx, int) and 0 <= idx < len(documents):
                    ranked.append((idx, float(score)))

            ranked.sort(key=lambda x: x[1], reverse=True)

            logger.info(
                "reranker_success",
                input_docs=len(documents),
                output_docs=len(ranked),
                top_score=ranked[0][1] if ranked else 0.0,
                latency_ms=latency_ms,
            )
            return ranked

        except Exception:
            latency_ms = int((time.perf_counter() - started) * 1000)
            logger.error("reranker_unexpected_error", latency_ms=latency_ms, exc_info=True)
            return [(i, 0.0) for i in range(len(documents))]
