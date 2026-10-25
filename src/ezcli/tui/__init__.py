import sys
from collections.abc import Iterable
from datetime import datetime
from pathlib import Path
from typing import TextIO

from textual import events
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.geometry import Region
from textual.message import Message
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Button, Input, OptionList, Static, TextArea
from textual.widgets.option_list import Option

from ezcli.application import CommandService, PreparedCommand
from ezcli.domain.models import GeneratedCommand, HistoryEntry, SafetyLevel
from ezcli.execution import execute_command
from ezcli.history import HistoryStore
from ezcli.plugins import handle_plugin_command
from ezcli.safety import check_command
from ezcli.tui.commands import SLASH_COMMANDS


class CommandOptionList(OptionList):
    """OptionList chuyên dụng cho slash commands, tự động điền lệnh khi nhấn Enter."""

    async def _on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            event.stop()
            event.prevent_default()
            if self.highlighted is not None:
                option = self.get_option_at_index(self.highlighted)
                if option and option.id:
                    self.app.post_message(CommandSelected(str(option.id)))
            return
        elif event.key == "escape":
            event.stop()
            event.prevent_default()
            self.display = False
            self.app.query_one("#prompt", TextArea).focus()
            return
        await super()._on_key(event)


class CommandSelected(Message):
    """Message tự định nghĩa khi người dùng chọn một lệnh từ OptionList."""

    def __init__(self, command: str) -> None:
        super().__init__()
        self.command = command


class LeftScrollTextArea(TextArea):
    """Text area that keeps its vertical scrollbar on the left."""

    async def _on_key(self, event: events.Key) -> None:
        """Submit the prompt instead of inserting a newline."""

        if self.id == "prompt" and event.key == "down":
            command_list = self.app.query_one("#command-list", CommandOptionList)
            if command_list.display:
                event.stop()
                event.prevent_default()
                command_list.focus()
                return

        if self.id == "prompt" and event.key == "q":
            event.stop()
            event.prevent_default()
            self.app.exit()
            return

        if self.id == "prompt" and event.key == "enter":
            event.stop()
            event.prevent_default()

            command_list = self.app.query_one("#command-list", CommandOptionList)

            if command_list.display:
                if command_list.highlighted is not None:
                    option = command_list.get_option_at_index(command_list.highlighted)
                    if option and option.id:
                        self.app.post_message(CommandSelected(str(option.id)))
                return

            self.post_message(PromptSubmitted(self.text))
            return

        await super()._on_key(event)

    def _arrange_scrollbars(self, region: Region) -> Iterable[tuple[Widget, Region]]:
        if self.show_horizontal_scrollbar:
            yield from super()._arrange_scrollbars(region)
            return

        if self.show_vertical_scrollbar and self.scrollbar_size_vertical:
            window_region, scrollbar_region = region.split_vertical(
                self.scrollbar_size_vertical
            )
            scrollbar = self.vertical_scrollbar
            scrollbar.window_virtual_size = self.virtual_size.height
            scrollbar.window_size = window_region.height
            yield scrollbar, scrollbar_region
            return

        yield from super()._arrange_scrollbars(region)


class PromptSubmitted(Message):
    """Message emitted when the main prompt is submitted."""

    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text


