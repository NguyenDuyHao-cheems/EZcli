"""Mock-based unit tests for the OllamaClient (Ollama HTTP adapter).

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

from ezcli.domain.models import GeneratedCommand
from ezcli.llm import LLMError, OllamaClient

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


def test_generate_returns_generated_command_on_success() -> None:
    """OllamaClient.generate parses a valid Ollama response into GeneratedCommand."""
    payload = {"response": "ls -la"}

    with patch(_PATCH_TARGET, return_value=_make_response(payload)) as mock_open:
        client = OllamaClient()
        result = client.generate("list files")

    assert isinstance(result, GeneratedCommand)
    assert result.command == "ls -la"
    assert result.prompt == "list files"
    mock_open.assert_called_once()


def test_generate_strips_whitespace_from_response() -> None:
    """Trailing/leading whitespace in the model response is stripped."""
    payload = {"response": "  echo hello  \n"}

    with patch(_PATCH_TARGET, return_value=_make_response(payload)):
        client = OllamaClient()
        result = client.generate("greet")

    assert result.command == "echo hello"


def test_generate_passes_context_in_request_body() -> None:
    """The shell context dict is serialised into the request prompt."""
    payload = {"response": "pwd"}
    context = {"shell": "bash", "cwd": "/home/user"}

    with patch(_PATCH_TARGET, return_value=_make_response(payload)) as mock_open:
        client = OllamaClient()
        client.generate("print working directory", context=context)

    call_args = mock_open.call_args
    request_obj = call_args[0][0]  # first positional arg = urllib.request.Request
    sent_body = json.loads(request_obj.data.decode("utf-8"))
    assert sent_body["model"] == "qwen2.5-coder:3b"
    assert "bash" in sent_body["prompt"]
    assert "/home/user" in sent_body["prompt"]


def test_generate_uses_custom_model_and_base_url() -> None:
    """Custom model name and base URL are reflected in the outgoing request."""
    payload = {"response": "cat /etc/hosts"}

    with patch(_PATCH_TARGET, return_value=_make_response(payload)) as mock_open:
        client = OllamaClient(
            model="llama3:8b",
            base_url="http://192.168.1.50:11434",
        )
        client.generate("show hosts file")

    request_obj = mock_open.call_args[0][0]
    assert "192.168.1.50:11434" in request_obj.full_url
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


def test_generate_raises_llm_error_on_http_404() -> None:
    """An HTTP 404 from Ollama is converted to LLMError."""
    http_error = HTTPError(
        url="http://localhost:11434/api/generate",
        code=404,
        msg="Not Found",
        hdrs=MagicMock(),
        fp=None,
    )

    with patch(_PATCH_TARGET, side_effect=http_error):
        client = OllamaClient()
        with pytest.raises(LLMError, match="HTTP error 404"):
            client.generate("list files")


def test_generate_raises_llm_error_on_http_500() -> None:
    """An HTTP 500 from Ollama is converted to LLMError."""
    http_error = HTTPError(
        url="http://localhost:11434/api/generate",
        code=500,
        msg="Internal Server Error",
        hdrs=MagicMock(),
        fp=None,
    )

    with patch(_PATCH_TARGET, side_effect=http_error):
        client = OllamaClient()
        with pytest.raises(LLMError, match="HTTP error 500"):
            client.generate("crash the server")


# ---------------------------------------------------------------------------
# Network / connectivity errors
# ---------------------------------------------------------------------------


def test_generate_raises_llm_error_when_ollama_not_running() -> None:
    """A URLError (Ollama not started) maps to LLMError with a helpful message."""
    with patch(_PATCH_TARGET, side_effect=URLError("Connection refused")):
        client = OllamaClient()
        with pytest.raises(LLMError, match="Could not connect to Ollama"):
            client.generate("list files")


def test_generate_raises_llm_error_on_os_error() -> None:
    """Any OSError (e.g. broken pipe) is also caught and mapped to LLMError."""
    with patch(_PATCH_TARGET, side_effect=OSError("Broken pipe")):
        client = OllamaClient()
        with pytest.raises(LLMError, match="Could not connect to Ollama"):
            client.generate("list files")


def test_generate_raises_llm_error_on_timeout() -> None:
    """A TimeoutError (slow Ollama) maps to LLMError."""
    with patch(_PATCH_TARGET, side_effect=TimeoutError("timed out")):
        client = OllamaClient()
        with pytest.raises(LLMError, match="Could not connect to Ollama"):
            client.generate("list files")


# ---------------------------------------------------------------------------
# Malformed / unexpected responses
# ---------------------------------------------------------------------------


def test_generate_raises_llm_error_on_invalid_json() -> None:
    """Non-JSON body from Ollama is mapped to LLMError."""
    mock_resp = MagicMock()
    mock_resp.read.return_value = b"not-json-at-all"
    cm = MagicMock()
    cm.__enter__ = MagicMock(return_value=mock_resp)
    cm.__exit__ = MagicMock(return_value=False)

    with patch(_PATCH_TARGET, return_value=cm):
        client = OllamaClient()
        with pytest.raises(LLMError, match="invalid response"):
            client.generate("list files")


def test_generate_raises_llm_error_when_response_key_missing() -> None:
    """A JSON body without the 'response' key maps to LLMError."""
    payload = {"model": "qwen2.5-coder:3b", "done": True}  # no 'response' key

    with patch(_PATCH_TARGET, return_value=_make_response(payload)):
        client = OllamaClient()
        with pytest.raises(LLMError, match="empty command"):
            client.generate("list files")


def test_generate_raises_llm_error_when_response_is_whitespace_only() -> None:
    """A response consisting only of whitespace is treated as empty."""
    payload = {"response": "   \n\t  "}

    with patch(_PATCH_TARGET, return_value=_make_response(payload)):
        client = OllamaClient()
        with pytest.raises(LLMError, match="empty command"):
            client.generate("list files")


def test_generate_raises_llm_error_when_body_is_not_a_dict() -> None:
    """A top-level JSON array (unexpected format) raises LLMError."""
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps([1, 2, 3]).encode("utf-8")
    cm = MagicMock()
    cm.__enter__ = MagicMock(return_value=mock_resp)
    cm.__exit__ = MagicMock(return_value=False)

    with patch(_PATCH_TARGET, return_value=cm):
        client = OllamaClient()
        with pytest.raises(LLMError, match="unexpected response format"):
            client.generate("list files")


# ---------------------------------------------------------------------------
# Timeout configuration is forwarded to urlopen
# ---------------------------------------------------------------------------


def test_generate_passes_timeout_to_urlopen() -> None:
    """The configured timeout value is forwarded to urlopen."""
    payload = {"response": "echo ok"}

    with patch(_PATCH_TARGET, return_value=_make_response(payload)) as mock_open:
        client = OllamaClient(timeout=5.0)
        client.generate("run something")

    _, kwargs = mock_open.call_args
    assert kwargs.get("timeout") == 5.0
