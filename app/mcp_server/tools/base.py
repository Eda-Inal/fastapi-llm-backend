import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

import structlog

logger = structlog.get_logger()

SENSITIVE_KEYS: frozenset[str] = frozenset({
    "metadata_filter",
    "api_key",
    "password",
    "token",
    "secret",
    "authorization",
})


def _redact_args(args: dict) -> dict:
    return {
        k: "<redacted>" if k.lower() in SENSITIVE_KEYS else v
        for k, v in args.items()
    }


@dataclass
class ToolResult:
    ok: bool
    content: str


class Tool(ABC):
    """
    Abstract base class for all tools.
    """

    name: str
    description: str
    parameters: dict

    def openai_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

    async def execute(self, args: dict[str, Any]) -> ToolResult:
        """
        Wrapper around run() that adds structured logging.
        Subclasses should implement run(), not execute().
        """
        start = time.perf_counter()
        safe_args = _redact_args(args)
        logger.info(
            "tool_call_started",
            tool=self.name,
            args=safe_args,
        )
        try:
            result = await self.run(args)
            duration_ms = (time.perf_counter() - start) * 1000
            logger.info(
                "tool_call_finished",
                tool=self.name,
                ok=result.ok,
                duration_ms=round(duration_ms, 2),
                content_length=len(result.content) if result.content else 0,
            )
            return result
        except Exception:
            duration_ms = (time.perf_counter() - start) * 1000
            logger.error(
                "tool_call_unhandled_exception",
                tool=self.name,
                duration_ms=round(duration_ms, 2),
                exc_info=True,
            )
            raise

    @abstractmethod
    async def run(self, args: dict[str, Any]) -> ToolResult:
        raise NotImplementedError
