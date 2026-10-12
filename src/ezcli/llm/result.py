"""Standardized result representation for LLM generation."""

from dataclasses import dataclass


@dataclass(frozen=True)
class LLMResult:
    """Represent the outcome of an LLM generation request."""

    success: bool
    content: str
    error: str | None = None

    def __post_init__(self) -> None:
        """Validate invariant rules for success and failure states."""
        if self.success:
            if self.error is not None:
                raise ValueError("When success is True, error must be None.")
        else:
            if not self.error:
                raise ValueError(
                    "When success is False, error must contain an error message."
                )
            if self.content != "":
                raise ValueError(
                    "When success is False, content must be an empty string."
                )
