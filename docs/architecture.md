# Kiến trúc EZcli

## Mục đích

EZcli được tổ chức theo các module có trách nhiệm tương đối độc lập. TUI là
điểm tương tác với người dùng, còn các xử lý nghiệp vụ như sinh command, kiểm
tra an toàn, thực thi và lưu lịch sử được tách ra để dễ kiểm thử và thay thế.

Kiến trúc này phù hợp với hướng phát triển local-first của dự án: adapter
Ollama có thể được thay đổi mà không cần đưa chi tiết giao tiếp với LLM vào
domain hoặc giao diện người dùng.

## Phân vùng của repository

Repository được chia thành các vùng có mục đích ổn định. Cây dưới đây mang
tính khái niệm, không phải danh sách bắt buộc của mọi file hoặc package. Có thể
thêm, đổi tên hoặc tổ chức lại file bên trong mỗi vùng mà không cần cập nhật
tài liệu này.

```text
EZcli/
├── .github/                  # Tự động hóa và quy trình cộng tác
├── docs/                     # Tài liệu sản phẩm và tài liệu kỹ thuật
├── src/                      # Mã nguồn ứng dụng
├── tests/                    # Kiểm thử tự động
└── các file cấu hình root    # Package, dependency, công cụ và quy trình
```

Các thư mục môi trường, file build và cache được tạo trong quá trình phát triển
không thuộc kiến trúc sản phẩm và không nên được commit vào repository.

### `.github/`

Chứa cấu hình hỗ trợ quy trình cộng tác trên GitHub, chẳng hạn mẫu issue,
workflow kiểm tra chất lượng và workflow xây dựng hoặc triển khai tài liệu.

### `docs/`

Chứa tài liệu dành cho người dùng, người đánh giá và nhóm phát triển. Tài liệu
được chia theo các nhóm như giới thiệu sản phẩm, kiến trúc, yêu cầu phần mềm
và kế hoạch triển khai. Có thể bổ sung hoặc sắp xếp lại các trang trong `docs/`
mà không làm thay đổi kiến trúc runtime của ứng dụng.

### `src/`

Chứa package Python của sản phẩm. Đây là vùng chứa mã nguồn runtime; các chi
tiết package bên trong được trình bày ở phần **Cấu trúc mã nguồn** theo các
trách nhiệm kiến trúc, không theo từng file cụ thể.

### `tests/`

Chứa test tự động cho domain, use case, adapter và các workflow quan trọng.
Test có thể được chia thành unit test, integration test hoặc các nhóm khác
tùy nhu cầu, nhưng không nên làm thay đổi ranh giới của mã nguồn sản phẩm.

### Các file cấu hình ở root

Các file ở root cấu hình package, dependency, công cụ chất lượng, tài liệu và
quy trình cộng tác. Tên hoặc số lượng file có thể thay đổi theo công cụ được
sử dụng; điều quan trọng là chúng phục vụ việc phát triển, kiểm thử, đóng gói
hoặc xuất bản tài liệu, không chứa logic nghiệp vụ chính.

## Cấu trúc mã nguồn

Sơ đồ sau mô tả các vùng trách nhiệm hiện tại ở mức khái niệm:

```text
src/ezcli/
├── application/  # Điều phối use case
├── domain/       # Khái niệm và quy tắc nghiệp vụ
├── context/      # Context của môi trường
├── llm/          # Giao tiếp với mô hình ngôn ngữ
├── safety/       # Phân tích rủi ro
├── execution/    # Thực thi command
├── history/      # Lịch sử thao tác
└── tui/          # Tương tác với người dùng
```

Tên package có thể được tách, gộp hoặc đổi tên khi thiết kế thay đổi. Điều cần
được bảo toàn là các trách nhiệm và ranh giới tương ứng: giao diện không chứa
nghiệp vụ cốt lõi, adapter bên ngoài không lan vào domain, và các use case
được điều phối ở một lớp phù hợp.

## Vai trò của từng lớp

### `tui`

Chịu trách nhiệm hiển thị giao diện và tiếp nhận thao tác của người dùng. TUI
không nên tự cài đặt logic phân tích rủi ro hoặc logic giao tiếp với Ollama.
Entry point của ứng dụng gọi TUI thông qua lệnh `ezcli`.

### `application`

Chứa các use case và điều phối workflow. Lớp này kết nối request từ TUI với
context collector, LLM client, safety checker, command executor và history
repository.

### `domain`

Chứa các khái niệm cốt lõi không phụ thuộc vào framework hoặc runtime cụ thể.
Một số model hiện có gồm:

