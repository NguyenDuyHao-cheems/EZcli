"""Contract and specification tests for the LLM client interface."""

import pytest

from ezcli.llm import LLMClient as PublicLLMClient
from ezcli.llm import LLMResult as PublicLLMResult
from ezcli.llm.client import LLMClient
from ezcli.llm.result import LLMResult


class FakeLLMClient:
    """Simple client used to verify interface conformance."""

    def generate(self, prompt: str) -> LLMResult:
        return LLMResult(
            success=True,
            content=f"Response to: {prompt}",
        )


class MockLLMClient:
    """Provide deterministic responses for tests."""

    def __init__(self, result: LLMResult) -> None:
        self._result = result
        self.last_prompt: str | None = None

    def generate(self, prompt: str) -> LLMResult:
        self.last_prompt = prompt
        return self._result


def test_public_module_exports() -> None:
    """LLMClient and LLMResult can be imported from the public ezcli.llm module."""
    assert PublicLLMClient is LLMClient
    assert PublicLLMResult is LLMResult


def test_client_satisfies_contract() -> None:
    client: LLMClient = FakeLLMClient()

    result = client.generate("Hello")

    assert result.success is True
    assert result.content == "Response to: Hello"
    assert result.error is None


def test_failed_result_has_error() -> None:
    result = LLMResult(
        success=False,
        content="",
        error="Connection failed.",
    )

    assert result.success is False
    assert result.content == ""
    assert result.error is not None


def test_successful_result_has_no_error() -> None:
    result = LLMResult(
        success=True,
        content="Hello",
    )

    assert result.success is True
    assert result.error is None


def test_mock_client_satisfies_contract_and_records_prompt() -> None:
    expected_result = LLMResult(
        success=True,
        content="Dependency injection is a design technique.",
    )
    mock: LLMClient = MockLLMClient(expected_result)

    result = mock.generate("Explain dependency injection.")

    assert result == expected_result
    assert getattr(mock, "last_prompt") == "Explain dependency injection."


def test_invariant_success_with_error_raises_error() -> None:
    with pytest.raises(ValueError, match="When success is True, error must be None."):
        LLMResult(
            success=True,
            content="Some output",
            error="Unexpected error",
        )


def test_invariant_failure_without_error_raises_error() -> None:
    with pytest.raises(
        ValueError,
        match="When success is False, error must contain an error message.",
    ):
        LLMResult(
            success=False,
            content="",
            error=None,
        )


def test_invariant_failure_with_content_raises_error() -> None:
    with pytest.raises(
        ValueError,
        match="When success is False, content must be an empty string.",
    ):
        LLMResult(
            success=False,
            content="Unexpected content",
            error="Something went wrong.",
        )
