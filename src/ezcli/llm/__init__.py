"""Client for generating Bash commands through a local Ollama instance."""

import json
import time
from datetime import datetime
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from ezcli.llm.client import LLMClient
from ezcli.llm.debug_logging import configure_llm_logger
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
        self._logger = configure_llm_logger()

    def generate(
        self,
        prompt: str,
        context: dict[str, str] | None = None,
    ) -> LLMResult:
        """Generate a Bash command without executing it."""
        if not prompt.strip():
            raise ValueError("Prompt must not be empty.")

        result = self._chat(
            operation="generate",
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
            operation="explain",
            system_prompt=EXPLANATION_SYSTEM_PROMPT,
            user_prompt=build_explanation_user_prompt(command),
        )

    def _chat(
        self,
        *,
        operation: str,
        system_prompt: str,
        user_prompt: str,
    ) -> LLMResult:
        """Send one non-streaming chat request to Ollama."""
        started_at = time.perf_counter()
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
            result = LLMResult(
                success=False,
                content="",
                error=f"Ollama returned HTTP error {exc.code}.",
            )
            self._log_result(operation, system_prompt, user_prompt, result, started_at)
            return result
        except TimeoutError:
            result = LLMResult(
                success=False,
                content="",
                error=f"Ollama request timed out after {self._timeout:g} seconds.",
            )
            self._log_result(operation, system_prompt, user_prompt, result, started_at)
            return result
        except (URLError, OSError):
            result = LLMResult(
                success=False,
                content="",
                error="Could not connect to Ollama. Check that Ollama is running.",
            )
            self._log_result(operation, system_prompt, user_prompt, result, started_at)
            return result
        except (json.JSONDecodeError, UnicodeDecodeError):
            result = LLMResult(
                success=False,
                content="",
                error="Ollama returned an invalid response.",
            )
            self._log_result(operation, system_prompt, user_prompt, result, started_at)
            return result

        if not isinstance(data, dict):
            result = LLMResult(
                success=False,
                content="",
                error="Ollama returned an unexpected response format.",
            )
            self._log_result(operation, system_prompt, user_prompt, result, started_at)
            return result

        provider_error = data.get("error")
        if isinstance(provider_error, str) and provider_error.strip():
            result = LLMResult(
                success=False,
                content="",
                error=f"Ollama returned an error: {provider_error.strip()}",
            )
            self._log_result(operation, system_prompt, user_prompt, result, started_at)
            return result

        message = data.get("message")
        if not isinstance(message, dict):
            result = LLMResult(
                success=False,
                content="",
                error="Ollama returned an unexpected response format.",
            )
            self._log_result(operation, system_prompt, user_prompt, result, started_at)
            return result

        generated_text = message.get("content")
        if not isinstance(generated_text, str):
            result = LLMResult(
                success=False,
                content="",
                error="Ollama returned an unexpected assistant content format.",
            )
            self._log_result(operation, system_prompt, user_prompt, result, started_at)
            return result

        content = generated_text.strip()
        if not content:
            result = LLMResult(
                success=False,
                content="",
                error="Ollama returned empty assistant content.",
            )
            self._log_result(operation, system_prompt, user_prompt, result, started_at)
            return result

        result = LLMResult(success=True, content=content)
        self._log_result(operation, system_prompt, user_prompt, result, started_at)
        return result

    def _log_result(
        self,
        operation: str,
        system_prompt: str,
        user_prompt: str,
        result: LLMResult,
        started_at: float,
    ) -> None:
        """Write one structured debug record without affecting the LLM result."""
        record = {
            "timestamp": datetime.now().astimezone().isoformat(),
            "operation": operation,
            "model": self._model,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "success": result.success,
            "response": result.content if result.success else None,
            "error": result.error,
            "latency_ms": round((time.perf_counter() - started_at) * 1000, 2),
        }
        self._logger.debug(json.dumps(record, ensure_ascii=False, indent=2))
