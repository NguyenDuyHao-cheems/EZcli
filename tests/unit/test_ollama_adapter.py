"""Mock-based unit tests for the OllamaClient (Ollama HTTP chat adapter).

All tests run entirely offline — no real Ollama process is required.
``urlopen`` is patched at the ``ezcli.llm`` import path so that the adapter
picks up the mock without touching any network socket.
"""

from __future__ import annotations

import json
from typing import Any
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError

import pytest

from ezcli.llm import LLMResult, OllamaClient

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_response(payload: dict[str, Any], status: int = 200) -> MagicMock:
    """Return a context-manager mock that yields a file-like HTTP response."""
    body = json.dumps(payload).encode("utf-8")
    mock_resp = MagicMock()
    mock_resp.read.return_value = body
    mock_resp.status = status

    cm = MagicMock()
    cm.__enter__ = MagicMock(return_value=mock_resp)
    cm.__exit__ = MagicMock(return_value=False)
    return cm


_PATCH_TARGET = "ezcli.llm.urlopen"


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------


def test_generate_returns_llm_result_on_success() -> None:
    """OllamaClient.generate parses a valid Ollama chat response into LLMResult."""
    payload = {"message": {"role": "assistant", "content": "ls -la"}}

    with patch(_PATCH_TARGET, return_value=_make_response(payload)) as mock_open:
        client = OllamaClient()
        result = client.generate("list files")

    assert result == LLMResult(success=True, content="ls -la")
    mock_open.assert_called_once()
    req = mock_open.call_args[0][0]
    assert req.full_url.endswith("/api/chat")


def test_generate_strips_whitespace_from_response() -> None:
    """Trailing/leading whitespace in the model response is stripped."""
    payload = {"message": {"role": "assistant", "content": "  echo hello  \n"}}

    with patch(_PATCH_TARGET, return_value=_make_response(payload)):
        client = OllamaClient()
        result = client.generate("greet")

    assert result == LLMResult(success=True, content="echo hello")


def test_generate_passes_context_and_messages_in_body() -> None:
    """The shell context and prompt are structured into chat messages."""
    payload = {"message": {"role": "assistant", "content": "pwd"}}
    context = {"shell": "bash", "cwd": "/home/user"}

    with patch(_PATCH_TARGET, return_value=_make_response(payload)) as mock_open:
        client = OllamaClient()
        client.generate("print working directory", context=context)

    call_args = mock_open.call_args
    request_obj = call_args[0][0]
    sent_body = json.loads(request_obj.data.decode("utf-8"))
    assert sent_body["model"] == "qwen2.5-coder:3b"
    assert sent_body["stream"] is False
    messages = sent_body["messages"]
    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert "bash" in messages[1]["content"]
    assert "/home/user" in messages[1]["content"]


def test_generate_uses_custom_model_and_base_url() -> None:
    """Custom model name and base URL are reflected in the outgoing request."""
    payload = {"message": {"role": "assistant", "content": "cat /etc/hosts"}}

    with patch(_PATCH_TARGET, return_value=_make_response(payload)) as mock_open:
        client = OllamaClient(
            model="llama3:8b",
            base_url="http://192.168.1.50:11434",
        )
        client.generate("show hosts file")

    request_obj = mock_open.call_args[0][0]
    assert "192.168.1.50:11434/api/chat" in request_obj.full_url
    body = json.loads(request_obj.data.decode("utf-8"))
    assert body["model"] == "llama3:8b"


# ---------------------------------------------------------------------------
# Empty prompt validation (no network call needed)
# ---------------------------------------------------------------------------


def test_generate_raises_value_error_for_empty_prompt() -> None:
    """An empty or whitespace-only prompt must raise ValueError before any I/O."""
    client = OllamaClient()

    with pytest.raises(ValueError, match="Prompt must not be empty"):
        client.generate("   ")


def test_generate_raises_value_error_for_blank_prompt() -> None:
    """A completely empty prompt string also raises ValueError."""
    client = OllamaClient()

    with pytest.raises(ValueError, match="Prompt must not be empty"):
        client.generate("")


# ---------------------------------------------------------------------------
# HTTP error responses
# ---------------------------------------------------------------------------


def test_generate_returns_failure_on_http_404() -> None:
    """An HTTP 404 from Ollama is returned as a failure LLMResult."""
    http_error = HTTPError(
        url="http://localhost:11434/api/chat",
        code=404,
        msg="Not Found",
        hdrs=MagicMock(),
        fp=None,
    )

    with patch(_PATCH_TARGET, side_effect=http_error):
        client = OllamaClient()
        result = client.generate("list files")

    assert result.success is False
    assert result.content == ""
    assert "404" in str(result.error)


