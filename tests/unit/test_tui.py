"""Unit tests for the EZcliApp TUI flow and ConfirmScreen modal.

All tests run offline without launching a real terminal. The tests verify
initial states, user interactions (generate, execute, cancel), safety level
handling, and confirmation modal behavior.
"""

from __future__ import annotations

import asyncio
from unittest.mock import MagicMock, patch

from textual.widgets import Input, Static, TextArea

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


def test_initial_state_shows_keyboard_actions() -> None:
    """When the TUI starts, the keyboard action hint is visible."""

    async def _test() -> None:
        app = EZcliApp()
        async with app.run_test():
            actions = app.query_one("#actions", Static)
            action_text = str(actions.content).lower()
            assert "xecute" in action_text
            assert "odify" in action_text
            assert "escribe" in action_text
            assert "bort" in action_text

    asyncio.run(_test())


def test_initial_state_result_placeholder() -> None:
    """When the TUI starts, the result widget displays initial placeholder text."""

    async def _test() -> None:
        app = EZcliApp()
        async with app.run_test():
            result_widget = app.query_one("#result", TextArea)
            assert result_widget is not None

    asyncio.run(_test())


def test_empty_prompt_does_not_generate() -> None:
    """Submitting an empty prompt does not create a prepared command."""

    async def _test() -> None:
        app = EZcliApp()
        async with app.run_test():
            app.on_input_submitted(Input.Submitted(Input(), ""))
            assert app._prepared is None

    asyncio.run(_test())


def test_abort_action_resets_prepared_command() -> None:
    """Pressing Abort resets the prepared command and enables prompt input."""

    async def _test() -> None:
        app = EZcliApp()
        async with app.run_test():
            app._prepared = _make_prepared()
            app.query_one("#prompt").disabled = True
            app.action_abort_action()

            assert app._prepared is None
            assert app.query_one("#prompt").disabled is False
            result_text = app.query_one("#result", TextArea).text
            assert "hủy" in result_text.lower()

    asyncio.run(_test())


# ---------------------------------------------------------------------------
# Direct method tests for EZcliApp logic
# ---------------------------------------------------------------------------


def test_show_result_disables_prompt_for_safe_command() -> None:
    """Displaying a safe prepared command disables prompt input."""

    async def _test() -> None:
        app = EZcliApp()
        async with app.run_test():
            prepared = _make_prepared(command="ls -la", level=SafetyLevel.SAFE)
            app._show_result(prepared)

            assert app._prepared is prepared
            assert app.query_one("#prompt").disabled is True
            result_text = app.query_one("#result", TextArea).text
            assert "ls -la" in result_text

    asyncio.run(_test())


def test_show_result_displays_blocked_command() -> None:
    """Displaying a BLOCKED command still shows the generated command."""

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
            assert app.query_one("#prompt").disabled is True
            result_text = app.query_one("#result", TextArea).text
            assert "rm -rf /" in result_text

    asyncio.run(_test())


def test_handle_generation_error_updates_result_area() -> None:
    """_handle_generation displays error message in result widget on failure."""

    async def _test() -> None:
        app = EZcliApp()
        async with app.run_test():
            with patch.object(
                app.service,
                "prepare_command",
                side_effect=RuntimeError("Ollama is not running"),
            ):
                app._handle_generation("trigger error")
            result_text = app.query_one("#result", TextArea).text.lower()
            assert "lỗi" in result_text or "error" in result_text

    asyncio.run(_test())


def test_describe_action_requests_explanation_in_background() -> None:
    """Pressing D requests an explanation without blocking the TUI."""

    async def _test() -> None:
        app = EZcliApp()
        async with app.run_test() as pilot:
            app._prepared = _make_prepared(command="mkdir demo")
            with patch.object(
                app.service,
                "explain_command",
                return_value="Creates the demo directory.",
            ) as explain:
                app.action_describe_action()
                await pilot.pause(1)

            explain.assert_called_once_with("mkdir demo")
            result_text = app.query_one("#result", TextArea).text
            assert "Creates the demo directory." in result_text

    asyncio.run(_test())


def test_on_confirmation_cancelled_updates_message() -> None:
    """When user cancels on the confirmation screen, execution is aborted."""

    async def _test() -> None:
        app = EZcliApp()
        async with app.run_test():
            app._prepared = None
            app._last_prompt = ""
            app._on_confirmation(confirmed=False)

            result_text = app.query_one("#result", TextArea).text
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


# ---------------------------------------------------------------------------
# /plugin slash command TUI tests
# ---------------------------------------------------------------------------


def test_tui_plugin_list_displays_plugin_catalog() -> None:
    """Submitting /plugin displays plugin catalog and keeps execute disabled."""

    async def _test() -> None:
        app = EZcliApp()
        async with app.run_test():
            app._handle_generation("/plugin")
            result_text = app.query_one("#result", TextArea).text

            assert "QUẢN LÝ PLUGINS" in result_text
            assert "tldr" in result_text
            assert app.query_one("#execute").disabled is True
            assert app._prepared is None

    asyncio.run(_test())


def test_tui_plugin_install_prepares_command_when_not_installed() -> None:
    """Submitting /plugin install <name> prepares command and enables execute."""

    async def _test() -> None:
        app = EZcliApp()
        async with app.run_test():
            with patch("ezcli.plugins.shutil.which", return_value=None):
                app._handle_generation("/plugin install tldr")

            result_text = app.query_one("#result", TextArea).text
            assert "Chuẩn bị cài đặt" in result_text
            assert app._prepared is not None
            assert app._prepared.generated.command == "pip install tldr"
            assert app.query_one("#execute").disabled is False

    asyncio.run(_test())


def test_tui_plugin_install_notifies_when_already_installed() -> None:
    """Submitting /plugin install <name> notifies user when already installed."""

    async def _test() -> None:
        app = EZcliApp()
        async with app.run_test():
            with patch("ezcli.plugins.shutil.which", return_value="/usr/bin/tldr"):
                app._handle_generation("/plugin install tldr")

            result_text = app.query_one("#result", TextArea).text
            assert "đã được cài đặt" in result_text
            assert app._prepared is None
            assert app.query_one("#execute").disabled is True

    asyncio.run(_test())
