"""Textual terminal interface for EZcli."""

from textual import work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Static

from ezcli.application import CommandService, PreparedCommand
from ezcli.domain.models import SafetyLevel
from ezcli.execution import execute_command


class EZcliApp(App[None]):
    """Interactive terminal interface for EZcli."""

    TITLE = "EZcli"
    SUB_TITLE = "Local Bash Command Assistant"

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
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self.service = CommandService()
        self._prepared: PreparedCommand | None = None

    def compose(self) -> ComposeResult:
        """Build the application layout."""
        with Vertical():
            yield Static("Nhập yêu cầu bằng ngôn ngữ tự nhiên để sinh lệnh Bash.")
            yield Input(
                placeholder="Ví dụ: liệt kê các file trong thư mục hiện tại",
                id="prompt",
            )
            yield Static(
                "Lệnh được sinh ra sẽ hiển thị tại đây.",
                id="result",
                markup=False,
            )
            with Horizontal(id="actions"):
                yield Button("Sinh lệnh", id="generate", variant="primary")
                yield Button("Thực thi", id="execute", variant="success", disabled=True)
                yield Button("Hủy", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle action button presses."""
        if event.button.id == "generate":
            prompt = self.query_one("#prompt", Input).value.strip()
            if not prompt:
                self.query_one("#result", Static).update("Vui lòng nhập yêu cầu.")
                return
            self._prepared = None
            self.query_one("#execute", Button).disabled = True
            self._generate(prompt)

        elif event.button.id == "execute":
            if self._prepared is None:
                return
            if self._prepared.safety.level == SafetyLevel.BLOCKED:
                self.query_one("#result", Static).update(
                    "Lệnh bị chặn và không thể thực thi."
                )
                return
            self.push_screen(
                ConfirmScreen(self._prepared),
                self._on_confirmation,
            )

        elif event.button.id == "cancel":
            self._prepared = None
            self.query_one("#execute", Button).disabled = True
            self.query_one("#result", Static).update("Đã hủy thao tác.")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Generate a command when Enter is pressed in the input."""
        if event.input.id == "prompt" and event.value.strip():
            self._generate(event.value.strip())

    @work(thread=True)
    def _generate(self, prompt: str) -> None:
        """Generate and assess a command without executing it."""
        try:
            prepared = self.service.prepare_command(prompt)
            self.app.call_from_thread(self._show_result, prepared)
        except Exception as exc:
            self.app.call_from_thread(
                self._show_error,
                f"Không thể sinh lệnh: {exc}",
            )

    def _show_result(self, prepared: PreparedCommand) -> None:
        """Display generated command and safety assessment."""
        self._prepared = prepared
        self.query_one("#execute", Button).disabled = (
            prepared.safety.level == SafetyLevel.BLOCKED
        )

        reasons = (
            "\n".join(f"- {reason}" for reason in prepared.safety.reasons)
            or "Không có cảnh báo từ các quy tắc hiện tại."
        )

        self.query_one("#result", Static).update(
            f"Yêu cầu: {prepared.generated.prompt}\n\n"
            f"Lệnh Bash:\n{prepared.generated.command}\n\n"
            f"Mức an toàn: {prepared.safety.level.value.upper()}\n"
            f"Chi tiết:\n{reasons}\n\n"
            "Lệnh chưa được thực thi."
        )

    def _show_error(self, message: str) -> None:
        """Display an error message."""
        self.query_one("#result", Static).update(message)

    def _on_confirmation(self, confirmed: bool | None) -> None:
        """Execute only after explicit user confirmation."""
        if not confirmed or self._prepared is None:
            self.query_one("#result", Static).update("Đã hủy thực thi.")
            return

        prepared = self._prepared
        result = execute_command(
            prepared.generated.command,
            confirmed=True,
        )

        self.service.record_outcome(
            prepared,
            status=result.status,
            exit_code=result.exit_code,
        )

        self.query_one("#result", Static).update(
            f"Trạng thái: {result.status.value}\n"
            f"Mã thoát: {result.exit_code}\n\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
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
        if event.button.id == "confirm":
            self.dismiss(True)
        else:
            self.dismiss(False)


def run() -> None:
    """Start the EZcli terminal interface."""
    EZcliApp().run()
