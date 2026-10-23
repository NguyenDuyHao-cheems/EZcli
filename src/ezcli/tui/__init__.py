"""Textual terminal interface for EZcli backed by the Ollama LLM client."""

import sys
from datetime import datetime
from pathlib import Path
from typing import TextIO

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Static

from ezcli.application import CommandService, PreparedCommand
from ezcli.domain.models import GeneratedCommand, HistoryEntry, SafetyLevel
from ezcli.execution import execute_command
from ezcli.history import HistoryStore
from ezcli.plugins import handle_plugin_command
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
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self.service = CommandService()
        self._prepared: PreparedCommand | None = None
        self._last_prompt: str = ""
        self.history_store = HistoryStore(Path(".ezcli_history.json"))

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
                markup=True,
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
            self._handle_generation(prompt)

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
            self._last_prompt = ""
            self.query_one("#execute", Button).disabled = True
            self.query_one("#result", Static).update("Đã hủy thao tác.")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Generate a command when Enter is pressed in the input."""
        prompt = event.value.strip()
        if prompt:
            self._handle_generation(prompt)

    def _handle_generation(self, prompt: str) -> None:
        """Generate a command through the real LLM service."""
        cleaned_prompt = prompt.strip()
        # Xử lý lệnh xem lịch sử
        if cleaned_prompt == "/history":
            history_text = handle_history_command(self.history_store)
            self.query_one("#result", Static).update(history_text)
            return

        # Xử lý lệnh quản lý plugin
        if cleaned_prompt == "/plugin" or cleaned_prompt.startswith("/plugin "):
            self._handle_plugin(cleaned_prompt)
            return

        self._last_prompt = prompt
        self._prepared = None
        self.query_one("#execute", Button).disabled = True
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

    def _handle_plugin(self, prompt: str) -> None:
        """Process /plugin slash commands (list, install, remove)."""
        parts = prompt.split()
        args = parts[1:]
        result = handle_plugin_command(args)

        self._last_prompt = prompt
        if result.command:
            safety = check_command(result.command)
            prepared = PreparedCommand(
                generated=GeneratedCommand(prompt=prompt, command=result.command),
                safety=safety,
            )
            self._prepared = prepared
            self.query_one("#execute", Button).disabled = (
                safety.level == SafetyLevel.BLOCKED
            )
            self.query_one("#result", Static).update(
                f"{result.message}\n\nNhấn 'Thực thi' để chạy lệnh này."
            )
        else:
            self._prepared = None
            self.query_one("#execute", Button).disabled = True
            self.query_one("#result", Static).update(result.message)

    def _show_result(self, prepared: PreparedCommand) -> None:
        """Display generated command concisely."""
        self._prepared = prepared
        self.query_one("#execute", Button).disabled = (
            prepared.safety.level == SafetyLevel.BLOCKED
        )
        current_dir = Path.cwd()
        safety_level = prepared.safety.level
        if safety_level == SafetyLevel.SAFE:
            color = "green"
        elif safety_level == SafetyLevel.WARNING:
            color = "yellow"
        else:  # BLOCKED
            color = "red"

        result_text = (
            f"Câu lệnh Bash:\n[{color}]{prepared.generated.command}[/{color}]\n\n"
            f"[dim] Thư mục hiện tại:\n {current_dir}[/dim]"
        )
        self.query_one("#result", Static).update(result_text)

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

        result = execute_command(
            prepared.generated.command,
            confirmed=True,
        )

        try:
            self.service.record_outcome(
                prepared,
                status=result.status,
                exit_code=result.exit_code,
            )
        except Exception:
            pass

        entry = HistoryEntry(
            prompt=self._last_prompt,
            command=prepared.generated.command,
            timestamp=datetime.now(),
            safety=prepared.safety.level,
            status=result.status,
            exit_code=result.exit_code,
        )
        try:
            self.history_store.save(entry)
        except Exception as e:
            print(f"Lỗi lưu lịch sử: {e}")

        stdout_text = result.stdout or ""
        stderr_text = result.stderr or ""

        self.query_one("#result", Static).update(
            f"Trạng thái: {result.status.value}\n"
            f"Mã thoát: {result.exit_code}\n\n"
            f"STDOUT:\n{stdout_text}\n\n"
            f"STDERR:\n{stderr_text}"
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


def handle_history_command(store: HistoryStore) -> str:
    """Đọc lịch sử từ store và định dạng thành chuỗi hiển thị lên TUI."""
    entries = store.load()
    if not entries:
        return "Lịch sử thao tác trống."

    lines = ["=== LỊCH SỬ THAO TÁC ==="]
    for idx, item in enumerate(entries, start=1):
        time_str = item.timestamp.strftime("%H:%M:%S")
        status_val = item.status.value
        safety_val = item.safety.value
        lines.append(
            f"[{idx}] {time_str} | Status: {status_val} | Safety: {safety_val}"
        )

        lines.append(f"    Prompt  : {item.prompt}")
        lines.append(f"    Command : {item.command}")
        if item.exit_code is not None:
            lines.append(f"    Exit Code: {item.exit_code}")
        lines.append("-" * 40)

    return "\n".join(lines)


def run() -> None:
    """Start the EZcli terminal interface."""
    EZcliApp().run()
