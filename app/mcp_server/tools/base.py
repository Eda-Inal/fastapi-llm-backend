from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


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

    @abstractmethod
    async def run(self, args: dict[str, Any]) -> ToolResult:
        raise NotImplementedError
