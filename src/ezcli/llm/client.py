"""Define the interface for an LLM client."""

from typing import Protocol

from ezcli.llm.result import LLMResult


class LLMClient(Protocol):
    """Define the interface for an LLM client."""

    def generate(self, prompt: str) -> LLMResult:
        """Generate a response from the given prompt."""
        ...
