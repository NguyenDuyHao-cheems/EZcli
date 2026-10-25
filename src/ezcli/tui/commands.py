SLASH_COMMANDS: dict[str, str] = {
    "/history": "Xem lịch sử các lệnh đã thực thi",
    "/plugin": "Quản lý plugin",
}


def get_registered_commands() -> list[str]:
    """Tự động trả về danh sách tất cả các lệnh bắt đầu bằng '/'."""
    return list(SLASH_COMMANDS.keys())
