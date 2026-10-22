"""Plugin management module for EZcli.

Supports listing, checking status, installing, and uninstalling common shell plugins.
"""

from __future__ import annotations

import shutil
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

__all__ = [
    "PluginCommandResult",
    "PluginInfo",
    "PluginSpec",
    "SUPPORTED_PLUGINS",
    "format_plugins_list",
    "handle_plugin_command",
    "is_plugin_installed",
    "list_plugins",
]


@dataclass(frozen=True)
class PluginSpec:
    """Specification of a supported shell plugin or CLI tool."""

    name: str
    description: str
    command_name: str
    relative_paths: tuple[str, ...] = ()
    install_command: str = ""
    uninstall_command: str = ""


@dataclass(frozen=True)
class PluginInfo:
    """Snapshot of a plugin's installation status."""

    name: str
    description: str
    installed: bool
    install_command: str
    uninstall_command: str


@dataclass(frozen=True)
class PluginCommandResult:
    """Outcome of processing a /plugin slash command."""

    message: str
    command: str | None = None


# Pre-defined curated catalog of popular shell plugins and utilities
SUPPORTED_PLUGINS: dict[str, PluginSpec] = {
    "tldr": PluginSpec(
        name="tldr",
        description="Simplified and community-driven man pages",
        command_name="tldr",
        install_command="pip install tldr",
        uninstall_command="pip uninstall -y tldr",
    ),
    "fzf": PluginSpec(
        name="fzf",
        description="Command-line fuzzy finder",
        command_name="fzf",
        install_command=(
            "git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf && "
            "~/.fzf/install --all"
        ),
        uninstall_command="rm -rf ~/.fzf",
    ),
    "zsh-autosuggestions": PluginSpec(
        name="zsh-autosuggestions",
        description="Fish-like autosuggestions for zsh",
        command_name="zsh-autosuggestions",
        relative_paths=(
            ".zsh/zsh-autosuggestions",
            ".oh-my-zsh/custom/plugins/zsh-autosuggestions",
        ),
        install_command=(
            "git clone https://github.com/zsh-users/zsh-autosuggestions "
            "~/.zsh/zsh-autosuggestions"
        ),
        uninstall_command="rm -rf ~/.zsh/zsh-autosuggestions",
    ),
    "zsh-syntax-highlighting": PluginSpec(
        name="zsh-syntax-highlighting",
        description="Fish-like syntax highlighting for zsh",
        command_name="zsh-syntax-highlighting",
        relative_paths=(
            ".zsh/zsh-syntax-highlighting",
            ".oh-my-zsh/custom/plugins/zsh-syntax-highlighting",
        ),
        install_command=(
            "git clone https://github.com/zsh-users/zsh-syntax-highlighting.git "
            "~/.zsh/zsh-syntax-highlighting"
        ),
        uninstall_command="rm -rf ~/.zsh/zsh-syntax-highlighting",
    ),
}


def is_plugin_installed(
    spec: PluginSpec,
    *,
    home_dir: Path | None = None,
    which_func: Callable[[str], str | None] | None = None,
) -> bool:
    """Check if a plugin/tool is installed on the system."""
    check_which = which_func or shutil.which
    if check_which(spec.command_name) is not None:
        return True

    target_home = home_dir or Path.home()
    for rel_path in spec.relative_paths:
        try:
            if (target_home / rel_path).exists():
                return True
        except Exception:
            pass

    return False


def list_plugins(
    *,
    home_dir: Path | None = None,
    which_func: Callable[[str], str | None] | None = None,
) -> list[PluginInfo]:
    """Return all supported plugins with their installation statuses."""
    result: list[PluginInfo] = []
    for spec in SUPPORTED_PLUGINS.values():
        installed = is_plugin_installed(spec, home_dir=home_dir, which_func=which_func)
        result.append(
            PluginInfo(
                name=spec.name,
                description=spec.description,
                installed=installed,
                install_command=spec.install_command,
                uninstall_command=spec.uninstall_command,
            )
        )
    return result


