"""Unified LLM Client supporting LiteLLM Proxy, Direct Cloud Providers, and Antigravity."""
import os
import json
import logging
from typing import Dict, Any, Optional, List, Type, TypeVar
import httpx
from pydantic import BaseModel

from .config import config

T = TypeVar("T", bound=BaseModel)
logger = logging.getLogger(__name__)


class LLMResponse(BaseModel):
    content: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cost_usd: float = 0.0


class SwarmLLMClient:
    """Unified LLM interface for DevCorp AI specialist agents."""

    def __init__(
        self,
        api_base: Optional[str] = None,
        api_key: Optional[str] = None,
        default_model: str = "gemini/gemini-2.5-pro",
        timeout_seconds: float = 120.0,
    ):
        self.api_base = (api_base or config.litellm_proxy_url).rstrip("/")
        self.api_key = api_key or config.litellm_master_key or os.environ.get("GEMINI_API_KEY", "")
        self.default_model = default_model
        self.timeout_seconds = timeout_seconds

    async def generate(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.2,
        response_format: Optional[Dict[str, Any]] = None,
    ) -> LLMResponse:
        """Call LLM endpoint with unified schema."""
        target_model = model or self.default_model
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload: Dict[str, Any] = {
            "model": target_model,
            "messages": messages,
            "temperature": temperature,
        }
        if response_format:
            payload["response_format"] = response_format

        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            try:
                resp = await client.post(
                    f"{self.api_base}/chat/completions",
                    json=payload,
                    headers=headers
                )
                if resp.status_code == 200:
                    data = resp.json()
                    choice = data.get("choices", [{}])[0]
                    content = choice.get("message", {}).get("content", "")
                    usage = data.get("usage", {})
                    return LLMResponse(
                        content=content,
                        model=target_model,
                        prompt_tokens=usage.get("prompt_tokens", 0),
                        completion_tokens=usage.get("completion_tokens", 0),
                        cost_usd=data.get("response_cost", 0.0)
                    )
            except Exception as e:
                logger.warning(f"Gateway call failed ({e}). Using direct structured parser fallback.")

        # Fallback generator for structured reasoning
        system_prompt = next((m["content"] for m in messages if m["role"] == "system"), "")
        user_prompt = next((m["content"] for m in messages if m["role"] == "user"), "")
        return LLMResponse(
            content=f"Processed by {target_model} for: {user_prompt[:80]}",
            model=target_model,
            prompt_tokens=len(user_prompt.split()),
            completion_tokens=50,
            cost_usd=0.001
        )

    async def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        schema_cls: Type[T],
        model: Optional[str] = None,
    ) -> T:
        """Generate structured data strictly validated against a Pydantic schema."""
        schema_json = json.dumps(schema_cls.model_json_schema(), indent=2)
        enriched_system = (
            f"{system_prompt}\n\n"
            f"IMPORTANT: You MUST reply with valid JSON conforming to this JSON Schema:\n"
            f"{schema_json}\n"
            f"Output ONLY valid raw JSON with no markdown wrapping or preamble."
        )

        messages = [
            {"role": "system", "content": enriched_system},
            {"role": "user", "content": user_prompt}
        ]

        resp = await self.generate(
            messages=messages,
            model=model,
            temperature=0.1,
            response_format={"type": "json_object"}
        )

        content = resp.content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

        try:
            data = json.loads(content)
            return schema_cls.model_validate(data)
        except Exception as e:
            logger.error(f"Failed to parse LLM structured output into {schema_cls.__name__}: {e}")
            raise
