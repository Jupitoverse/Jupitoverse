"""
LangChain-compatible ChatModel for Amdocs OpenAI API Gateway.
Endpoint: POST https://ai-framework1:8085/api/v1/call_llm
Headers: API-Key, X-Effective-Caller, Content-Type, accept
Payload: llm_model, messages, max_tokens [, tools, tool_choice ]
"""

import json
import os
import urllib3
from contextvars import ContextVar
from typing import Any, Callable, List, Optional, Sequence, Union

import requests
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.tools import BaseTool
from langchain_core.utils.function_calling import convert_to_openai_tool

# Suppress InsecureRequestWarning when verify_ssl=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Context var so _generate can see bound tools when invoked via .bind(tools=...)
_AMDOCS_INVOKE_CONFIG: ContextVar[Optional[dict]] = ContextVar("_AMDOCS_INVOKE_CONFIG", default=None)


def _message_to_dict(msg: BaseMessage) -> dict:
    """Convert LangChain message to Amdocs API format {role, content}."""
    if isinstance(msg, HumanMessage):
        role = "user"
    elif isinstance(msg, AIMessage):
        role = "assistant"
    elif isinstance(msg, SystemMessage):
        role = "system"
    else:
        role = getattr(msg, "type", "user").replace("_", "")
        if role == "human":
            role = "user"
    content = msg.content if isinstance(msg.content, str) else str(msg.content)
    return {"role": role, "content": content}


class AmdocsChatOpenAI(BaseChatModel):
    """Chat model that calls Amdocs OpenAI Gateway (call_llm API)."""

    api_url: str = "https://ai-framework1:8085/api/v1/call_llm"
    api_key: str = ""
    effective_caller: str = "abhisha3@amdocs.com"
    llm_model: str = "gpt-4.1"
    max_tokens: int = 8000
    verify_ssl: bool = False

    class Config:
        arbitrary_types_allowed = True

    @property
    def _llm_type(self) -> str:
        return "amdocs_openai"

    def bind_tools(
        self,
        tools: Sequence[Union[dict, type, Callable, BaseTool]],
        *,
        tool_choice: Optional[Union[dict, str, bool]] = None,
        **kwargs: Any,
    ):
        """Bind tools for agent tool-calling. Returns self.bind(tools=..., tool_choice=...)."""
        formatted = [convert_to_openai_tool(t) for t in tools]
        if tool_choice is not None and tool_choice not in ("auto", "none", "any", "required"):
            if isinstance(tool_choice, str):
                tool_choice = {"type": "function", "function": {"name": tool_choice}}
            elif tool_choice is True:
                tool_choice = "required"
        return self.bind(tools=formatted, tool_choice=tool_choice, **kwargs)

    def invoke(self, input: Any, config: Optional[dict] = None, **kwargs: Any):
        """Set config in context so _generate can read bound tools."""
        token = _AMDOCS_INVOKE_CONFIG.set(config or {})
        try:
            return super().invoke(input, config=config, **kwargs)
        finally:
            _AMDOCS_INVOKE_CONFIG.reset(token)

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        headers = {
            "Content-Type": "application/json",
            "accept": "application/json",
            "API-Key": self.api_key or os.getenv("AMDOCS_API_KEY", ""),
            "X-Effective-Caller": self.effective_caller or os.getenv("AMDOCS_EFFECTIVE_CALLER", ""),
        }
        payload = {
            "llm_model": kwargs.get("llm_model", self.llm_model),
            "messages": [_message_to_dict(m) for m in messages],
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
        }
        config = _AMDOCS_INVOKE_CONFIG.get() or {}
        if config.get("tools"):
            payload["tools"] = config["tools"]
        if config.get("tool_choice") is not None:
            payload["tool_choice"] = config["tool_choice"]

        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                verify=self.verify_ssl,
                timeout=120,
            )
            response.raise_for_status()
        except requests.HTTPError as e:
            body = ""
            try:
                body = e.response.text or ""
            except Exception:
                pass
            msg = f"Amdocs gateway error {e.response.status_code}: {e}. Response: {body[:500]}"
            if "invalid token" in body.lower() or "regenerate your token" in body.lower():
                msg += " → Regenerate your API token in the Amdocs LLM portal and update AMDOCS_API_KEY in .env"
            raise RuntimeError(msg) from e
        data = response.json()

        msg_block = None
        if "choices" in data and len(data["choices"]) > 0:
            msg_block = data["choices"][0].get("message", data["choices"][0])
        elif "message" in data and isinstance(data["message"], dict):
            msg_block = data["message"]

        if msg_block is None:
            content = data.get("content", str(data))
            generation = ChatGeneration(message=AIMessage(content=content))
            return ChatResult(generations=[generation])

        content = msg_block.get("content", "") or ""
        tool_calls_raw = msg_block.get("tool_calls")
        if tool_calls_raw:
            tool_calls = []
            for tc in tool_calls_raw:
                fn = tc.get("function", {})
                args_str = fn.get("arguments", "{}")
                if isinstance(args_str, dict):
                    args_str = json.dumps(args_str)
                try:
                    args = json.loads(args_str)
                except json.JSONDecodeError:
                    args = {}
                tool_calls.append({
                    "name": fn.get("name", ""),
                    "args": args,
                    "id": tc.get("id", ""),
                })
            generation = ChatGeneration(
                message=AIMessage(content=content or "", tool_calls=tool_calls)
            )
        else:
            generation = ChatGeneration(message=AIMessage(content=content))
        return ChatResult(generations=[generation])
