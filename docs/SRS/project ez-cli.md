[[Project Công nghệ phần mềm]]
##  vấn đề
- các lệnh trong cli nhiều, khó nhớ. Mỗi lệnh lại có các tham số, cấu trúc, cờ khác nhau dẫn đến người dùng thường phải hỏi AI hoặc tự tìm tài liệu để đọc.
- người dùng muốn xài cli tiện phải tự setup công cụ, sửa file config, backup file v.v. học phím tắt
### stakeholder
**người dùng non-tech**5

**dev**

**agent**

**giảng viên**-client

**người lập trình ezcli**



## giải pháp
- sử dụng modell llm để ngưởi dùng có thể dùng nntn đưa ra yêu cầu rồi model sẽ trả về câu lệnh + giải thích

## FR
```
sgpt --shell "find all json files in current folder"
# -> find . -type f -name "*.json"
# -> [E]xecute, [D]escribe, [A]bort: e
`
```
- nhận input nlp -> command + explain (optional)
- tiếp tục hỏi về câu lệnh nếu exp chưa rõ
- tính năng common use case kế thừa tldr
- tính năng tra cứu sử dụng `curl cheat.sh/command`
- gợi ý lệnh mờ trong quá khứ kế thừa fzf
- autosuggestion autocompletion kế thừa zsh-autosuggest
- hỗ trợ alias tự động và quản lí alias
- 
## NFR
- xác nhận trước khi thực thi 
- bảo mật riêng tư lịch sử lệnh
- cross-platform, sp đa dạng shell
- câu lệnh sinh ra chính xác không bị hallucination
- tốc độ sinh nhanh dưới 1s
	-  tách sinh lệnh và sinh explain (chỉ sinh khi user yêu cầu )
	- lưu cache
- lazy import skill/ docs của câu lệnh
- know the state of user (OS, shell)
	- cho phép người dùng tùy chọn đính kèm ngữ cảnh (OS, shell, cur dir, quyền hiện tại, các tệp trong dir)
	- cơ chế hỗ trợ user cài đặt các công cụ còn thiếu trong lệnh hoặc chuyển sang công cụ hiện có
	- duy trì bộ nhớ phiên làm việc (3-5 câu lệnh + output trước đó)
- hightlight syntax
- local-first
- an toàn 
	- hightlight warning tuy mức độ, phân tích cú pháp tĩnh
	- sử dụng rag + kho dữ liệu có sẵn tldr-pages/cheat.sh
	- chạy dry run
- 
	
## So sánh với các solution khác
### hỏi ai model rồi copy paste 

| citeria  | ezcli              | ai                 |
| -------- | ------------------ | ------------------ |
| tích hợp | tích hợp vào shell | phải chuyển cửa sổ |
| tốc độ   | nhanh              | chậm               |
|          |                    |                    |
|          |                    |                    |
### gh copilot

| citeria  | ezcli          | gh copilot                                      |
| -------- | -------------- | ----------------------------------------------- |
| cost     | self-host free | paid api                                        |
| speed    | nhanh          | 1-2s                                            |
| tích hợp | tại shell      | trả về câu lệnh -> phải copy -> paste vào shell |


| citeria | ezcli | gh copilot |
| ------- | ----- | ---------- |
|         |       |            |
### warp terminal
- chỉ sử dụng openai api compatible (so local/private IPs (like localhost:11434 for Ollama) still fail)
- không fully local, vẫn đi qua server warp
### shell_gpt
**is not optimized for local models and may not work as expected.**
### thefuck
- phải gõ lệnh sai rồi ms sửa
- tự động chạy lệnh đã sửa
### lazygit
- bó hẹp trong phạm vi git 
- tui
- 

---
## triết lí
> đẹp như warp xịn như shell_gpt
> local-first

### khó khăn
- an toàn khó khi AI sinh ảo giác, lệnh kh tồn tại hoặc lệnh nguy hiểm -> hightlight warning tuy mức độ, phân tích cú pháp tĩnh
	- sử dụng rag + kho dữ liệu có sẵn tldr-pages/cheat.sh
	- 
- độ trễ cao nếu dùng model kh phù hợp -> finetune model 4b, chuyển sang precision 4bit 
	- tách sinh lệnh và sinh explain (chỉ sinh khi user yêu cầu )
	- lưu cache
	
## backlog nice to have
### fr1-hỗ trợ api model cloud như openai
- **Tầng lọc và làm sạch dữ liệu tự động trước khi gửi:** Tích hợp bộ quét biểu thức chính quy và nhận diện thực thể ngay tại máy khách. Toàn bộ các chuỗi có định dạng mã khóa bảo mật, mật khẩu trong chuỗi kết nối, địa chỉ IP mạng nội bộ hay đường dẫn chứa tên người dùng thực sẽ bị thay thế bằng các giá trị giả lập trước khi dữ liệu rời khỏi máy tính.
    
- **Chính sách ưu tiên xử lý nội bộ:** Thiết lập chế độ mặc định xử lý hoàn toàn ngoại tuyến trên máy người dùng. Hệ thống chỉ cho phép gửi yêu cầu lên các dịch vụ đám mây khi người dùng chủ động bật tính năng này cho các yêu cầu phức tạp, đi kèm thông báo rõ ràng về các gói tin chuẩn bị được gửi đi.
    
- **Giao thức không lưu vết với nhà cung cấp dịch vụ:** Cấu hình các kết nối đám mây thông qua các đầu mối dịch vụ có cam kết không lưu trữ dữ liệu truyền tải để phục vụ huấn luyện mô hình, đồng thời hủy bỏ toàn bộ phiên làm việc ngay sau khi trả lời hoàn tất.
- **routing** giữa model local và cloud 
- nén context
### fr2-tích hợp sâu bằng hotkey
### fr3-sửa lỗi thông minh

---
## inbox
- jc mayhelp 
