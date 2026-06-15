from collections.abc import AsyncIterator

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.repositories.chat_log import create_chat_log
from app.db.repositories.document import has_documents_for_user
from app.services.groq_client import LLMClient
from app.services.react_agent_prompts import build_system_prompt, parse_react_response
from app.services.tool_client.remote_client import RemoteToolClient

logger = structlog.get_logger()

# Phrases that indicate the user explicitly asked for a web search, in
# addition to whatever tool context-based selection would otherwise pick.
_WEB_SEARCH_TRIGGERS = (
    "search the web",
    "search online",
    "look online",
    "look it up online",
    "web search",
    "webde ara",
    "web'de ara",
    "internette ara",
    "internet'te ara",
)


def _user_requested_web_search(messages: list[dict]) -> bool:
    for m in reversed(messages):
        if m.get("role") == "user":
            content = (m.get("content") or "").lower()
            return any(trigger in content for trigger in _WEB_SEARCH_TRIGGERS)
    return False


class ReActAgentService:
    """
    Orchestrates a text-based ReAct (Thought/Action/Observation/Final Answer)
    loop. Independent from ChatService: no native function-calling, no shared
    state with the /chat/stream pipeline.
    """

    def __init__(self) -> None:
        self.client = LLMClient()
        self.mcp = RemoteToolClient()

    async def _get_available_tools(
        self,
        *,
        session: AsyncSession,
        user_id: str | None,
        messages: list[dict],
    ) -> list[dict]:
        """
        Decide which tools the agent may use, based on context rather than
        leaving the choice to the model:
          - the user has uploaded documents -> rag_search
          - otherwise -> web_search
          - if the user explicitly asks to search the web, web_search is
            added regardless of the above
        """
        conv_has_docs = (
            user_id is not None
            and await has_documents_for_user(session, user_id=user_id)
        )

        wanted_names = {"rag_search"} if conv_has_docs else {"web_search"}
        if _user_requested_web_search(messages):
            wanted_names.add("web_search")

        tools = await self.mcp.list_tools()
        return [
            t for t in tools
            if isinstance(t, dict) and t.get("function", {}).get("name") in wanted_names
        ]

    async def stream_agent(
        self,
        *,
        session: AsyncSession,
        messages: list[dict],
        model: str,
        user_id: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        conversation_id: str | None = None,
        tags: list[str] | None = None,
    ) -> AsyncIterator[dict]:
        """
        Run the ReAct loop and yield streaming events.

        The model may call one of the available tools per iteration, observe
        the result, and continue until it produces a Final Answer or the
        iteration budget is exhausted.
        """
        log = logger.bind(model=model, conversation_id=conversation_id, user_id=user_id)

        available_tools = await self._get_available_tools(
            session=session, user_id=user_id, messages=messages
        )
        available_names = {
            t.get("function", {}).get("name") for t in available_tools
        }

        system_prompt = build_system_prompt(available_tools)
        llm_messages = [{"role": "system", "content": system_prompt}, *messages]

        log.info("agent_loop_started", tool_count=len(available_tools))

        final_answer: str | None = None
        last_raw_response = ""

        for iteration in range(settings.agent_max_iterations):
            iter_log = log.bind(iteration=iteration + 1)

            buffer: list[str] = []
            async for event in self.client.stream_chat_completion(
                messages=llm_messages,
                model=model,
                tools=None,
                temperature=temperature if temperature is not None else 0.0,
                max_tokens=max_tokens,
                stop=["Observation:"],
                call_type="agent",
            ):
                if event["type"] == "chunk":
                    if event.get("text"):
                        buffer.append(event["text"])
                elif event["type"] == "error":
                    iter_log.error("agent_llm_error", message=event.get("message"))
                    yield {"type": "error", "message": event.get("message", "LLM error")}
                    yield {"type": "done", "finish_reason": "error"}
                    return
                elif event["type"] == "done":
                    break

            raw_response = "".join(buffer)
            last_raw_response = raw_response
            parsed = parse_react_response(raw_response)

            iter_log.info(
                "agent_loop_iteration_parsed",
                has_thought=parsed["thought"] is not None,
                action=parsed["action"],
                has_final_answer=parsed["final_answer"] is not None,
            )

            if parsed["thought"]:
                yield {"type": "thought", "text": parsed["thought"]}

            if parsed["final_answer"]:
                final_answer = parsed["final_answer"]
                break

            action = parsed["action"]
            action_input = parsed["action_input"]

            if action in available_names and isinstance(action_input, dict):
                if action == "rag_search":
                    # Server-side injection -- the model never controls this.
                    metadata_filter = action_input.get("metadata_filter")
                    if not isinstance(metadata_filter, dict):
                        metadata_filter = {}
                    if user_id:
                        metadata_filter["user_id"] = user_id
                    action_input["metadata_filter"] = metadata_filter
                    tool_timeout = settings.agent_rag_timeout
                else:
                    tool_timeout = settings.agent_web_search_timeout

                yield {"type": "action", "tool": action, "args": action_input}

                tool_result = await self.mcp.call_tool(
                    action, action_input, timeout=tool_timeout
                )

                yield {
                    "type": "observation",
                    "tool": action,
                    "result": tool_result.content,
                }

                llm_messages.append({"role": "assistant", "content": raw_response})
                llm_messages.append({"role": "user", "content": f"Observation: {tool_result.content}"})
                continue

            # Unrecognized action or malformed Action Input -- stop the loop
            # with whatever text the model produced. Stage 4 refines this.
            final_answer = raw_response
            break

        if final_answer is None:
            final_answer = last_raw_response

        yield {"type": "chunk", "text": final_answer}
        yield {"type": "done", "finish_reason": "stop"}

        prompt_text = ""
        for m in reversed(messages):
            if m.get("role") == "user":
                prompt_text = m.get("content", "")
                break

        await create_chat_log(
            session=session,
            prompt=prompt_text,
            messages=messages,
            response=final_answer,
            model_name=model,
            temperature=temperature,
            max_tokens=max_tokens,
            conversation_id=conversation_id,
            turn_index=None,
            user_id=user_id,
        )
        await session.commit()
