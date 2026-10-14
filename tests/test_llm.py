"""Tests for the Ollama client."""

import json
from http.client import HTTPResponse
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from ezcli.domain.models import GeneratedCommand
from ezcli.llm import LLMError, OllamaClient


def mock_response(payload: dict[str, Any]) -> MagicMock:
    """Build a mock HTTP response containing JSON."""
    response = MagicMock(spec=HTTPResponse)
    response.__enter__.return_value = response
    response.read.return_value = json.dumps(payload).encode("utf-8")
    return response


def test_generate_success() -> None:
    client = OllamaClient()
    response = mock_response({"response": "ls -la"})

    with patch("ezcli.llm.urlopen", return_value=response) as mocked_urlopen:
        result = client.generate("list files")

    assert result == GeneratedCommand(prompt="list files", command="ls -la")
    mocked_urlopen.assert_called_once()


def test_generate_sends_context() -> None:
    client = OllamaClient()
    response = mock_response({"response": "pwd"})

    with patch("ezcli.llm.urlopen", return_value=response) as mocked_urlopen:
        client.generate(
            "show current directory",
            context={"current_directory": "/tmp"},
        )

    request = mocked_urlopen.call_args.args[0]
    payload = json.loads(request.data.decode("utf-8"))

    assert payload["model"] == "qwen2.5-coder:3b"
    assert payload["stream"] is False
    assert "/tmp" in payload["prompt"]


def test_empty_prompt_is_rejected() -> None:
    client = OllamaClient()

    with pytest.raises(ValueError, match="Prompt must not be empty"):
        client.generate("   ")


def test_connection_error_raises_llm_error() -> None:
    client = OllamaClient()

    with patch(
        "ezcli.llm.urlopen",
        side_effect=OSError("connection failed"),
    ):
        with pytest.raises(LLMError, match="Could not connect"):
            client.generate("list files")


def test_empty_response_raises_llm_error() -> None:
    client = OllamaClient()
    response = mock_response({"response": "  "})

    with patch("ezcli.llm.urlopen", return_value=response):
        with pytest.raises(LLMError, match="empty command"):
            client.generate("list files")


def test_invalid_json_raises_llm_error() -> None:
    client = OllamaClient()
    response = MagicMock(spec=HTTPResponse)
    response.__enter__.return_value = response
    response.read.return_value = b"not valid json"

    with patch("ezcli.llm.urlopen", return_value=response):
        with pytest.raises(LLMError, match="invalid response"):
            client.generate("list files")