- `CommandRequest`: yêu cầu tự nhiên của người dùng.
- `GeneratedCommand`: command được sinh và phần giải thích.
- `SafetyResult`: kết quả kiểm tra an toàn.
- `HistoryEntry`: một lần thao tác được lưu trong lịch sử.
- `SafetyLevel`: `safe`, `warning` hoặc `blocked`.
- `ExecutionStatus`: trạng thái của lần thực thi.

Domain nên giữ các kiểu dữ liệu và quy tắc cần thiết cho nghiệp vụ, không nên
biết chi tiết về Textual, Typer, Ollama hoặc cách lưu trữ cụ thể.

### `context`

Thu thập thông tin liên quan đến môi trường hiện tại, chẳng hạn shell, thư mục
làm việc hoặc các thông tin cần thiết khác. Context được truyền vào LLM dưới
dạng phù hợp thay vì để LLM tự đoán môi trường.

### `llm`

Định nghĩa giao diện cho client sinh command và biểu diễn kết quả trả về.
Module này là ranh giới giữa ứng dụng và một runtime LLM cụ thể. Ollama là
hướng tích hợp chính, còn mock client hỗ trợ phát triển và kiểm thử mà không
cần chạy model thật.

### `safety`

Phân tích command bằng các rule đã định nghĩa và trả về mức độ an toàn cùng
các lý do tương ứng. Module này có thể đưa ra ba kết quả chính:

- `safe`: chưa phát hiện mẫu rủi ro đã biết.
- `warning`: có rủi ro cần người dùng xem xét.
- `blocked`: không cho phép tiếp tục thực thi theo rule.

Safety checker là lớp phòng thủ, không phải bằng chứng rằng command hoàn toàn
an toàn.

### `execution`

Chịu trách nhiệm thực thi command sau khi workflow đã kiểm tra và nhận được
xác nhận hợp lệ từ người dùng. Kết quả cần bao gồm trạng thái, output hoặc lỗi
và exit code khi có thể.

### `history`

Lưu lại request, command, thời điểm, mức độ an toàn, trạng thái và exit code.
Việc lưu trữ được giữ ở máy cục bộ theo định hướng local-first.

## Luồng phụ thuộc

Luồng tương tác chính được định hướng như sau:

```text
TUI
 |
 v
Application
 |------> Context
 |------> LLM client
 |------> Safety checker
 |------> Command executor
 └------> History repository
              |
              v
           Domain
```

Mũi tên thể hiện quan hệ sử dụng ở mức khái niệm. Domain là nền tảng chung,
còn application điều phối các thành phần. TUI không nên gọi trực tiếp Ollama
hoặc thực thi shell command để tránh làm trộn logic giao diện với logic
nghiệp vụ.

## Luồng xử lý command

1. TUI nhận một `CommandRequest`.
2. Application yêu cầu `context` thu thập thông tin môi trường cần thiết.
3. Application gọi `LLMClient` để sinh `GeneratedCommand`.
4. Safety checker phân tích command và tạo `SafetyResult`.
5. TUI hiển thị command, giải thích, cảnh báo và yêu cầu xác nhận.
6. Nếu kết quả là `blocked` hoặc người dùng từ chối, command không được thực
   thi; trạng thái tương ứng có thể được lưu vào history.
7. Nếu được xác nhận, execution thực thi command và trả về kết quả.
8. Application tạo `HistoryEntry` và chuyển cho history component lưu cục bộ.

Mọi lỗi từ LLM, safety checker, executor hoặc history cần được biểu diễn rõ
cho application và TUI. Không nên biến lỗi thành kết quả thành công giả hoặc
âm thầm bỏ qua lỗi.

## Ranh giới và nguyên tắc mở rộng

- Dùng `Protocol` hoặc interface ở các ranh giới như LLM, execution và history
  để có thể thay adapter mà không đổi use case.
- Giữ dependency hướng vào domain và application; framework chỉ nằm ở lớp ngoài.
- Dùng mock cho LLM và các thành phần bên ngoài trong unit test.
- Không đưa cloud API, remote execution hoặc arbitrary shell vào MVP.
- Khi thêm shell hoặc hệ điều hành mới, cần xác định rõ phạm vi hỗ trợ thay vì
  giả định Bash behavior áp dụng ở mọi nơi.

## Liên hệ với tài liệu yêu cầu

Kiến trúc này hiện thực hóa các mục tiêu trong
[đề xuất dự án](SRS/PA01_Nhom09_ProjectProposal.md), đặc biệt là local LLM,
kiểm tra safety rule, xác nhận trước khi execute và lưu history cục bộ. Khi
kiến trúc thay đổi đáng kể, tài liệu yêu cầu và kế hoạch sprint cũng cần được
cập nhật để giữ tài liệu nhất quán với code.
