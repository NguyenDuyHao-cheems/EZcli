"""Textual terminal interface for EZcli backed by the Ollama LLM client."""

import sys
from typing import TextIO

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Static

from ezcli.application import CommandService, PreparedCommand
from ezcli.domain.models import SafetyLevel
from ezcli.execution import execute_command
from ezcli.safety import check_command


class EZcliApp(App[None]):
    """Interactive terminal interface for EZcli."""

    TITLE = "EZcli"
    SUB_TITLE = "Local Bash Command Assistant (Ollama)"

    CSS = """
    Screen {
        padding: 1 2;
    }

    #prompt {
        margin-bottom: 1;
    }

    #result {
        height: 1fr;
        border: round $primary;
        padding: 1;
        margin-bottom: 1;
    }

    #actions {
        height: auto;
        color: $text-muted;
        padding: 0 1;
    }
    """

    BINDINGS = [
        ("e", "execute_action", "Execute"),
        ("m", "modify_action", "Modify"),
        ("d", "describe_action", "Describe"),
        ("a", "abort_action", "Abort"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.service = CommandService()
        self._prepared: PreparedCommand | None = None
        self._last_prompt: str = ""

    def compose(self) -> ComposeResult:
        """Build the application layout."""
        with Vertical():
            yield Static("> Nhập yêu cầu để sinh lệnh Bash.")
            yield Input(
                placeholder="Ví dụ: liệt kê các file trong thư mục hiện tại",
                id="prompt",
            )
            yield Static(
                "Lệnh được sinh ra sẽ hiển thị tại đây.",
                id="result",
                markup=False,
            )
            yield Static(
                "[E]xecute, [M]odify, [D]escribe, [A]bort",
                id="actions",
                markup=False,
            )

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Generate a command when Enter is pressed in the prompt."""
        prompt = event.value.strip()
        if prompt:
            self._handle_generation(prompt)

    def action_execute_action(self) -> None:
        """Start the execute workflow for the prepared command."""
        if self._prepared is None:
            return
        if self._prepared.safety.level == SafetyLevel.BLOCKED:
            self.query_one("#result", Static).update(
                "Lệnh bị chặn và không thể thực thi."
            )
            return
        self.push_screen(ConfirmScreen(self._prepared), self._on_confirmation)

    def action_modify_action(self) -> None:
        """Open the command editor when a command has been generated."""
        if self._prepared is None:
            return
        self.push_screen(ModifyScreen(self._prepared), self._on_modified)

    def action_describe_action(self) -> None:
        """Show the available description for the prepared command."""
        if self._prepared is None:
            return
        explanation = self._prepared.generated.explanation.strip()
        if not explanation:
            explanation = "Chưa có mô tả cho lệnh này."
        self.query_one("#result", Static).update(
            f"{self._prepared.generated.command}\n\nGiải thích:\n{explanation}"
        )

    def action_abort_action(self) -> None:
        """Abort the current command workflow and return to prompt input."""
        self._prepared = None
        self._last_prompt = ""
        prompt = self.query_one("#prompt", Input)
        prompt.value = ""
        prompt.disabled = False
        prompt.focus()
        self.query_one("#result", Static).update(
            "Đã hủy. Nhập yêu cầu mới rồi nhấn Enter."
        )

    def _handle_generation(self, prompt: str) -> None:
        """Generate a command through the real LLM service."""
        self._last_prompt = prompt
        self._prepared = None
        self.query_one("#result", Static).update("Đang sinh lệnh...")

        try:
            prepared = self.service.prepare_command(prompt)
        except RuntimeError as exc:
            self.query_one("#result", Static).update(f"[Lỗi]: {exc}")
            return
        except Exception as exc:
            self.query_one("#result", Static).update(f"Không thể sinh lệnh: {exc}")
            return

        self._show_result(prepared)

    def _show_result(self, prepared: PreparedCommand) -> None:
        """Display a generated command and enable keyboard actions."""
        self._prepared = prepared
        self.query_one("#prompt", Input).disabled = True
        self.query_one("#result", Static).update(prepared.generated.command)

    def _on_modified(self, command: str | None) -> None:
        """Apply an edited command and recalculate its safety level."""
        if command is None or self._prepared is None:
            return
        command = command.strip()
        if not command:
            self.query_one("#result", Static).update("Lệnh không được để trống.")
            return
        generated = self._prepared.generated
        updated = PreparedCommand(
            generated=type(generated)(
                prompt=generated.prompt,
                command=command,
                explanation=generated.explanation,
            ),
            safety=check_command(command),
        )
        self._show_result(updated)

    def _on_confirmation(self, confirmed: bool | None) -> None:
        """Handle execution confirmation or return back to generation view."""
        if not confirmed or self._prepared is None:
            if self._prepared is not None:
                self._show_result(self._prepared)
            elif self._last_prompt:
                self._handle_generation(self._last_prompt)
            else:
                self.query_one("#result", Static).update("Đã hủy thực thi.")
            return

        prepared = self._prepared

        if sys.platform == "win32":
            try:
                stdout_stream: TextIO = sys.stdout
                stderr_stream: TextIO = sys.stderr
                if hasattr(stdout_stream, "reconfigure"):
                    stdout_stream.reconfigure(encoding="utf-8")
                if hasattr(stderr_stream, "reconfigure"):
                    stderr_stream.reconfigure(encoding="utf-8")
            except Exception:
                pass

        result = execute_command(prepared.generated.command, confirmed=True)

        try:
            self.service.record_outcome(
                prepared,
                status=result.status,
                exit_code=result.exit_code,
            )
        except Exception:
            pass

        self.query_one("#result", Static).update(
            f"Trạng thái: {result.status.value}\n"
            f"Mã thoát: {result.exit_code}\n\n"
            f"STDOUT:\n{result.stdout or ''}\n\n"
            f"STDERR:\n{result.stderr or ''}"
        )


class ConfirmScreen(ModalScreen[bool]):
    """Ask for explicit confirmation before executing a command."""

    def __init__(self, prepared: PreparedCommand) -> None:
        super().__init__()
        self.prepared = prepared

    def compose(self) -> ComposeResult:
        yield Static(
            "Bạn có chắc muốn thực thi lệnh này?\n\n"
            f"{self.prepared.generated.command}\n\n"
            f"Mức an toàn: {self.prepared.safety.level.value.upper()}"
        )
        with Horizontal():
            yield Button("Xác nhận thực thi", id="confirm", variant="error")
            yield Button("Quay lại", id="back")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "confirm")


class ModifyScreen(ModalScreen[str | None]):
    """Collect an edited version of a generated command."""

    def __init__(self, prepared: PreparedCommand) -> None:
        super().__init__()
        self.prepared = prepared

    def compose(self) -> ComposeResult:
        yield Static("Sửa command rồi nhấn Enter để xác nhận.")
        yield Input(value=self.prepared.generated.command, id="modified-command")
        with Horizontal():
            yield Button("Lưu", id="save", variant="primary")
            yield Button("Quay lại", id="back")

    def on_mount(self) -> None:
        self.query_one("#modified-command", Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.dismiss(event.value)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            self.dismiss(self.query_one("#modified-command", Input).value)
        else:
            self.dismiss(None)


def run() -> None:
    """Start the EZcli terminal interface."""
    EZcliApp().run()
