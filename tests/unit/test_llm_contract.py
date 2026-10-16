"""Contract and specification tests for the LLM client interface."""

from ezcli.domain.models import GeneratedCommand
from ezcli.llm import GeneratedCommand as PublicGeneratedCommand
from ezcli.llm import LLMClient as PublicLLMClient
from ezcli.llm import LLMError, OllamaClient
from ezcli.llm.client import LLMClient


class FakeLLMClient:
    """Simple client used to verify interface conformance."""

    def generate(
        self,
        prompt: str,
        context: dict[str, str] | None = None,
    ) -> GeneratedCommand:
        return GeneratedCommand(
            prompt=prompt,
            command="ls -la",
        )


class MockLLMClient:
    """Provide deterministic responses for tests."""

    def __init__(self, result: GeneratedCommand) -> None:
        self._result = result
        self.last_prompt: str | None = None
        self.last_context: dict[str, str] | None = None

    def generate(
        self,
        prompt: str,
        context: dict[str, str] | None = None,
    ) -> GeneratedCommand:
        self.last_prompt = prompt
        self.last_context = context
        return self._result


def test_public_module_exports() -> None:
    """The public module exports the command model, client protocol, and adapter."""
    assert PublicGeneratedCommand is GeneratedCommand
    assert PublicLLMClient is LLMClient
    assert issubclass(LLMError, RuntimeError)
    assert callable(OllamaClient)


def test_ollama_client_satisfies_contract() -> None:
    """The production OllamaClient must satisfy the LLMClient protocol."""
    client: LLMClient = OllamaClient()

    assert hasattr(client, "generate")
    assert callable(client.generate)


def test_client_satisfies_contract() -> None:
    client: LLMClient = FakeLLMClient()

    result = client.generate("list files", {"current_directory": "/tmp"})

    assert result == GeneratedCommand(prompt="list files", command="ls -la")


def test_mock_client_satisfies_contract_and_records_request() -> None:
    expected_result = GeneratedCommand(
        prompt="Explain dependency injection.",
        command="echo explanation",
    )
    mock: LLMClient = MockLLMClient(expected_result)
    context = {"shell": "bash"}

    result = mock.generate("Explain dependency injection.", context)

    assert result == expected_result
    assert isinstance(mock, MockLLMClient)
    assert mock.last_prompt == "Explain dependency injection."
    assert mock.last_context == context
