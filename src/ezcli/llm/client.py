"""Define the interface for an LLM client."""

from typing import Protocol

from ezcli.llm.result import LLMResult


class LLMClient(Protocol):
    """Define the interface for a client that generates Bash commands."""

    def generate(
        self,
        prompt: str,
        context: dict[str, str] | None = None,
    ) -> LLMResult:
        """Generate a Bash command result from a prompt and shell context."""

        ...
