# plan cho sprint 1

[plan](https://chatgpt.com/s/t_6ac8bb9786ac81918a563724d69641ad)

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
    ) -> GeneratedCommand:
        ...
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
