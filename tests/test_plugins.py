"""Unit tests for the EZcli plugin management module.

All tests run 100% offline using mock checks without making external network calls.
"""

from __future__ import annotations

from pathlib import Path

from ezcli.plugins import (
    SUPPORTED_PLUGINS,
    PluginInfo,
    format_plugins_list,
    handle_plugin_command,
    is_plugin_installed,
    list_plugins,
)


def test_is_plugin_installed_detected_via_which() -> None:
    """When a command is found in PATH, is_plugin_installed returns True."""
    spec = SUPPORTED_PLUGINS["tldr"]

    def mock_which(cmd: str) -> str | None:
        return "/usr/bin/tldr" if cmd == "tldr" else None

    assert is_plugin_installed(spec, which_func=mock_which) is True


def test_is_plugin_installed_not_found(tmp_path: Path) -> None:
    """When command is not in PATH and no directory exists, returns False."""
    spec = SUPPORTED_PLUGINS["tldr"]

    def mock_which(cmd: str) -> str | None:
        return None

    assert is_plugin_installed(spec, home_dir=tmp_path, which_func=mock_which) is False


def test_is_plugin_installed_detected_via_home_directory(tmp_path: Path) -> None:
    """When plugin is stored in ~/.zsh/..., detects via file system."""
    spec = SUPPORTED_PLUGINS["zsh-autosuggestions"]
    zsh_plugin_dir = tmp_path / ".zsh" / "zsh-autosuggestions"
    zsh_plugin_dir.mkdir(parents=True)

    def mock_which(cmd: str) -> str | None:
        return None

    assert is_plugin_installed(spec, home_dir=tmp_path, which_func=mock_which) is True


def test_list_plugins_returns_all_supported(tmp_path: Path) -> None:
    """list_plugins contains all items defined in SUPPORTED_PLUGINS."""

    def mock_which(cmd: str) -> str | None:
        return None

    plugins = list_plugins(home_dir=tmp_path, which_func=mock_which)
    names = [p.name for p in plugins]

    assert "tldr" in names
    assert "fzf" in names
    assert "zsh-autosuggestions" in names
    assert "zsh-syntax-highlighting" in names
    assert all(not p.installed for p in plugins)


def test_format_plugins_list() -> None:
    """format_plugins_list produces readable status text."""
    plugins = [
        PluginInfo(
            name="tldr",
            description="Short man pages",
            installed=True,
            install_command="pip install tldr",
            uninstall_command="pip uninstall -y tldr",
        ),
        PluginInfo(
            name="fzf",
            description="Fuzzy finder",
            installed=False,
            install_command="...",
            uninstall_command="...",
        ),
    ]
    output = format_plugins_list(plugins)

    assert "QUẢN LÝ PLUGINS" in output
    assert "[✓] Đã cài đặt" in output
    assert "[✗] Chưa cài đặt" in output
    assert "tldr" in output
    assert "fzf" in output


def test_handle_plugin_command_list(tmp_path: Path) -> None:
    """Invoking handle_plugin_command with no args or 'list' returns formatted list."""

    def mock_which(cmd: str) -> str | None:
        return None

    result_default = handle_plugin_command([], home_dir=tmp_path, which_func=mock_which)
    assert result_default.command is None
    assert "QUẢN LÝ PLUGINS" in result_default.message

    result_list = handle_plugin_command(
        ["list"], home_dir=tmp_path, which_func=mock_which
    )
    assert result_list.command is None
    assert "QUẢN LÝ PLUGINS" in result_list.message


def test_handle_plugin_command_install_missing_arg() -> None:
    """Running install without plugin name returns guidance message."""
    result = handle_plugin_command(["install"])
    assert result.command is None
    assert "chỉ định tên plugin" in result.message


def test_handle_plugin_command_install_unsupported() -> None:
    """Running install for unsupported plugin returns error with available options."""
    result = handle_plugin_command(["install", "non_existent_tool"])
    assert result.command is None
    assert "không được hỗ trợ" in result.message


def test_handle_plugin_command_install_when_already_installed() -> None:
    """When plugin is already installed, does not generate install command."""

    def mock_which(cmd: str) -> str | None:
        return "/bin/tldr" if cmd == "tldr" else None

    result = handle_plugin_command(["install", "tldr"], which_func=mock_which)
    assert result.command is None
    assert "đã được cài đặt" in result.message


def test_handle_plugin_command_install_when_not_installed(tmp_path: Path) -> None:
    """When plugin is not installed, generates install command."""

    def mock_which(cmd: str) -> str | None:
        return None

    result = handle_plugin_command(
        ["install", "tldr"], home_dir=tmp_path, which_func=mock_which
    )
    assert result.command == "pip install tldr"
    assert "Chuẩn bị cài đặt" in result.message


def test_handle_plugin_command_remove_missing_arg() -> None:
    """Running remove without plugin name returns guidance message."""
    result = handle_plugin_command(["remove"])
    assert result.command is None
    assert "chỉ định tên plugin" in result.message


def test_handle_plugin_command_remove_unsupported() -> None:
    """Running remove for unsupported plugin returns error message."""
    result = handle_plugin_command(["remove", "unknown_tool"])
    assert result.command is None
    assert "không được hỗ trợ" in result.message


def test_handle_plugin_command_remove_when_not_installed(tmp_path: Path) -> None:
    """When plugin is not installed, remove indicates it is not installed."""

    def mock_which(cmd: str) -> str | None:
        return None

    result = handle_plugin_command(
        ["remove", "tldr"], home_dir=tmp_path, which_func=mock_which
    )
    assert result.command is None
    assert "chưa được cài đặt" in result.message


def test_handle_plugin_command_remove_when_installed() -> None:
    """When plugin is installed, generates uninstall command."""

    def mock_which(cmd: str) -> str | None:
        return "/bin/tldr" if cmd == "tldr" else None

    result = handle_plugin_command(["remove", "tldr"], which_func=mock_which)
    assert result.command == "pip uninstall -y tldr"
    assert "Chuẩn bị gỡ cài đặt" in result.message


def test_handle_plugin_command_unknown_subcommand() -> None:
    """Unknown subcommands return helpful syntax instructions."""
    result = handle_plugin_command(["invalid_subcommand"])
    assert result.command is None
    assert "không hợp lệ" in result.message
