import httpx
from app.tool_server.tools.base import Tool, ToolResult
from app.core.config import settings


class WebSearchTool(Tool):
    name = "web_search"
    description = (
        "Search the public web (via Tavily) for live or current information — "
        "weather, news, real-time events, recent updates. "
        "Returns up to 3 results as a combined text snippet with URLs and content excerpts. "
        "This is NOT a fallback for rag_search; use only when the question explicitly "
        "requires current or live external information."
    )
    parameters = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query — a concise, keyword-rich phrase. Use natural language, not boolean operators.",
            }
        },
        "required": ["query"],
    }

    def __init__(self) -> None:
        self._client: httpx.AsyncClient | None = None

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=10)
        return self._client

    async def run(self, args: dict) -> ToolResult:
        try:
            query = args.get("query")
            if not isinstance(query, str) or not query.strip():
                return ToolResult(ok=False, content="Web search not used: missing or invalid query.")

            if not getattr(settings, "tavily_api_key", None):
                return ToolResult(ok=False, content="Web search not available: missing Tavily API key.")

            payload = {
                "api_key": settings.tavily_api_key,
                "query": query,
                "max_results": 3,
            }

            r = await self._get_client().post("https://api.tavily.com/search", json=payload)
            if r.status_code >= 400:
                return ToolResult(ok=False, content=f"Web search failed: HTTP {r.status_code}")
            data = r.json()

            results = data.get("results", [])
            if not isinstance(results, list) or not results:
                return ToolResult(ok=True, content="Web search returned no results.")

            formatted = "\n".join(
                f"{i.get('url', '')}: {i.get('content', '')}"
                for i in results
                if isinstance(i, dict)
            ).strip()
            return ToolResult(ok=True, content=formatted or "Web search returned results but could not format them.")

        except Exception:
            return ToolResult(ok=False, content="Web search failed due to an unexpected error.")
