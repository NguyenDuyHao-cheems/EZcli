# plan cho sprint 1

[plan](https://chatgpt.com/s/t_6ac8bb9786ac81918a563724d69641ad)


# 12/10/2026 Chốt contract LLMClient và LLMResult

## Báo cáo rà soát và thực hiện lại Sprint 1

### Khó khăn và điểm chưa đồng bộ đã phát hiện

Khi đối chiếu contract LLM với SRS, có hai kiểu kết quả cùng tồn tại:

- `LLMResult(success, content, error)` phù hợp để mô tả trạng thái giao tiếp với
  LLM.
- `GeneratedCommand(prompt, command, explanation)` phù hợp hơn với nghiệp vụ
  EZcli vì SRS yêu cầu sinh Bash command, hiển thị command, safety checking,
  confirmation và lưu prompt/command vào history.

Codebase ban đầu kiểm thử hai hướng riêng biệt: contract test dùng
`LLMResult`, còn Ollama adapter và application dùng
`generate_command() -> GeneratedCommand`. Vì vậy test đều có thể chạy thành
 công nhưng adapter thật chưa thực sự implement `LLMClient`.

Điểm khó khăn chính là phải giữ được context của shell trong pipeline, đồng
thời không đưa chi tiết HTTP, JSON, model hoặc streaming vào contract public.
Ngoài ra, lỗi Ollama cần được xử lý rõ ràng để thỏa mãn yêu cầu reliability
trong SRS.

### Quyết định contract

Sprint 1 được chốt theo model nghiệp vụ `GeneratedCommand`:

```python
class LLMClient(Protocol):
    def generate(
        self,
        prompt: str,
        context: dict[str, str] | None = None,
    ) -> GeneratedCommand: ...
```

`GeneratedCommand` được dùng xuyên suốt từ LLM adapter tới application,
safety checker và history. `OllamaClient` giữ `LLMError` để báo lỗi kết nối,
timeout, response không hợp lệ hoặc response rỗng. Các tham số Ollama như
model, URL và timeout vẫn là chi tiết nội bộ của adapter, không thuộc
contract.

### Công việc đã thực hiện

- Cập nhật `LLMClient` để trả về `GeneratedCommand`.
- Đổi API của `OllamaClient` từ `generate_command()` sang `generate()`.
- Cho phép contract nhận context tùy chọn vì SRS có yêu cầu `FR-09`.
- Đổi `CommandService` sang phụ thuộc `LLMClient` thay vì phụ thuộc trực tiếp
  vào `OllamaClient`.
- Cập nhật contract tests, Ollama tests và application tests.
- Export `GeneratedCommand` và `LLMClient` từ `ezcli.llm`.
- Giữ lại `result.py` như phần mã đã có, nhưng không còn là public contract
  của Sprint 1.

### Kết quả mong đợi

Luồng chính sau khi thực hiện lại:

```text
prompt + context
    -> LLMClient.generate()
    -> GeneratedCommand
    -> safety checking
    -> confirmation/execution
    -> history
```

Luồng lỗi từ Ollama vẫn được báo bằng `LLMError`, để application/TUI có thể
hiển thị lỗi và không thực thi command khi LLM không khả dụng.


# 15/10/2026 Triển khai adapter Ollama /api/chat

### Đã thực hiện

- Chuyển `OllamaClient` từ `/api/generate` sang `POST /api/chat`.
- Gửi request theo định dạng `messages` của Ollama với `stream: false`.
- Ánh xạ `message.content` thành `LLMResult(success=True, content=...)`.
- Chuẩn hóa lỗi HTTP, mạng, timeout, JSON không hợp lệ và response sai cấu
  trúc thành `LLMResult(success=False, content="", error=...)`.
- Giữ timeout mặc định 30 giây và cho phép thay đổi qua
  `OllamaClient(timeout=...)`.
- Cập nhật `LLMClient` contract và application để chỉ kiểm tra safety khi
  `LLMResult.success` là `True`.
- Cập nhật unit tests dùng mock, không phụ thuộc Ollama đang chạy.

### Kết quả kiểm chứng

Các lệnh sau đã chạy thành công:

```text
uv run ruff check src tests
All checks passed!

uv run mypy
Success: no issues found in 22 source files

uv run pytest
34 passed in 0.31s
```

Đã kiểm thử tích hợp với Ollama thật bằng model `qwen2.5-coder:3b`. Endpoint
`/api/chat` phản hồi thành công với `message.role=assistant` và
`message.content`, xác nhận đường đi thành công của adapter.

### Lưu ý sau kiểm thử tích hợp

- Model có thể trả command trong Markdown code fence, ví dụ
  ```` ```bash ... ``` ```` thay vì chỉ trả command thuần. Adapter hiện ánh xạ
  đúng `message.content`, nhưng output cần được chuẩn hóa trước khi thực thi
  thật.
- System message nên tiếp tục yêu cầu model trả về duy nhất Bash command;
  đồng thời cần cân nhắc bước loại bỏ code fence trước safety check. Command
  vẫn phải đi qua safety check trước khi được thực thi.
- Timeout hiện được cấu hình qua constructor, ví dụ
  `OllamaClient(timeout=60.0)`. Timeout mặc định vẫn là 30 giây. Nếu cần cấu
  hình từ biến môi trường hoặc file cấu hình, đó sẽ là công việc mở rộng tiếp
  theo.
- Kiểm thử tích hợp xác nhận kết nối và ánh xạ response, nhưng không thay thế
  cho unit tests vì phụ thuộc vào Ollama, model và tài nguyên máy.

