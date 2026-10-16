"""Unit tests for LLMResult — validate invariants for success and failure states."""

from dataclasses import FrozenInstanceError

import pytest

from ezcli.llm.result import LLMResult

# ---------------------------------------------------------------------------
# Success state
# ---------------------------------------------------------------------------


def test_success_result_stores_content() -> None:
    """A successful result has content and no error."""
    result = LLMResult(success=True, content="ls -la")

    assert result.success is True
    assert result.content == "ls -la"
    assert result.error is None


def test_success_result_allows_empty_content() -> None:
    """success=True with an empty string content is valid by the model."""
    result = LLMResult(success=True, content="")

    assert result.success is True
    assert result.error is None


def test_success_result_is_frozen() -> None:
    """LLMResult is immutable (frozen dataclass)."""
    result = LLMResult(success=True, content="echo hi")

    with pytest.raises(FrozenInstanceError):
        result.content = "modified"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Invariant: success=True must not carry an error
# ---------------------------------------------------------------------------


def test_success_true_with_error_raises() -> None:
    """success=True combined with a non-None error must be rejected."""
    with pytest.raises(ValueError, match="error must be None"):
        LLMResult(success=True, content="ls", error="some error")


# ---------------------------------------------------------------------------
# Failure state
# ---------------------------------------------------------------------------


def test_failure_result_stores_error() -> None:
    """A failed result has an error message and empty content."""
    result = LLMResult(success=False, content="", error="Connection refused")

    assert result.success is False
    assert result.content == ""
    assert result.error == "Connection refused"


def test_failure_result_requires_non_empty_error() -> None:
    """success=False without an error message must be rejected."""
    with pytest.raises(ValueError, match="error must contain an error message"):
        LLMResult(success=False, content="", error=None)


def test_failure_result_requires_empty_content() -> None:
    """success=False with non-empty content must be rejected."""
    with pytest.raises(ValueError, match="content must be an empty string"):
        LLMResult(success=False, content="some output", error="oops")


def test_failure_empty_error_string_raises() -> None:
    """An empty string error is treated as missing and must be rejected."""
    with pytest.raises(ValueError, match="error must contain an error message"):
        LLMResult(success=False, content="", error="")


# ---------------------------------------------------------------------------
# Equality and hashing (frozen dataclass)
# ---------------------------------------------------------------------------


def test_equal_results_compare_equal() -> None:
    """Two LLMResult instances with identical fields must be equal."""
    a = LLMResult(success=True, content="echo hello")
    b = LLMResult(success=True, content="echo hello")

    assert a == b


def test_different_results_compare_unequal() -> None:
    """Results with different content must not be equal."""
    a = LLMResult(success=True, content="ls")
    b = LLMResult(success=True, content="pwd")

    assert a != b


def test_frozen_result_is_hashable() -> None:
    """A frozen dataclass must be usable as a dict key or set member."""
    result = LLMResult(success=True, content="ls -la")
    result_set = {result}

    assert result in result_set