def test_generate_returns_failure_on_http_500() -> None:
    """An HTTP 500 from Ollama is returned as a failure LLMResult."""
    http_error = HTTPError(
        url="http://localhost:11434/api/chat",
        code=500,
        msg="Internal Server Error",
        hdrs=MagicMock(),
        fp=None,
    )

    with patch(_PATCH_TARGET, side_effect=http_error):
        client = OllamaClient()
        result = client.generate("crash the server")

    assert result.success is False
    assert result.content == ""
    assert "500" in str(result.error)


# ---------------------------------------------------------------------------
# Network / connectivity errors
# ---------------------------------------------------------------------------


def test_generate_returns_failure_when_ollama_not_running() -> None:
    """A URLError maps to failure LLMResult with a helpful message."""
    with patch(_PATCH_TARGET, side_effect=URLError("Connection refused")):
        client = OllamaClient()
        result = client.generate("list files")

    assert result.success is False
    assert result.content == ""
    assert "Could not connect to Ollama" in str(result.error)


def test_generate_returns_failure_on_os_error() -> None:
    """An OSError maps to failure LLMResult."""
    with patch(_PATCH_TARGET, side_effect=OSError("Broken pipe")):
        client = OllamaClient()
        result = client.generate("list files")

    assert result.success is False
    assert "Could not connect to Ollama" in str(result.error)


def test_generate_returns_failure_on_timeout() -> None:
    """A TimeoutError maps to failure LLMResult with timeout info."""
    with patch(_PATCH_TARGET, side_effect=TimeoutError()):
        client = OllamaClient(timeout=10.0)
        result = client.generate("list files")

    assert result == LLMResult(
        success=False,
        content="",
        error="Ollama request timed out after 10 seconds.",
    )


# ---------------------------------------------------------------------------
# Malformed / unexpected responses
# ---------------------------------------------------------------------------


def test_generate_returns_failure_on_invalid_json() -> None:
    """Non-JSON body from Ollama is mapped to failure LLMResult."""
    mock_resp = MagicMock()
    mock_resp.read.return_value = b"not-json-at-all"
    cm = MagicMock()
    cm.__enter__ = MagicMock(return_value=mock_resp)
    cm.__exit__ = MagicMock(return_value=False)

    with patch(_PATCH_TARGET, return_value=cm):
        client = OllamaClient()
        result = client.generate("list files")

    assert result.success is False
    assert result.error == "Ollama returned an invalid response."


def test_generate_returns_failure_when_message_key_missing() -> None:
    """A JSON body without the 'message' key returns failure LLMResult."""
    payload = {"model": "qwen2.5-coder:3b", "done": True}

    with patch(_PATCH_TARGET, return_value=_make_response(payload)):
        client = OllamaClient()
        result = client.generate("list files")

    assert result.success is False
    assert "unexpected response format" in str(result.error)


def test_generate_returns_failure_when_content_is_whitespace_only() -> None:
    """A response consisting only of whitespace is treated as empty."""
    payload = {"message": {"content": "   \n\t  "}}

    with patch(_PATCH_TARGET, return_value=_make_response(payload)):
        client = OllamaClient()
        result = client.generate("list files")

    assert result.success is False
    assert result.error == "Ollama returned empty assistant content."


def test_generate_returns_failure_when_body_is_not_a_dict() -> None:
    """A top-level JSON array raises unexpected format error."""
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps([1, 2, 3]).encode("utf-8")
    cm = MagicMock()
    cm.__enter__ = MagicMock(return_value=mock_resp)
    cm.__exit__ = MagicMock(return_value=False)

    with patch(_PATCH_TARGET, return_value=cm):
        client = OllamaClient()
        result = client.generate("list files")

    assert result.success is False
    assert "unexpected response format" in str(result.error)


# ---------------------------------------------------------------------------
# Timeout configuration is forwarded to urlopen
# ---------------------------------------------------------------------------


def test_generate_passes_timeout_to_urlopen() -> None:
    """The configured timeout value is forwarded to urlopen."""
    payload = {"message": {"role": "assistant", "content": "echo ok"}}

    with patch(_PATCH_TARGET, return_value=_make_response(payload)) as mock_open:
        client = OllamaClient(timeout=5.0)
        client.generate("run something")

    _, kwargs = mock_open.call_args
    assert kwargs.get("timeout") == 5.0