class EZcliApp(App[None]):
    """Interactive terminal interface for EZcli."""

    TITLE = "EZcli"
    SUB_TITLE = "Local Bash Command Assistant (Ollama)"

    CSS = """

    Screen {
        padding: 1 2;
        background: transparent;
    }

    #prompt {
        height: 5;
        min-height: 2;
        margin: 0 0 1 0;
        padding: 0 1;
    }

    #command-list {
        height: auto;
        max-height: 5;
        margin-bottom: 1;
        display: none;
    }

    #result-scroll {
        height: 1fr;
        border: round $primary;
        padding: 0 1;
        margin-bottom: 0;
    }

    #result {
        width: 100%;
        height: auto;
    }

    #actions {
        height: auto;
        color: $text-muted;
        padding: 0 1;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True, show=False),
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
        self.history_store = HistoryStore(Path(".ezcli_history.json"))
        self._is_selecting_command = False

    def compose(self) -> ComposeResult:
        """Build the application layout."""
        options = [
            Option(f"{cmd} - {desc}", id=cmd) for cmd, desc in SLASH_COMMANDS.items()
        ]

        with Vertical():
            yield Static("> Nhập yêu cầu để sinh lệnh Bash.\n")
            yield LeftScrollTextArea(
                placeholder="Ví dụ: liệt kê các file trong thư mục hiện tại",
                id="prompt",
            )
            yield CommandOptionList(*options, id="command-list")
            with VerticalScroll(id="result-scroll"):
                yield Static(
                    "Lệnh được sinh ra sẽ hiển thị tại đây.",
                    id="result",
                    markup=True,
                )

            yield Static(
                "[E]xecute, [M]odify, [D]escribe, [A]bort",
                id="actions",
                markup=False,
            )

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        if self._is_selecting_command:
            return

        if event.text_area.id != "prompt":
            return

        text = event.text_area.text.strip()
        command_list = self.query_one("#command-list", CommandOptionList)

        if text == "/":
            command_list.display = True
        elif not text.startswith("/"):
            command_list.display = False

    def on_command_selected(self, message: CommandSelected) -> None:
        """Điền lệnh được chọn, ẩn menu và trả focus về prompt."""
        command_list = self.query_one("#command-list", CommandOptionList)
        prompt_widget = self.query_one("#prompt", TextArea)
        command_list.display = False

        self._is_selecting_command = True
        prompt_widget.load_text(message.command)
        prompt_widget.focus()

        self.call_after_refresh(setattr, self, "_is_selecting_command", False)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Generate a command when Enter is pressed in the prompt."""
        prompt = event.value.strip()
        if prompt:
            self._handle_generation(prompt)

    def on_prompt_submitted(self, event: PromptSubmitted) -> None:
        """Generate a command when Enter is pressed in the prompt."""
        prompt = event.text.strip()
        if prompt:
            self._handle_generation(prompt)

    def _update_result(self, text: str) -> None:
        """Update the scrollable result area."""
        self.query_one("#result", Static).update(text)

    def action_execute_action(self) -> None:
        """Start the execute workflow for the prepared command."""
        if self._prepared is None:
            return
        if self._prepared.safety.level == SafetyLevel.BLOCKED:
            self._update_result("Lệnh bị chặn và không thể thực thi.")
            return
        self.push_screen(ConfirmScreen(self._prepared), self._on_confirmation)

    def action_modify_action(self) -> None:
        """Open the command editor when a command has been generated."""
        if self._prepared is None:
            return
        self.push_screen(ModifyScreen(self._prepared), self._on_modified)

    def action_describe_action(self) -> None:
        """Request and show a description for the prepared command."""
        if self._prepared is None:
            return
        command = self._prepared.generated.command
        self._update_result("Đang tạo mô tả...")
        self.run_worker(
            lambda: self._explain_in_background(command),
            thread=True,
        )

    def _explain_in_background(self, command: str) -> None:
        """Request an explanation without blocking the Textual event loop."""
        try:
            explanation = self.service.explain_command(command)
        except RuntimeError as exc:
            self.call_from_thread(self._show_explanation_error, command, str(exc))
            return
        self.call_from_thread(
            self._show_explanation,
            command,
            explanation,
        )

    def _show_explanation(self, command: str, explanation: str) -> None:
        """Render an explanation if the command is still current."""
        if self._prepared is None or self._prepared.generated.command != command:
            return
        self._update_result(f"{command}\n\nGiải thích:\n{explanation}")

    def _show_explanation_error(self, command: str, error: str) -> None:
        """Render an explanation error if the command is still current."""
        if self._prepared is None or self._prepared.generated.command != command:
            return
        self._update_result(f"{command}\n\n[Lỗi]: {error}")

    def action_abort_action(self) -> None:
        """Abort the current command workflow and return to prompt input."""
        self._prepared = None
        self._last_prompt = ""
        prompt = self.query_one("#prompt", TextArea)
        prompt.load_text("")
        prompt.disabled = False
        prompt.focus()
        self._update_result("Đã hủy. Nhập yêu cầu mới rồi nhấn Enter.")

    def _handle_generation(self, prompt: str) -> None:
        """Generate a command through the real LLM service."""
        cleaned_prompt = prompt.strip()
        # Xử lý lệnh xem lịch sử
        if cleaned_prompt == "/history":
            history_text = handle_history_command(self.history_store)
            self._update_result(history_text)
            return

        # Xử lý lệnh quản lý plugin
        if cleaned_prompt == "/plugin" or cleaned_prompt.startswith("/plugin "):
            self._handle_plugin(cleaned_prompt)
            return

        self._last_prompt = prompt
        self._prepared = None
        prompt_widget = self.query_one("#prompt", TextArea)
        prompt_widget.load_text("Đang xử lý...")
        prompt_widget.disabled = True
        self.run_worker(
            lambda: self._prepare_in_background(prompt),
            thread=True,
        )

    def _prepare_in_background(self, prompt: str) -> None:
        """Prepare a command without blocking the Textual event loop."""
        try:
            prepared = self.service.prepare_command(prompt)
        except RuntimeError as exc:
            self.call_from_thread(self._show_generation_error, prompt, str(exc))
            return
        except Exception as exc:
            self.call_from_thread(
                self._show_generation_error,
                prompt,
                f"Không thể sinh lệnh: {exc}",
            )
            return

        self.call_from_thread(self._show_prepared_result, prompt, prepared)

    def _show_generation_error(self, prompt: str, error: str) -> None:
        """Restore the prompt and show a generation error."""
        prompt_widget = self.query_one("#prompt", TextArea)
        prompt_widget.load_text(prompt)
        prompt_widget.disabled = False
        prompt_widget.focus()
        self._update_result(f"[Lỗi]: {error}")

    def _show_prepared_result(self, prompt: str, prepared: PreparedCommand) -> None:
        """Restore the prompt and show the prepared command."""
        prompt_widget = self.query_one("#prompt", TextArea)
        prompt_widget.load_text(prompt)
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
            self._update_result(
                f"{result.message}\n\nNhấn 'Thực thi' để chạy lệnh này."
            )
        else:
            self._prepared = None
            self.query_one("#execute", Button).disabled = True
            self._update_result(result.message)

    def _show_result(self, prepared: PreparedCommand) -> None:
        """Display a generated command and enable keyboard actions."""
        self._prepared = prepared

        self.query_one("#prompt", TextArea).disabled = True
        safety_level = prepared.safety.level
        if safety_level == SafetyLevel.SAFE:
            color = "green"
        elif safety_level == SafetyLevel.WARNING:
            color = "yellow"
        else:  # BLOCKED
            color = "red"
        result_text = f"[{color}]{prepared.generated.command}[/{color}]\n\n"
        self._update_result(result_text)

    def _on_modified(self, command: str | None) -> None:
        """Apply an edited command and recalculate its safety level."""
        if command is None or self._prepared is None:
            return
        command = command.strip()
        if not command:
            self._update_result("Lệnh không được để trống.")
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
                self._update_result("Đã hủy thực thi.")
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

        self._update_result(
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
        if self.prepared.safety.level == SafetyLevel.WARNING:
            reasons = "\n".join(
                f"- {reason}" for reason in self.prepared.safety.reasons
            )
            message = (
                "CẢNH BÁO: lệnh này có thể ảnh hưởng đến hệ thống.\n\n"
                f"{self.prepared.generated.command}\n\n"
                f"Lý do cảnh báo:\n{reasons}\n\n"
                "Bạn có hiểu rủi ro và vẫn muốn thực thi không?"
            )
            confirm_label = "Tôi hiểu, vẫn thực thi"
        else:
            message = (
                "Bạn có chắc muốn thực thi lệnh này?\n\n"
                f"{self.prepared.generated.command}\n\n"
                f"Mức an toàn: {self.prepared.safety.level.value.upper()}"
            )
            confirm_label = "Xác nhận thực thi"

        yield Static(message)
        with Horizontal():
            yield Button(confirm_label, id="confirm", variant="error")
            yield Button("Hủy", id="back")

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
