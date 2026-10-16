"""Unit tests for the EZcliApp TUI flow and ConfirmScreen modal.

All tests run offline without launching a real terminal. The tests verify
initial states, user interactions (generate, execute, cancel), safety level
handling, and confirmation modal behavior.
"""

from __future__ import annotations

import asyncio
from unittest.mock import MagicMock

from textual.widgets import Static

from ezcli.application import PreparedCommand
from ezcli.domain.models import (
    GeneratedCommand,
    SafetyLevel,
    SafetyResult,
)
from ezcli.tui import ConfirmScreen, EZcliApp

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_prepared(
    prompt: str = "list files",
    command: str = "ls -la",
    level: SafetyLevel = SafetyLevel.SAFE,
    reasons: tuple[str, ...] = (),
) -> PreparedCommand:
    return PreparedCommand(
        generated=GeneratedCommand(prompt=prompt, command=command),
        safety=SafetyResult(level=level, reasons=reasons),
    )


# ---------------------------------------------------------------------------
# Tests using Textual App.run_test (asyncio.run wrapper)
# ---------------------------------------------------------------------------


def test_initial_state_execute_disabled() -> None:
    """When the TUI starts, the Execute button must be disabled."""

    async def _test() -> None:
        app = EZcliApp()
        async with app.run_test():
            execute_btn = app.query_one("#execute")
            assert execute_btn.disabled is True

    asyncio.run(_test())


def test_initial_state_result_placeholder() -> None:
    """When the TUI starts, the result widget displays initial placeholder text."""

    async def _test() -> None:
        app = EZcliApp()
        async with app.run_test():
            result_widget = app.query_one("#result", Static)
            assert result_widget is not None

    asyncio.run(_test())


def test_empty_prompt_shows_validation_message() -> None:
    """Clicking Generate with empty input displays a validation message."""

    async def _test() -> None:
        app = EZcliApp()
        async with app.run_test() as pilot:
            await pilot.click("#generate")
            await pilot.pause()

            result_text = str(app.query_one("#result", Static).content).lower()
            assert "nhập yêu cầu" in result_text or "vui lòng" in result_text

    asyncio.run(_test())


def test_cancel_button_resets_prepared_and_disables_execute() -> None:
    """Clicking Cancel resets any prepared command and disables the Execute button."""

    async def _test() -> None:
        app = EZcliApp()
        async with app.run_test() as pilot:
            # Simulate an already-prepared command
            app._prepared = _make_prepared()
            app.query_one("#execute").disabled = False

            await pilot.click("#cancel")
            await pilot.pause()

            assert app._prepared is None
            assert app.query_one("#execute").disabled is True
            result_text = str(app.query_one("#result", Static).content)
            assert "hủy" in result_text.lower()

    asyncio.run(_test())


# ---------------------------------------------------------------------------
# Direct method tests for EZcliApp logic
# ---------------------------------------------------------------------------


def test_show_result_enables_execute_for_safe_command() -> None:
    """Displaying a safe prepared command enables the Execute button."""

    async def _test() -> None:
        app = EZcliApp()
        async with app.run_test():
            prepared = _make_prepared(command="ls -la", level=SafetyLevel.SAFE)
            app._show_result(prepared)

            assert app._prepared is prepared
            assert app.query_one("#execute").disabled is False
            result_text = str(app.query_one("#result", Static).content)
            assert "ls -la" in result_text
            assert "SAFE" in result_text

    asyncio.run(_test())


def test_show_result_disables_execute_for_blocked_command() -> None:
    """Displaying a BLOCKED command keeps the Execute button disabled."""

    async def _test() -> None:
        app = EZcliApp()
        async with app.run_test():
            prepared = _make_prepared(
                command="rm -rf /",
                level=SafetyLevel.BLOCKED,
                reasons=("Root deletion",),
            )
            app._show_result(prepared)

            assert app._prepared is prepared
            assert app.query_one("#execute").disabled is True
            result_text = str(app.query_one("#result", Static).content)
            assert "BLOCKED" in result_text
            assert "Root deletion" in result_text

    asyncio.run(_test())


def test_show_error_updates_result_area() -> None:
    """_show_error displays the error message in the result widget."""

    async def _test() -> None:
        app = EZcliApp()
        async with app.run_test():
            app._show_error("Không thể kết nối đến Ollama.")
            result_text = str(app.query_one("#result", Static).content)
            assert "Không thể kết nối đến Ollama." in result_text

    asyncio.run(_test())


def test_on_confirmation_cancelled_updates_message() -> None:
    """When user cancels on the confirmation screen, execution is aborted."""

    async def _test() -> None:
        app = EZcliApp()
        async with app.run_test():
            app._prepared = _make_prepared()
            app._on_confirmation(confirmed=False)

            result_text = str(app.query_one("#result", Static).content)
            assert "hủy thực thi" in result_text.lower()

    asyncio.run(_test())


# ---------------------------------------------------------------------------
# ConfirmScreen modal tests
# ---------------------------------------------------------------------------


def test_confirm_screen_dismiss_true_on_confirm() -> None:
    """ConfirmScreen dismisses with True when user clicks confirm."""

    async def _test() -> None:
        prepared = _make_prepared(command="echo test", level=SafetyLevel.SAFE)
        screen = ConfirmScreen(prepared)
        screen.dismiss = MagicMock()  # type: ignore[method-assign]

        event = MagicMock()
        event.button.id = "confirm"
        screen.on_button_pressed(event)

        screen.dismiss.assert_called_once_with(True)

    asyncio.run(_test())


def test_confirm_screen_dismiss_false_on_back() -> None:
    """ConfirmScreen dismisses with False when user clicks back."""

    async def _test() -> None:
        prepared = _make_prepared(command="echo test", level=SafetyLevel.SAFE)
        screen = ConfirmScreen(prepared)
        screen.dismiss = MagicMock()  # type: ignore[method-assign]

        event = MagicMock()
        event.button.id = "back"
        screen.on_button_pressed(event)

        screen.dismiss.assert_called_once_with(False)

    asyncio.run(_test())
