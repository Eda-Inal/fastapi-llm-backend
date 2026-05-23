from __future__ import annotations

import os
from typing import Any

import structlog

logger = structlog.get_logger()


def is_enabled() -> bool:
    from app.core.config import settings
    return settings.langsmith_tracing_enabled and bool(settings.langsmith_api_key)


def _configure_env() -> None:
    from app.core.config import settings
    if settings.langsmith_api_key:
        os.environ["LANGCHAIN_API_KEY"] = settings.langsmith_api_key
    os.environ["LANGCHAIN_PROJECT"] = settings.langsmith_project
    os.environ["LANGCHAIN_TRACING_V2"] = "true"


def create_run(
    name: str,
    run_type: str,
    inputs: dict[str, Any],
    parent_run=None,
    metadata: dict[str, Any] | None = None,
    tags: list[str] | None = None,
):
    """
    Create and post a LangSmith RunTree.
    Returns None when tracing is disabled or if an error occurs,
    so callers can treat None as a no-op sentinel.
    """
    if not is_enabled():
        return None
    try:
        _configure_env()
        from langsmith.run_trees import RunTree  # lazy import

        kwargs: dict[str, Any] = dict(
            name=name,
            run_type=run_type,
            inputs=inputs,
            tags=tags or [],
            extra={"metadata": metadata or {}},
        )

        if parent_run is not None:
            run = parent_run.create_child(**kwargs)
        else:
            from app.core.config import settings
            run = RunTree(project_name=settings.langsmith_project, **kwargs)

        run.post()
        return run
    except Exception:
        logger.warning("langsmith_create_run_failed", exc_info=True)
        return None


def end_run(run, outputs: dict[str, Any], error: str | None = None) -> None:
    """End and patch a RunTree. Safe to call with run=None."""
    if run is None:
        return
    try:
        if error:
            run.end(error=error)
        else:
            run.end(outputs=outputs)
        run.patch()
    except Exception:
        logger.warning("langsmith_end_run_failed", exc_info=True)
