"""Contract and specification tests for the LLM client interface."""

from ezcli.llm import LLMClient as PublicLLMClient
from ezcli.llm import LLMResult as PublicLLMResult
from ezcli.llm.client import LLMClient
from ezcli.llm.result import LLMResult


class FakeLLMClient:
    """Simple client used to verify interface conformance."""

    def generate(
        self,
        prompt: str,
        context: dict[str, str] | None = None,
    ) -> LLMResult:
        return LLMResult(success=True, content="ls -la")


class MockLLMClient:
    """Provide deterministic responses for tests."""

    def __init__(self, result: LLMResult) -> None:
        self._result = result
        self.last_prompt: str | None = None
        self.last_context: dict[str, str] | None = None

    def generate(
        self,
        prompt: str,
        context: dict[str, str] | None = None,
    ) -> LLMResult:
        self.last_prompt = prompt
        self.last_context = context
        return self._result


def test_public_module_exports() -> None:
    """The public module exports the result model and client protocol."""
    assert PublicLLMResult is LLMResult
    assert PublicLLMClient is LLMClient


def test_client_satisfies_contract() -> None:
    client: LLMClient = FakeLLMClient()

    result = client.generate("list files", {"current_directory": "/tmp"})

    assert result == LLMResult(success=True, content="ls -la")


def test_mock_client_satisfies_contract_and_records_request() -> None:
    expected_result = LLMResult(success=True, content="echo explanation")
    mock: LLMClient = MockLLMClient(expected_result)
    context = {"shell": "bash"}

    result = mock.generate("Explain dependency injection.", context)

    assert result == expected_result
    assert isinstance(mock, MockLLMClient)
    assert mock.last_prompt == "Explain dependency injection."
    assert mock.last_context == context
