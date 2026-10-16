"""Tests for the Ollama chat client."""

import json
from http.client import HTTPResponse
from typing import Any
from unittest.mock import MagicMock, patch
from urllib.error import URLError

from ezcli.llm import LLMResult, MockLLMProvider, OllamaClient


def mock_response(payload: dict[str, Any]) -> MagicMock:
    """Build a mock HTTP response containing JSON."""
    response = MagicMock(spec=HTTPResponse)
    response.__enter__.return_value = response
    response.read.return_value = json.dumps(payload).encode("utf-8")
    return response


def test_generate_success() -> None:
    client = OllamaClient()
    response = mock_response({"message": {"role": "assistant", "content": "ls -la"}})

    with patch("ezcli.llm.urlopen", return_value=response) as mocked_urlopen:
        result = client.generate("list files")

    assert result == LLMResult(success=True, content="ls -la")
    request = mocked_urlopen.call_args.args[0]
    assert request.full_url.endswith("/api/chat")


def test_generate_sends_chat_messages_and_context() -> None:

    client = OllamaClient()
    response = mock_response({"message": {"role": "assistant", "content": "pwd"}})

    with patch("ezcli.llm.urlopen", return_value=response) as mocked_urlopen:
        client.generate(
            "show current directory",
            context={"current_directory": "/tmp"},
        )

    request = mocked_urlopen.call_args.args[0]
    payload = json.loads(request.data.decode("utf-8"))

    assert request.full_url.endswith("/api/chat")
    assert payload["model"] == "qwen2.5-coder:3b"
    assert payload["stream"] is False
    assert payload["messages"][0]["role"] == "system"
    assert "/tmp" in payload["messages"][1]["content"]


def test_generate_uses_configured_timeout() -> None:
    client = OllamaClient(timeout=12.5)
    response = mock_response({"message": {"role": "assistant", "content": "pwd"}})

    with patch("ezcli.llm.urlopen", return_value=response) as mocked_urlopen:
        client.generate("show current directory")

    assert mocked_urlopen.call_args.kwargs["timeout"] == 12.5


def test_generate_uses_thirty_second_default_timeout() -> None:
    client = OllamaClient()
    response = mock_response({"message": {"role": "assistant", "content": "pwd"}})

    with patch("ezcli.llm.urlopen", return_value=response) as mocked_urlopen:
        client.generate("show current directory")

    assert mocked_urlopen.call_args.kwargs["timeout"] == 30.0


def test_empty_prompt_is_rejected() -> None:
    client = OllamaClient()

    try:
        client.generate("   ")
    except ValueError as exc:
        assert str(exc) == "Prompt must not be empty."
    else:
        raise AssertionError("Expected empty prompt to be rejected")


def test_connection_error_returns_failure_result() -> None:
    client = OllamaClient()

    with patch(
        "ezcli.llm.urlopen",
        side_effect=URLError("connection failed"),
    ):
        result = client.generate("list files")

    assert result.success is False
    assert result.content == ""
    assert result.error == "Could not connect to Ollama. Check that Ollama is running."


def test_timeout_returns_failure_result() -> None:
    client = OllamaClient(timeout=7.0)

    with patch("ezcli.llm.urlopen", side_effect=TimeoutError()):
        result = client.generate("list files")

    assert result == LLMResult(
        success=False,
        content="",
        error="Ollama request timed out after 7 seconds.",
    )


def test_empty_response_returns_failure_result() -> None:
    client = OllamaClient()
    response = mock_response({"message": {"content": "  "}})

    with patch("ezcli.llm.urlopen", return_value=response):
        result = client.generate("list files")

    assert result.success is False
    assert result.error == "Ollama returned empty assistant content."


def test_invalid_json_returns_failure_result() -> None:
    client = OllamaClient()
    response = MagicMock(spec=HTTPResponse)
    response.__enter__.return_value = response
    response.read.return_value = b"not valid json"

    with patch("ezcli.llm.urlopen", return_value=response):
        result = client.generate("list files")

    assert result == LLMResult(
        success=False,
        content="",
        error="Ollama returned an invalid response.",
    )


# --- MockLLMProvider Tests ---


def test_mock_success_flow() -> None:
    """Kiểm tra luồng sinh nội dung thành công với Mock theo chuẩn contract."""
    provider = MockLLMProvider()
    result: LLMResult = provider.generate_command("find json files", context={})

    assert result.success is True
    assert result.content is not None
    assert "find" in result.content
    assert result.error is None


def test_mock_error_handling() -> None:
    """Kiểm tra Mock trả về lỗi rõ ràng trong LLMResult theo chuẩn contract."""
    provider = MockLLMProvider()
    result: LLMResult = provider.generate_command("trigger error", context={})

    assert result.success is False
    assert result.error is not None
    assert result.content == ""