def format_plugins_list(plugins: list[PluginInfo]) -> str:
    """Format the list of plugins for display in TUI or terminal."""
    lines = [
        "=== QUẢN LÝ PLUGINS ===",
        "Danh sách các plugin hỗ trợ:",
    ]
    for p in plugins:
        status = "[✓] Đã cài đặt" if p.installed else "[✗] Chưa cài đặt"
        lines.append(f"- {p.name:<24} : {status} - {p.description}")

    lines.append("")
    lines.append("Cú pháp sử dụng:")
    lines.append("  /plugin                   : Xem danh sách plugin")
    lines.append("  /plugin install <tên>     : Cài plugin (vd: /plugin install tldr)")
    lines.append("  /plugin remove <tên>      : Gỡ cài đặt plugin")
    return "\n".join(lines)


def handle_plugin_command(
    args: list[str],
    *,
    home_dir: Path | None = None,
    which_func: Callable[[str], str | None] | None = None,
) -> PluginCommandResult:
    """Handle /plugin slash command and arguments.

    Returns:
        PluginCommandResult with display message and optional command to execute.
    """
    if not args or args[0] in ("list", "ls"):
        plugins = list_plugins(home_dir=home_dir, which_func=which_func)
        return PluginCommandResult(message=format_plugins_list(plugins))

    subcommand = args[0].lower()

    if subcommand in ("install", "add"):
        if len(args) < 2:
            return PluginCommandResult(
                message=(
                    "Vui lòng chỉ định tên plugin cần cài đặt. "
                    "Ví dụ: /plugin install tldr"
                )
            )
        plugin_name = args[1].strip().lower()
        spec = SUPPORTED_PLUGINS.get(plugin_name)
        if spec is None:
            available = ", ".join(SUPPORTED_PLUGINS.keys())
            return PluginCommandResult(
                message=(
                    f"Plugin '{plugin_name}' không được hỗ trợ. "
                    f"Các plugin khả dụng: {available}"
                )
            )
        if is_plugin_installed(spec, home_dir=home_dir, which_func=which_func):
            return PluginCommandResult(
                message=f"Plugin '{plugin_name}' đã được cài đặt trên hệ thống."
            )
        return PluginCommandResult(
            message=(
                f"Chuẩn bị cài đặt plugin '{plugin_name}'. Lệnh: {spec.install_command}"
            ),
            command=spec.install_command,
        )

    if subcommand in ("remove", "uninstall", "delete", "rm"):
        if len(args) < 2:
            return PluginCommandResult(
                message=(
                    "Vui lòng chỉ định tên plugin cần gỡ cài đặt. "
                    "Ví dụ: /plugin remove tldr"
                )
            )
        plugin_name = args[1].strip().lower()
        spec = SUPPORTED_PLUGINS.get(plugin_name)
        if spec is None:
            available = ", ".join(SUPPORTED_PLUGINS.keys())
            return PluginCommandResult(
                message=(
                    f"Plugin '{plugin_name}' không được hỗ trợ. "
                    f"Các plugin khả dụng: {available}"
                )
            )
        if not is_plugin_installed(spec, home_dir=home_dir, which_func=which_func):
            return PluginCommandResult(
                message=f"Plugin '{plugin_name}' chưa được cài đặt trên hệ thống."
            )
        return PluginCommandResult(
            message=(
                f"Chuẩn bị gỡ cài đặt plugin '{plugin_name}'. "
                f"Lệnh: {spec.uninstall_command}"
            ),
            command=spec.uninstall_command,
        )

    return PluginCommandResult(
        message=(
            f"Lệnh phụ '/plugin {args[0]}' không hợp lệ.\n"
            "Dùng '/plugin' hoặc '/plugin list' để xem danh sách hỗ trợ."
        )
    )
