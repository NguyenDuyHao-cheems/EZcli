"""Define the interface for an LLM client."""

from typing import Protocol

from ezcli.domain.models import GeneratedCommand


class LLMClient(Protocol):
    """Define the interface for a client that generates Bash commands."""

    def generate(
        self,
        prompt: str,
        context: dict[str, str] | None = None,
    ) -> GeneratedCommand:
        """Generate a Bash command from a prompt and optional shell context."""
        ...
