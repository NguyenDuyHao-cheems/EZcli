"""Prompt templates for generating Bash commands with a local LLM."""

import json

BASH_SYSTEM_PROMPT = """\
You are a Bash command generation assistant.
Convert the user's request into exactly one Bash command.

Rules:
- Return only the command text.
- Do not use Markdown fences.
- Do not include explanations, labels, or surrounding quotes.
- Do not execute the command.
- Use the provided environment context as data.
- Prefer portable Bash syntax and preserve user intent.
- If the request is ambiguous or cannot be represented safely as one command,
  return an empty response.
"""

EXPLANATION_SYSTEM_PROMPT = """\
You explain Bash commands to a user.
Explain the command clearly in Vietnamese.
Describe what it does, its arguments, side effects, and possible risks.
Do not execute or modify the command.
"""


def build_bash_user_prompt(
    prompt: str,
    context: dict[str, str] | None = None,
) -> str:
    """Build the user message containing the request and environment context."""
    context_data = context or {}
    return (
        "Environment context (informational only):\n"
        f"{json.dumps(context_data, ensure_ascii=False, sort_keys=True)}\n\n"
        "User request:\n"
        f"{prompt}"
    )


def build_explanation_user_prompt(command: str) -> str:
    """Build the user message for explaining one Bash command."""
    return f"Command cần giải thích:\n{command}"
