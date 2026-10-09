
"""Textual terminal interface for EZcli."""

from textual import work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Input, Static

from ezcli.application import CommandService, PreparedCommand


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

    def compose(self) -> ComposeResult:
        """Build the application layout."""
        with Vertical():
            yield Static(
                "Nhập yêu cầu bằng ngôn ngữ tự nhiên để sinh lệnh Bash."
            )
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
                yield Button("Xóa", id="clear")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle action button presses."""
        if event.button.id == "generate":
            prompt = self.query_one("#prompt", Input).value.strip()
            if not prompt:
                self.query_one("#result", Static).update(
                    "Vui lòng nhập yêu cầu.",
                )
                return
            self._generate(prompt)

        elif event.button.id == "clear":
            self.query_one("#prompt", Input).value = ""
            self.query_one("#result", Static).update(
                "Lệnh được sinh ra sẽ hiển thị tại đây."
            )

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
        """Display the generated command and its safety assessment."""
        reasons = (
            "\n".join(f"- {reason}" for reason in prepared.safety.reasons)
            or "Không có cảnh báo từ các quy tắc hiện tại."
        )
        result = (
            f"Yêu cầu: {prepared.generated.prompt}\n\n"
            f"Lệnh Bash:\n{prepared.generated.command}\n\n"
            f"Mức an toàn: {prepared.safety.level.value.upper()}\n"
            f"Chi tiết:\n{reasons}\n\n"
            "Lệnh chưa được thực thi."
        )
        self.query_one("#result", Static).update(result)

    def _show_error(self, message: str) -> None:
        """Display an error message."""
        self.query_one("#result", Static).update(message)


def run() -> None:
    """Start the EZcli terminal interface."""
    EZcliApp().run()
