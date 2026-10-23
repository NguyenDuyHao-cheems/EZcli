"""Client for generating Bash commands through a local Ollama instance."""

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from ezcli.llm.client import LLMClient
from ezcli.llm.mock import MockLLMProvider
from ezcli.llm.prompts import (
    BASH_SYSTEM_PROMPT,
    EXPLANATION_SYSTEM_PROMPT,
    build_bash_user_prompt,
    build_explanation_user_prompt,
)
from ezcli.llm.result import LLMResult

__all__ = [
    "LLMClient",
    "LLMResult",
    "MockLLMProvider",
    "OllamaClient",
    "BASH_SYSTEM_PROMPT",
    "EXPLANATION_SYSTEM_PROMPT",
    "build_bash_user_prompt",
    "build_explanation_user_prompt",
]


class OllamaClient:
    """Generate Bash commands using Ollama's local HTTP API."""

    def __init__(
        self,
        model: str = "qwen2.5-coder:3b",
        base_url: str = "http://localhost:11434",
        timeout: float = 30.0,
    ) -> None:
        self._model = model
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    def generate(
        self,
        prompt: str,
        context: dict[str, str] | None = None,
    ) -> LLMResult:
        """Generate a Bash command without executing it."""
        if not prompt.strip():
            raise ValueError("Prompt must not be empty.")

        result = self._chat(
            system_prompt=BASH_SYSTEM_PROMPT,
            user_prompt=build_bash_user_prompt(prompt, context),
        )
        if not result.success:
            return result

        command = result.content.strip()
        if "```" in command:
            return LLMResult(
                success=False,
                content="",
                error="Ollama returned Markdown instead of a Bash command.",
            )

        if "\n" in command or "\r" in command:
            return LLMResult(
                success=False,
                content="",
                error="Ollama returned more than one command line.",
            )

        return LLMResult(success=True, content=command)

    def explain(self, command: str) -> LLMResult:
        """Generate an explanation only when explicitly requested."""
        if not command.strip():
            raise ValueError("Command must not be empty.")

        return self._chat(
            system_prompt=EXPLANATION_SYSTEM_PROMPT,
            user_prompt=build_explanation_user_prompt(command),
        )

    def _chat(self, *, system_prompt: str, user_prompt: str) -> LLMResult:
        """Send one non-streaming chat request to Ollama."""
        payload = {
            "model": self._model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
        }
        request = Request(
            url=f"{self._base_url}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urlopen(request, timeout=self._timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            return LLMResult(
                success=False,
                content="",
                error=f"Ollama returned HTTP error {exc.code}.",
            )
        except TimeoutError:
            return LLMResult(
                success=False,
                content="",
                error=f"Ollama request timed out after {self._timeout:g} seconds.",
            )
        except (URLError, OSError):
            return LLMResult(
                success=False,
                content="",
                error="Could not connect to Ollama. Check that Ollama is running.",
            )
        except (json.JSONDecodeError, UnicodeDecodeError):
            return LLMResult(
                success=False,
                content="",
                error="Ollama returned an invalid response.",
            )

        if not isinstance(data, dict):
            return LLMResult(
                success=False,
                content="",
                error="Ollama returned an unexpected response format.",
            )

        provider_error = data.get("error")
        if isinstance(provider_error, str) and provider_error.strip():
            return LLMResult(
                success=False,
                content="",
                error=f"Ollama returned an error: {provider_error.strip()}",
            )

        message = data.get("message")
        if not isinstance(message, dict):
            return LLMResult(
                success=False,
                content="",
                error="Ollama returned an unexpected response format.",
            )

        generated_text = message.get("content")
        if not isinstance(generated_text, str):
            return LLMResult(
                success=False,
                content="",
                error="Ollama returned an unexpected assistant content format.",
            )

        content = generated_text.strip()
        if not content:
            return LLMResult(
                success=False,
                content="",
                error="Ollama returned empty assistant content.",
            )

        return LLMResult(success=True, content=content)
