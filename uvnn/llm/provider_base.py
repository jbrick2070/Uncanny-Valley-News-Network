from __future__ import annotations
import abc

class LLMProvider(abc.ABC):
    """Base interface for all upstream LLM prompters."""

    @abc.abstractmethod
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generate text given a system instructions and a user prompt.
        """
        pass
