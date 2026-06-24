from typing import Dict, List, Optional

import requests

from app.core.config import LLMConfig


class OpenAICompatibleClient:
    def __init__(self, config: LLMConfig):
        self.config = config

    def is_configured(self) -> bool:
        return bool(
            self.config.enabled
            and self.config.base_url.strip()
            and self.config.model.strip()
        )

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        if not self.is_configured():
            raise RuntimeError("LLM client is not fully configured")

        url = self._build_chat_completion_url()
        headers = {
            "Content-Type": "application/json",
        }
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"

        payload = {
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.temperature if temperature is None else temperature,
            "max_tokens": self.config.max_tokens if max_tokens is None else max_tokens,
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=self.config.timeout,
        )
        response.raise_for_status()
        response_data = response.json()

        choices = response_data.get("choices") or []
        if not choices:
            raise RuntimeError("No choices returned from LLM API")

        message = choices[0].get("message") or {}
        content = message.get("content")
        if isinstance(content, list):
            text_parts = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
            content = "\n".join(part for part in text_parts if part)

        if not content:
            raise RuntimeError("Empty content returned from LLM API")

        return content.strip()

    def _build_chat_completion_url(self) -> str:
        base_url = self.config.base_url.rstrip("/")
        if base_url.endswith("/chat/completions"):
            return base_url
        return f"{base_url}/chat/completions"
