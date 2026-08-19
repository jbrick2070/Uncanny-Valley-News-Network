from __future__ import annotations
import json
import urllib.request
import urllib.error
from typing import Optional

from .provider_base import LLMProvider

class LocalOpenAIProvider(LLMProvider):
    """
    Connects to any local OpenAI-compatible endpoint (LM Studio, Ollama, vLLM)
    using only standard library urllib.
    """
    def __init__(self, base_url: str = "http://127.0.0.1:1234/v1", model: str = "default"):
        self.base_url = base_url.rstrip('/')
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.8,
            "max_tokens": 300
        }

        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )

        try:
            with urllib.request.urlopen(req) as response:
                body = response.read()
                data = json.loads(body)
                return data["choices"][0]["message"]["content"].strip()
        except urllib.error.URLError as e:
            print(f"[LocalOpenAIProvider] Failed to connect or generate: {e}")
            # Fallback to returning a minimal default to prevent crashing
            return "Dynamic live broadcast footage, chaotic news anchor reading a strange report, VHS aesthetic, talking, highly detailed."
