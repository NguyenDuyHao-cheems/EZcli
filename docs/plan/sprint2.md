# plan cho sprint 2

[plan](https://app.notion.com/p/print-2-3fb408fa796680edbe42d76e4b88dd4e)

## Tổng kết công việc đã thực hiện

### Implement NL-to-Bash Pipeline

Đã xây dựng và kiểm tra luồng nhận yêu cầu bằng ngôn ngữ tự nhiên, gửi tới
Ollama và trả về Bash command để các lớp phía trên sử dụng.

Các công việc đã hoàn thành:

1. **Kiểm tra interface LLM**
   - Xác nhận `LLMClient.generate(prompt, context)` là contract phù hợp cho
     pipeline.
   - Giữ nguyên `LLMResult` làm kiểu kết quả chuẩn cho cả thành công và thất
     bại.
   - Đảm bảo `CommandService` có thể sử dụng client thật hoặc mock client.

2. **Xây dựng prompt template**
   - Tách prompt dành cho Bash command vào module
     `src/ezcli/llm/prompts.py`.
   - Prompt yêu cầu mô hình `qwen2.5-coder:3b` trả về đúng một Bash command.
   - Không cho phép output chứa Markdown, giải thích hoặc nhãn bao quanh
     command.
   - Context của môi trường được truyền vào prompt dưới dạng dữ liệu thông tin.

3. **Xử lý đầu ra và lỗi LLM**
   - Xử lý lỗi HTTP, timeout, lỗi kết nối và JSON không hợp lệ.
   - Xử lý response thiếu `message` hoặc có cấu trúc không đúng.
   - Xử lý output rỗng, chỉ chứa khoảng trắng hoặc có kiểu dữ liệu không hợp lệ.
   - Từ chối output nhiều dòng hoặc output được bọc trong Markdown code fence.
   - Xử lý lỗi do Ollama trả về trong JSON dù request HTTP thành công.
   - Các lỗi đều trả về `LLMResult` thất bại với `content` rỗng và thông báo lỗi
     rõ ràng.

4. **Bổ sung unit test bằng mock**
   - Bổ sung test mock cho response thành công, lỗi provider, output sai kiểu,
     output nhiều dòng và output chứa Markdown.
   - Các test Ollama không cần kết nối tới server thật.
   - Kiểm tra contract giữa `LLMClient`, `LLMResult` và `OllamaClient`.

5. **Đảm bảo không tự động thực thi command**
   - `OllamaClient` chỉ gửi request và trả về kết quả.
   - `CommandService.prepare_command()` chỉ tạo command và kiểm tra safety.
   - Bổ sung test xác nhận `execute_command` không được gọi trong bước chuẩn bị
     command.
   - Việc thực thi chỉ được thực hiện ở bước riêng khi có xác nhận rõ ràng từ
     người dùng.

### Kết quả kiểm thử

- Ruff: đạt, không còn lỗi lint.
- Unit test liên quan đến LLM, application và execution: `45 passed`.
