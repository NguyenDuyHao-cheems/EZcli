# PROJECT PROPOSAL

> **Môn học:** Nhập môn Công nghệ Phần mềm
>
> **Đơn vị:** Bộ môn Công nghệ Phần mềm – Khoa Công nghệ Thông tin, Trường Đại học Khoa học Tự nhiên, ĐHQG-HCM
>
> **Tên đề tài:** EZcli
>
> **Mã nhóm / Lớp:** Nhóm 09 - 2024/3
>
> **Giảng viên hướng dẫn:** TS.Ngô Ngọc Đăng Khoa

## 1. THÔNG TIN DỰ ÁN & ĐÁNH GIÁ THÀNH VIÊN

### 1.1. Danh sách thành viên & Phân công vai trò

| STT | MSSV     | Họ và Tên              | Vai trò chính trong dự án                                      | % Đóng góp dự kiến |     |
| --- | -------- | ---------------------- | -------------------------------------------------------------- | ------------------ | --- |
| 1   | 24120306 | **Nguyễn Duy Hào**     | **Trưởng nhóm**                                                | 100%               |     |
| 2   | 24120304 | **Trần Thị Bích Hạnh** | Điều phối dự án (Scrum Master)                                 | 100%               |     |
| 3   | 24120299 | **Nguyễn Thị Ngọc Hà** | Trưởng nhóm Giao diện (Frontend Lead) / Thiết kế UI-UX         | 100%               |     |
| 4   | 24120044 | **Bùi Thị Thùy Dương** | Quản lý chất lượng & Kiểm thử (QA/QC) / Lập trình viên Backend | 100%               |     |

## 2. PHÁT BIỂU BÀI TOÁN & PHẠM VI DỰ ÁN

### 2.1. Bối cảnh & Phát biểu bài toán sơ lược

* **Bối cảnh thực tế:** Giao diện dòng lệnh (CLI) là công cụ làm việc thiết yếu nhưng số lượng câu lệnh quá lớn, cấu trúc tham số và các cờ tùy chọn phức tạp, không đồng nhất giữa các hệ điều hành.

* **Vấn đề tồn đọng:**

  * *Vấn đề 1:* Người dùng thường xuyên phải rời khỏi cửa sổ dòng lệnh để tra cứu tài liệu hoặc hỏi AI trên trình duyệt web, gây gián đoạn mạch làm việc.

  * *Vấn đề 2:* Việc thiết lập các công cụ hỗ trợ gợi ý lệnh thủ công đòi hỏi kỹ năng cấu hình phức tạp, dễ gây lỗi hệ thống.

* **Mục tiêu dự án:** Xây dựng ứng dụng dòng lệnh ezcli tích hợp mô hình ngôn ngữ xử lý trực tiếp tại máy tính cá nhân, chuyển đổi yêu cầu ngôn ngữ tự nhiên thành câu lệnh chính xác, an toàn và tức thì.

### 2.2. Stakeholder

| Mã đối tượng | Bên liên quan | Vai trò trong hệ thống | Nhu cầu chính & Kỳ vọng | Mức độ ảnh hưởng |
| ----- | ----- | ----- | ----- | ----- |
| `STK-01` | Người dùng ít kinh nghiệm | Người dùng cuối | Chuyển đổi mô tả công việc thông thường thành lệnh CLI chính xác mà không cần nhớ cú pháp. | Rất cao |
| `STK-02` | Lập trình viên | Người dùng nâng cao | Tăng tốc độ thao tác, gợi ý cú pháp phức tạp, tìm kiếm mờ lịch sử lệnh và hỗ trợ quản lý bí danh. | Rất cao |
| `STK-03` | Giảng viên hướng dẫn | Khách hàng đánh giá | Nghiệm thu độ hoàn thiện đồ án, tính thực tiễn và tính chuẩn mực kỹ thuật trong tài liệu. | Cao |
| `STK-04` | Nhóm phát triển ezcli | Đội ngũ kỹ thuật | Làm chủ mã nguồn, tối ưu hóa mô hình cục bộ đạt tốc độ phản hồi cao và đảm bảo an toàn thực thi. | Trung bình |

### 2.3. Phạm vi dự án

* **Nội dung trong phạm vi phát triển:**

  * Sinh câu lệnh từ văn bản tự nhiên kèm giải thích tùy chọn.
  * Cơ chế xác thực trước khi chạy.
  * Gợi ý lệnh mờ.
  * Hỗ trợ sử dụng mô hình cục bộ qua ollama.

* **Nội dung nằm ngoài phạm vi phát triển:**

  * Tự động chuyển hướng yêu cầu lên các mô hình điện toán đám mây trả phí.

  * Đăng ký phím tắt toàn cục trên hệ điều hành.

  * Trình nền tự động giám sát và sửa lỗi ngầm sau khi lệnh thực thi thất bại.

### 2.4. Bảng thuật ngữ nghiệp vụ & Từ viết tắt

| Thuật ngữ / Viết tắt | Giải nghĩa chi tiết trong ngữ cảnh đề tài |
| ----- | ----- |
| `SRS` | Đặc tả yêu cầu phần mềm (Software Requirements Specification) |
| `CLI` | Giao diện dòng lệnh (Command-Line Interface) - Giao diện cho phép người dùng tương tác với hệ điều hành thông qua các dòng lệnh văn bản. |
| `Shell` | Chương trình phân giải lệnh của hệ điều hành, tiếp nhận lệnh từ người dùng (qua CLI) và gửi tới hệ điều hành để thực thi. |
| `LLM cục bộ` | Mô hình ngôn ngữ lớn (Large Language Model) được tối ưu để chạy trực tiếp trên máy tính cá nhân (local) thay vì trên máy chủ đám mây. |
| `Phân tích cú pháp tĩnh` | Kỹ thuật kiểm tra chuỗi lệnh sinh ra mà không cần thực thi chúng, nhằm phát hiện lỗi hoặc cảnh báo các lệnh có tính phá hoại/nguy hiểm. |
| `Bí danh` | Tên viết tắt hoặc từ khóa đại diện (Alias) cho một lệnh hay một chuỗi lệnh phức tạp trong môi trường dòng lệnh. |
| `DoD` | Tiêu chí hoàn thành cho từng hạng mục công việc (Definition of Done) |

## 3. SO SÁNH & ĐÁNH GIÁ CÁC GIẢI PHÁP HIỆN TẠI

### 3.1. Tổng quan các giải pháp hiện hành trên thị trường

* **Giải pháp thủ công / Bán tự động:**
  * **Tra cứu lệnh bằng tài liệu trên mạng hoặc hỏi AI**
    * Khi gặp các câu lệnh phức tạp hoặc ít sử dụng, người dùng thường phải rời khỏi cửa sổ dòng lệnh (Terminal) để tra cứu trên Google, Stack Overflow hoặc dùng các công cụ AI (như ChatGPT, Claude) để tìm kiếm. Điều này này làm gián đoạn mạch làm việc của họ, tốn thời gian copy-paste câu lệnh qua lại, đồng thời tiềm ẩn rủi ro lộ dữ liệu nhạy cảm khi sao chép các lệnh chứa đường dẫn hay thông số hệ thống nội bộ lên đám mây.
   * **Cấu hình gợi ý lệnh mờ**
     * Người dùng cài đặt công cụ bên thứ ba như fzf để tìm kiếm chuỗi lệnh gần đúng. Mặc dù hỗ trợ tìm lại câu lệnh nhanh hơn, công cụ này chỉ hoạt động trên các lệnh đã từng gõ trong quá khứ, hoàn toàn không thể hỗ trợ sinh lệnh mới.

  * **Tạo và quản lý bí danh**
    * Người dùng tự định nghĩa các chuỗi viết tắt cho câu lệnh dài trong tệp cấu hình (.bashrc, .zshrc). Cách này đòi hỏi kỹ năng cấu hình thủ công phức tạp, khó bảo trì/đồng bộ khi danh sách bí danh lớn dần, và người dùng vẫn phải tự nhớ danh sách các bí danh mà mình đã thiết lập.
  * **Tìm trong lịch sử lệnh đã gõ**
    *  Người dùng dựa vào tính năng tra cứu lịch sử mặc định của Shell hoặc các plugin gợi ý. Nhược điểm lớn là dữ liệu lịch sử dễ bị trôi, mất mát khi chuyển đổi môi trường làm việc, tốn thời gian lọc hàng ngàn lệnh cũ và gặp nhiều khó khăn nếu gặp tác vụ chưa từng thực hiện được trước đó.  
* **Giải pháp thương mại đóng gói sẵn:**
  * **Warp Terminal:** ứng dụng GUI hỗ trợ chat với AI và gõ lệnh trực tiếp trong giao diện.
    * Trình giả lập thiết bị đầu cuối thế hệ mới tích hợp trợ lý AI. Mặc dù mang lại trải nghiệm tốt cho người dùng khi họ có thể gõ lệnh trực tiếp, nhưng Warp lại yêu cầu kết nối mạng, toàn bộ luồng dữ liệu/truy vấn bắt buộc phải đi qua máy chủ trung gian của Warp (kể cả khi kết nối tới các mô hình AI cục bộ như Ollama/localhost), dẫn đến rủi ro về quyền riêng tư và chi phí duy trì dịch vụ.
  * **Shell GPT:** tích hợp lệnh `sgpt` và cờ `-s` hỗ trợ gợi ý lệnh bằng ngôn ngữ tự nhiên.
    * *Công cụ dòng lệnh* hỗ trợ sinh lệnh và giải thích thông qua tham số (ví dụ: sgpt --shell). Điểm hạn chế của Shell GPT là chưa tối ưu tốt cho các mô hình chạy cục bộ (local models), đồng thời người dùng vẫn phải nhớ các cờ/cú pháp của chính lệnh đó.
### 3.2. Bảng phân tích so sánh chi tiết

| Tiêu chí so sánh | Hỏi AI trên trình duyệt | Shell GPT (shell_gpt) | Warp Terminal | Giải pháp ezcli đề xuất |
| ----- | ----- | ----- | ----- | ----- |
| **Tính tích hợp** | Kém (phải chuyển qua lại giữa các cửa sổ) | Tốt (có thể gọi lệnh `sgpt` trực tiếp ngay trong shell) | Tốt (tích hợp trong trình giả lập thiết bị đầu cuối) | Tốt (tích hợp gõ lệnh trực tiếp trong ứng dụng) |
| **Chi phí vận hành** | Miễn phí hoặc mua gói | Tiết kiệm / Miễn phí (hỗ trợ mô hình cục bộ / local model hoặc API cá nhân) | Phụ thuộc gói dịch vụ đám mây hoặc mô hình cục bộ nhưng dữ liệu phải đi qua server của **Warp**| Hoàn toàn miễn phí (tự lưu trữ cục bộ) |
| **Tốc độ phản hồi** | Chậm (độ trễ mạng cao) | Nhanh (khi chạy với mô hình cục bộ hoặc gọi API) | Phụ thuộc máy chủ dịch vụ | Nhanh ($\le 1$ giây với mô hình nén cục bộ) |
| **Bảo mật dữ liệu** | Kém (dữ liệu gửi lên máy chủ bên thứ ba) | Cao (hỗ trợ xử lý hoàn toàn cục bộ / local, không gửi dữ liệu ra ngoài) | Dữ liệu phải đi qua server của Warp dù chạy cục bộ | Tốt (xử lý cục bộ, không rò rỉ dữ liệu ra ngoài) |
| **An toàn thực thi** | Có nhắc nhở người dùng nhưng không đảm bảo hoàn toàn vì không có thông tin máy ngươi dùng | Tốt (có cơ chế hỏi xác nhận trước khi chạy và hỗ trợ giải thích lệnh) | Cảnh báo cơ bản | Phân tích cú pháp tĩnh và xác nhận trước khi chạy |
| **Độ thân thiện (UX)** | Trung bình (giao diện web trực quan nhưng gây đứt gãy thao tác) | Thấp (người dùng phải cài đặt thủ công shell_gpt, phải nhớ các tham số và câu lệnh để sử dụng, chỉ là lệnh trong shell không phải giao diện thân thiện) | Cao (giao diện terminal đồ họa hiện đại, trực quan) | Cao (giao diện tương tác trực quan, gợi ý thông minh, thao tác tiện lợi mà không cần nhớ cú pháp) |

### 3.3. Điểm khác biệt & Lợi thế cạnh tranh của giải pháp đề xuất

* **Hoạt động ngoại tuyến & tự chủ hoàn toàn:** EZcli được thiết kế để xử lý các chức năng chính trực tiếp trên thiết bị của người dùng, không phụ thuộc vào kết nối Internet. Nhờ đó, người dùng vẫn có thể sử dụng công cụ khi mất mạng hoặc làm việc trong môi trường hạn chế kết nối. Việc sử dụng mô hình và dữ liệu được lưu trữ cục bộ cũng giúp giảm sự phụ thuộc vào các dịch vụ API bên ngoài và không phát sinh chi phí sử dụng API theo từng yêu cầu.

* **Không rò rỉ dữ liệu:** Toàn bộ quá trình xử lý yêu cầu ngôn ngữ tự nhiên và sinh câu lệnh được thực hiện cục bộ trên máy tính của người dùng. Các thông tin liên quan đến môi trường làm việc như đường dẫn thư mục, tên người dùng, hệ điều hành, shell và lịch sử câu lệnh không cần gửi lên máy chủ bên thứ ba. Điều này giúp hạn chế nguy cơ dữ liệu nhạy cảm bị truyền ra ngoài.

* **Chủ động phân tích trước khi chạy:** EZcli không chỉ chuyển đổi yêu cầu bằng ngôn ngữ tự nhiên thành câu lệnh mà còn thực hiện phân tích cú pháp và kiểm tra an toàn trước khi cho phép thực thi. Hệ thống có thể đưa ra cảnh báo đối với những câu lệnh có khả năng gây ảnh hưởng đến dữ liệu hoặc hệ thống. Người dùng được cung cấp các lựa chọn để xem giải thích, xác nhận thực thi hoặc hủy thao tác, qua đó giảm nguy cơ thực hiện nhầm các câu lệnh không mong muốn.

* **Giao diện trực quan & tối ưu trải nghiệm người dùng:** EZcli được thiết kế với giao diện dòng lệnh trực quan, sử dụng màu sắc, syntax highlighting, thông báo và cảnh báo rõ ràng để giúp người dùng dễ theo dõi kết quả. Các chức năng như gợi ý câu lệnh, tìm kiếm lịch sử và quản lý bí danh giúp giảm số thao tác phải thực hiện thủ công, đồng thời hạn chế việc người dùng phải *tự tùy biến* terminal quá nhiều để có được trải nghiệm thuận tiện.

## 4. GIẢI PHÁP ĐỀ XUẤT & ĐẶC TẢ YÊU CẦU PHẦN MỀM (SRS)

### 4.1. Bảng câu chuyện người dùng

| Nhu cầu của bên liên quan                                                                             | Yêu cầu hệ thống giải quyết tương ứng               |     |
| ----------------------------------------------------------------------------------------------------- | --------------------------------------------------- | --- |
| Là **người dùng không chuyên về công nghệ**, tôi muốn được gợi ý lệnh để không phải nhớ lệnh.         | Gợi ý lệnh bằng ngôn ngữ tự nhiên `FR-01` & `FR-02` |     |
| Là **Lập trình viên**, tôi muốn 1 phần mềm được cấu hình sẵn từ đầu, không phải mất công tự tùy biến. | `NFR-04`                                            |     |
| Là **Lập trình viên**, tôi muốn sử dụng được mô hình llm cục bộ để không phải trả tiền API.           | `Fr-01` và `NFR-02`                                 |     |
| Là **Người dùng chung**, tôi muốn thời gian xử lý nhanh và dữ liệu được bảo vệ an toàn.               | `NFR-02`và `NFR-01`                                 |     |

### 4.2. Danh mục yêu cầu chức năng (FR)

| Mã yêu cầu | Tên chức năng                  | Mô tả chi tiết hành vi của hệ thống                                                                          | Mức ưu tiên | Nguồn gốc      | Tiêu chí nghiệm thu                                                            |     |
| ---------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------ | ----------- | -------------- | ------------------------------------------------------------------------------ | --- |
| `FR-01`    | Sinh lệnh từ ngôn ngữ tự nhiên | Tiếp nhận chuỗi văn bản mô tả và sinh ra câu lệnh tương ứng.                                                 | Must Have   | STK-01, STK-02 | Sinh đúng câu lệnh thực thi hợp lệ theo môi trường hiện tại.                   |     |
| `FR-02`    | Giải thích chi tiết câu lệnh   | Phân tích cấu trúc, cờ và tham số của câu lệnh vừa sinh ra theo yêu cầu của người dùng.                      | Should Have | STK-01         | Hiển thị mô tả rõ ràng từng tham số khi người dùng chọn lệnh giải thích.       |     |
| `FR-03`    | Xác nhận trước khi thực thi    | Cung cấp ba tùy chọn bắt buộc: Thực thi, Giải thích, hoặc Hủy bỏ trước khi chạy bất kỳ lệnh nào.             | Must Have   | STK-01, STK-02 | Lệnh chỉ được chạy vào hệ thống khi người dùng xác nhận thực thi.              |     |
| `FR-04`    | Tra cứu mẫu tác vụ phổ biến    | Tìm kiếm và hiển thị các trường hợp sử dụng chuẩn thông qua tích hợp dữ liệu tldr và cheat.sh.               | Should Have | STK-02         | Trả về danh sách mẫu ví dụ tương ứng với tên lệnh tra cứu.                     |     |
| `FR-05`    | Tìm kiếm mờ lịch sử lệnh       | Tìm kiếm các lệnh từng thực hiện trong quá khứ dựa trên thuật toán so khớp mờ.                               | Should Have | STK-02         | Danh sách kết quả gợi ý đúng câu lệnh gần khớp nhất theo thời gian thực.       |     |
| `FR-06`    | Quản lý bí danh tự động        | Hỗ trợ tạo mới, chỉnh sửa và ghi nhớ các bí danh rút gọn cho các lệnh dài.                                   | Could Have  | STK-02         | Bí danh mới được áp dụng ngay lập tức vào phiên làm việc hiện tại.             |     |
| `FR-07`    | Nhận diện ngữ cảnh hệ thống    | Tự động đọc thông tin về hệ điều hành, shell đang dùng, thư mục hiện tại để tối ưu câu lệnh sinh ra.         | Must Have   | STK-04         | Câu lệnh sinh ra khớp hoàn toàn với cú pháp của hệ điều hành và shell đang mở. |     |
| `FR-08`    | Phân tích an toàn cú pháp      | Phân tích cú pháp tĩnh và tô màu cảnh báo nếu câu lệnh có nguy cơ xóa tệp hoặc can thiệp sâu quyền hệ thống. | Must Have   | STK-01, STK-04 | Hiển thị cảnh báo trực quan với các câu lệnh có khả năng gây mất mát dữ liệu.  |     |

### 4.3. Danh mục yêu cầu phi chức năng (NFR)

| Mã yêu cầu | Nhóm chất lượng        | Tiêu chí kỹ thuật định lượng                                                                                                                                          | Phương pháp kiểm chứng                                                                                                                 |     |
| ---------- | ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | --- |
| `NFR-01`   | **Hiệu năng **         | Thời gian sinh câu lệnh từ văn bản tự nhiên $\le 1.0$ giây khi chạy LLM cục bộ trên cấu hình máy tính tiêu chuẩn  (mô hình 3B tham số, máy 4GB VRAM)                  | Đo đạc tự động thời gian phản hồi (từ khi gửi yêu cầu đến khi in kết quả) bằng script kiểm thử với tập 100 câu lệnh đầu vào khác nhau. |     |
| `NFR-02`   | **Bảo mật & An toàn ** | 100% dữ liệu xử lý cục bộ không truyền ra internet. Nhận diện và cảnh báo thành công 100% các câu lệnh phá hoại (vd: `rm -rf /`, `mkfs`) bằng phân tích cú pháp tĩnh. | Chạy thử nghiệm tập 50 lệnh nguy hiểm (Malicious Dataset) để kiểm chứng cơ chế cảnh báo.                                               |     |
| `NFR-03`   | **Tương thích **       | Tỷ lệ sập ứng dụng  $\le 1\%$. Lệnh sinh ra tương thích 100% trên 3 môi trường shell mục tiêu: Bash, Zsh (Linux/macOS) và PowerShell (Windows).                       | Thực thi 200 lượt test tự động trên máy ảo của 3 hệ điều hành tương ứng để xác nhận lệnh sinh ra chạy hợp lệ, không lỗi cú pháp shell. |     |
| `NFR-04`   | **Độ thân thiện**      | Hỗ trợ theme light & dark.  Người dùng không cần phải ấn 1 chỗ nhiều lần mới tìm được giao diện mình cần.                                                             | Có nút chuyển light & dark mode. Các nút bấm không phân quá 3 cấp                                                                      |     |


### 4.4. Đặc tả kịch bản sử dụng

*Mỗi kịch bản phải làm rõ luồng chính và tối thiểu 1 luồng ngoại lệ/rẽ nhánh.*

#### Kịch bản 1: Sinh câu lệnh từ văn bản tự nhiên và lựa chọn hành động (`SC-01`)

* **Tác nhân chính:** Người dùng cuối.

* **Tiền điều kiện:** Công cụ ezcli đã được cấu hình và mô hình xử lý cục bộ đang ở trạng thái sẵn sàng.

* **Sự kiện kích hoạt:** Người dùng nhập yêu cầu bằng ngôn ngữ tự nhiên.

* **Luồng sự kiện chính:**

  1. Người dùng nhập câu lệnh yêu cầu (Ví dụ: What is the command to list file in this directory).

  2. Hệ thống thu thập ngữ cảnh làm việc hiện tại (thư mục hiện tại) và chuyển vào bộ xử lý.

  3. Hệ thống trả về câu lệnh tương ứng trên màn hình và phân tích cú pháp tĩnh.

  4. Hệ thống đưa ra menu gồm 4 lựa chọn: Thực thi [E], Sửa đổi [M], Giải thích [D], Hủy bỏ [A].

  5. Người dùng nhấn chọn phím E để thực thi.

  6. Hệ thống chuyển lệnh xuống trình bao để thực hiện và trả về kết quả cho người dùng.

* **Luồng rẽ nhánh / Ngoại lệ:**

  * *Rẽ nhánh tại bước 5 (Người dùng chọn D):* Hệ thống hiển thị bảng bóc tách ý nghĩa từng tham số của lệnh, sau đó quay lại menu ba lựa chọn.

  * *Rẽ nhánh tại bước 5 (Người dùng chọn A):* Hệ thống hủy bỏ câu lệnh và trả quyền điều khiển về dòng lệnh thông thường.
  * *Rẽ nhánh tại bước 5 (Người dùng chọn M):* cho phép người dùng sửa đổi lệnh và hiển thị lại menu lựa chọn bên dưới.
  * *Ngoại lệ tại bước 3 (Phát hiện lệnh nguy hiểm):* Hệ thống đổi màu cảnh báo nổi bật và yêu cầu xác nhận thêm một bước trước khi cho phép bấm thực thi.

* **Hậu điều kiện:** Lệnh được thực thi an toàn trên hệ thống hoặc phiên làm việc kết thúc theo lựa chọn của người dùng.

#### Kịch bản 2: Tra cứu lịch sử lệnh hoặc cấu hình bí danh mới. (`SC-02`)

* **Tác nhân chính:** Người dùng nâng cao

* **Tiền điều kiện:** Công cụ ezcli đã được cài đặt và cấu hình. Lịch sử lệnh hoặc dữ liệu cấu hình của người dùng có thể được truy cập cục bộ.

* **Sự kiện kích hoạt:** Người dùng yêu cầu tra cứu một câu lệnh đã sử dụng trước đó hoặc muốn tạo một bí danh mới cho một câu lệnh thường dùng.

* **Luồng sự kiện chính:**

  1. Người dùng mở chức năng quản lý lịch sử lệnh hoặc cấu hình bí danh của ezcli.

  2. Người dùng nhập từ khóa hoặc nội dung cần tìm kiếm trong lịch sử lệnh.

  3. Hệ thống thực hiện tìm kiếm mờ trên lịch sử câu lệnh được lưu trữ cục bộ và hiển thị các kết quả phù hợp.

  4. Người dùng lựa chọn một câu lệnh từ kết quả tìm kiếm để sử dụng hoặc tạo bí danh.

  5. Người dùng nhập tên bí danh mới và xác nhận câu lệnh tương ứng.

  6. Hệ thống kiểm tra tên bí danh và lưu cấu hình bí danh vào bộ nhớ cục bộ.

  7. Hệ thống thông báo tạo bí danh thành công và cho phép người dùng sử dụng bí danh trong các lần thao tác tiếp theo.

* **Luồng rẽ nhánh / Ngoại lệ:**

  * *Rẽ nhánh tại bước 3 (Không tìm thấy lịch sử phù hợp):* Hệ thống thông báo không tìm thấy câu lệnh tương ứng và cho phép người dùng thực hiện tìm kiếm lại với từ khóa khác.

  * *Rẽ nhánh tại bước 5 (Tên bí danh đã tồn tại):* Hệ thống thông báo tên bí danh đã được sử dụng và yêu cầu người dùng nhập tên khác hoặc xác nhận ghi đè cấu hình hiện tại.

  * *Ngoại lệ tại bước 6 (Không thể lưu cấu hình):* Hệ thống thông báo lỗi và không tạo bí danh mới nếu dữ liệu không thể được lưu trữ.
* **Hậu điều kiện:** Lịch sử lệnh được tra cứu thành công hoặc bí danh mới được lưu trữ cục bộ và sẵn sàng sử dụng cho các lần thao tác tiếp theo.

### 4.5. Kiến trúc tổng thể phần mềm & Công nghệ đề xuất

* **Mô hình kiến trúc phần mềm:**
EZcli sử dụng kiến trúc Local-first, trong đó các thành phần chính của hệ thống được thực thi trực tiếp trên máy tính của người dùng, không phụ thuộc vào máy chủ trung gian. Phù hợp với yêu cầu hoạt động ngoại tuyến, xử lý cục bộ và bảo vệ dữ liệu người dùng.

* **Công nghệ giao diện dòng lệnh (CLI/TUI):** EZcli dự kiến được xây dựng bằng Python CLI, kết hợp Rich để hỗ trợ màu sắc, cảnh báo và syntax highlighting. prompt_toolkit có thể được sử dụng để hỗ trợ nhập liệu tương tác, tự động gợi ý và phím tắt. Nhằm tạo giao diện TUI trực quan và thuận tiện hơn cho người dùng.

* **Công nghệ xử lý và mô hình AI:** liên kết với mô hình cục bộ thông qua ollama.

* **Lưu trữ dữ liệu:**
Các dữ liệu được lưu trữ cục bộ trên thiết bị. Dùng định dạng txt/json/md.

* **Giải pháp triển khai & Hạ tầng:**
EZcli được đóng gói và cài đặt trực tiếp trên máy tính của người dùng, hỗ trợ các hệ điều hành Windows, Linux và macOS.
### 4.6. Yêu cầu môi trường & Phần cứng

* **Phía Máy chủ:**

  * Không yêu cầu máy chủ.

* **Phía Người dùng (Client):**

  * Thiết bị: Máy tính cá nhân

  * Hệ điều hành: Windows, Linux hoặc macOS.

  * Shell: Bash, Zsh hoặc PowerShell.

  * CPU: Tối thiểu 4 nhân.

  * RAM: Tối thiểu 4 GB RAM trống (khuyến nghị 8 GB trở lên để mô hình hoạt động ổn định.)

  * Ổ đĩa: Tối thiểu 3 GB dung lượng trống cho chương trình, mô hình SLM và cache.
  - VRAM: 4GB (đối với macOS thì yêu cầu ram > 4GB)
  * Internet: Không bắt buộc

  * Quyền hệ thống: EZcli cần quyền phù hợp để thực thi các lệnh mà người dùng yêu cầu; các lệnh có nguy cơ ảnh hưởng hệ thống sẽ được cảnh báo và yêu cầu xác nhận trước khi thực thi.

## 5. KẾ HOẠCH PHÁT TRIỂN THEO MÔ HÌNH SCRUM

### 5.1. Thiết lập quy trình phát triển

* **Mô hình làm việc:** Nhóm áp dụng Scrum để phát triển theo từng phần nhỏ, ưu tiên các chức năng cốt lõi của ứng dụng dòng lệnh EZcli và liên tục kiểm tra sản phẩm sau mỗi Sprint.

* **Độ dài một chu kỳ (Sprint):** 02 tuần / Sprint. Mỗi Sprint phải tạo ra ít nhất một phần chức năng hoặc tài liệu có thể kiểm tra được.

* **Các buổi làm việc theo quy chuẩn Scrum:**

  * *Lập kế hoạch Sprint (Sprint Planning):* Tổ chức vào đầu mỗi Sprint để Product Owner thống nhất mục tiêu, nhóm chọn các yêu cầu có thể thực hiện và phân rã thành các task cụ thể.

  * *Họp cập nhật tiến độ (Daily Standup):* Tổ chức ngắn gọn 10-15 phút theo lịch thống nhất của nhóm. Mỗi thành viên báo cáo phần đã hoàn thành, phần tiếp theo và trở ngại cần hỗ trợ.

  * *Đánh giá kết quả Sprint (Sprint Review):* Tổ chức vào cuối Sprint để chạy thử phần chức năng đã hoàn thành, đối chiếu với tiêu chí nghiệm thu và ghi nhận phản hồi.

  * *Họp cải tiến (Sprint Retrospective):* Tổ chức sau Sprint Review để xác định điểm làm tốt, vấn đề phát sinh và biện pháp cải thiện cho Sprint tiếp theo.

* **Quản lý công việc:** Mỗi task phải liên kết với một yêu cầu `FR`, `NFR` hoặc hạng mục tài liệu, có người phụ trách, mức ưu tiên và Sprint thực hiện. Trạng thái công việc gồm `To do`, `In progress`, `Review` và `Done`.

* **Tiêu chuẩn hoàn thành cho một hạng mục công việc (DoD):**

  * Mã nguồn vượt qua kiểm tra tĩnh và được ít nhất một thành viên khác rà soát.

  * Có kiểm thử cho phần logic cốt lõi và các luồng lỗi quan trọng.

  * Chức năng chạy được trên môi trường phát triển/kiểm thử đã thống nhất, phù hợp với hệ điều hành và shell được hỗ trợ.

  * Luồng chính của EZcli được kiểm tra, bao gồm sinh lệnh, giải thích, hủy hoặc xác nhận trước khi thực thi.

  * Các lệnh có nguy cơ gây mất dữ liệu hoặc thay đổi hệ thống được cảnh báo trước khi thực thi.

  * Tài liệu liên quan và ma trận truy vết được cập nhật; không còn lỗi nghiêm trọng đã biết.

### 5.2. Lộ trình phát triển & Kế hoạch chi tiết từng Sprint

| Giai đoạn / Sprint | Thời lượng | Mục tiêu cốt lõi | Hạng mục công việc chính | Sản phẩm bàn giao dự kiến |
| ----- | ----- | ----- | ----- | ----- |
| **Sprint 0** | Tuần 1 - 2 | Chốt yêu cầu, kiến trúc và môi trường phát triển | \- Rà soát phạm vi, user story, `FR` và `NFR`  \- Chốt kiến trúc ứng dụng CLI và cơ chế sử dụng mô hình cục bộ  \- Khởi tạo kho mã nguồn, quy ước code, kiểm thử và review  \- Hoàn thiện Mini-SRS phiên bản đầu | Mini-SRS phiên bản 1.0, kiến trúc sơ bộ, kho mã nguồn và môi trường phát triển sẵn sàng |
| **Sprint 1** | Tuần 3 - 4 | Xây dựng khung EZcli và nhận diện ngữ cảnh hệ thống | \- Xây dựng giao diện dòng lệnh/tương tác  \- Tiếp nhận yêu cầu bằng ngôn ngữ tự nhiên  \- Nhận diện hệ điều hành, shell và thư mục hiện tại theo `FR-07`  \- Chuẩn bị cơ chế kết nối với mô hình xử lý cục bộ | Phiên bản có thể khởi động, nhận yêu cầu và thu thập context của môi trường hiện tại |
| **Sprint 2** | Tuần 5 - 6 | Hoàn thành luồng sinh, giải thích và xác nhận lệnh | \- Hiện thực `FR-01` sinh lệnh và `FR-02` giải thích lệnh  \- Hiện thực `FR-03` với các lựa chọn thực thi, giải thích hoặc hủy  \- Kiểm tra lệnh trước khi chuyển cho shell  \- Xử lý đầu vào không hợp lệ và lỗi từ mô hình  \- Viết unit test cho luồng chính | Phiên bản chạy được luồng từ yêu cầu tự nhiên đến kết quả thực thi hoặc hủy lệnh |
| **Sprint 3** | Tuần 7 - 8 | Hoàn thiện chức năng nâng cao và an toàn thực thi | \- Hiện thực tra cứu mẫu tác vụ theo `FR-04`  \- Tìm kiếm mờ lịch sử theo `FR-05`  \- Tạo, sửa và sử dụng bí danh theo `FR-06`  \- Phân tích cú pháp và cảnh báo lệnh nguy hiểm theo `FR-08`  \- Kiểm thử các trường hợp biên và yêu cầu thay đổi đã được chấp thuận | Phiên bản tích hợp các chức năng nâng cao, lịch sử/bí danh và cảnh báo an toàn |
| **Sprint 4** | Tuần 9 | Kiểm thử, tối ưu và đóng gói bàn giao | \- Kiểm thử tích hợp và nghiệm thu các luồng chính  \- Đo các yêu cầu `NFR-01` đến `NFR-04` trong khả năng của nhóm  \- Kiểm tra dữ liệu được lưu và xử lý cục bộ  \- Sửa lỗi, tối ưu và đóng gói ứng dụng  \- Hoàn thiện hướng dẫn sử dụng, tài liệu và báo cáo | Phiên bản EZcli hoàn chỉnh có thể cài đặt/chạy thử, bộ kiểm thử và tài liệu bàn giao |

### 5.3. Quy trình tiếp nhận & Xử lý thay đổi yêu cầu

*Khi có yêu cầu thay đổi phát sinh từ giảng viên hoặc thực tế khảo sát, nhóm thực hiện theo 4 bước sau:*

1. **Tiếp nhận & Định danh:** Ghi nhận vào biểu mẫu thay đổi (Mã `CR-xx`), mô tả rõ bối cảnh và lý do thay đổi.

2. **Phân tích tác động:** Trưởng nhóm cùng các thành viên đánh giá mức độ ảnh hưởng đến yêu cầu chức năng, cơ sở dữ liệu, giao diện và tiến độ dự án.

3. **Quyết định & Lên kế hoạch:** Nếu chấp thuận, Product Owner cập nhật mức độ ưu tiên và đưa vào danh sách công việc của Sprint tiếp theo.

4. **Cập nhật tài liệu:** Điều chỉnh trực tiếp trong tài liệu SRS, cập nhật ma trận truy vết và tăng chỉ số phiên bản tài liệu.

### 5.4. Ma trận truy vết yêu cầu

| Mã nhu cầu | Bên liên quan | Mã yêu cầu (FR/NFR) | Mã kịch bản | Mã kiểm thử | Sprint thực hiện | Mã yêu cầu thay đổi |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| `N-01` | STK-01 | `FR-01`, `FR-07`, `NFR-01` | `SC-01` | `TC-01` | Sprint 1, 2 | \- |
| `N-02` | STK-01, STK-02 | `FR-02`, `FR-03`, `FR-08`, `NFR-02` | `SC-01` | `TC-02`, `TC-04` | Sprint 2, 3 | \- |
| `N-03` | STK-02 | `FR-04`, `FR-05`, `FR-06` | `SC-02` | `TC-03`, `TC-04` | Sprint 3 | \- |
| `N-04` | STK-04 | `NFR-03`, `NFR-04` | (Phủ toàn hệ thống) | `TC-05` | Sprint 4 | \- |

## 6. KẾ HOẠCH NHÂN SỰ & NGÂN SÁCH DỰ KIẾN

### 6.1. Phân bổ trách nhiệm (Ma trận RACI)

*(Quy ước: **R** - Thực hiện chính, **A** - Chịu trách nhiệm duyệt, **C** - Tham vấn ý kiến, **I** - Nhận thông tin kết quả)*

| Hạng mục công việc chính | Nguyễn Duy Hào (PO) | Trần Thị Bích Hạnh (SM) | Nguyễn Thị Ngọc Hà (FE) | Bùi Thị Thùy Dương (QA/BE) |
| ----- | ----- | ----- | ----- | ----- |
| Thu thập yêu cầu, user story và phạm vi sản phẩm | **A** / **R** | **R** | C | C |
| Soạn thảo và cập nhật Mini-SRS | **A** / **R** | C | **R** | C |
| Thiết kế kiến trúc EZcli và cơ chế xử lý cục bộ | **A** / **R** | C | C | **R** |
| Thiết kế giao diện dòng lệnh/tương tác người dùng | C | C | **A** / **R** | **R** |
| Hiện thực nhận diện context và luồng sinh lệnh | **A** | **R** | C | **R** |
| Hiện thực giải thích, xác nhận và thực thi lệnh | C | **R** | C | **A** / **R** |
| Hiện thực lịch sử, tra cứu và quản lý bí danh | C | **R** | **A** / **R** | C |
| Phân tích an toàn cú pháp và cảnh báo lệnh | C | **R** | C | **A** / **R** |
| Lập kế hoạch kiểm thử và đảm bảo chất lượng | C | **R** | **R** | **A** / **R** |
| Điều phối quy trình và theo dõi tiến độ Sprint | C | **A** / **R** | I | I |
| Kiểm thử nghiệm thu và xác nhận sản phẩm | **A** / **R** | C | **R** | C |
| Đóng gói, hướng dẫn sử dụng và báo cáo bàn giao | **A** / **R** | **R** | **R** | C |

### 6.2. Dự toán ngân sách và Chi phí thực hiện

| Danh mục chi phí | Chi tiết hạng mục đầu tư | Số lượng | Đơn giá dự kiến | Thành tiền (VNĐ) | Ghi chú giải trình |
| ----- | ----- | ----- | ----- | ----- | ----- |
| **Thiết bị phát triển và kiểm thử** | Máy tính cá nhân của các thành viên | 4 thiết bị | 0 đ | 0 đ | Tận dụng thiết bị sẵn có; không phát sinh chi phí thuê hoặc mua mới |
| **Mô hình và phần mềm mã nguồn mở** | Mô hình xử lý cục bộ, runtime và thư viện cần thiết | 1 bộ | 0 đ | 0 đ | Sử dụng phần mềm/mô hình miễn phí hoặc mã nguồn mở trong phạm vi đồ án |
| **Công cụ quản lý và thiết kế** | GitHub, công cụ quản lý task và công cụ thiết kế | 1 gói | 0 đ | 0 đ | Sử dụng gói miễn phí hoặc gói dành cho sinh viên |
| **Hạ tầng máy chủ (Cloud VPS)** | Không sử dụng cho phiên bản EZcli chạy cục bộ | 0 tháng | 0 đ | 0 đ | Không cần máy chủ để xử lý yêu cầu hoặc lưu lịch sử |
| **Tên miền (Domain)** | Không sử dụng | 0 năm | 0 đ | 0 đ | EZcli không cung cấp website hoặc dịch vụ trực tuyến |
| **Tài liệu trực tuyến** | Tạo và chia sẻ tài liệu/báo cáo phục vụ nghiệm thu bằng các dịch vụ trực tuyến | 1 gói | 0 đ | 0 đ | Sử dụng dịch vụ trực tuyến miễn phí, không phát sinh chi phí in ấn |
| **Kinh phí dự phòng rủi ro** | Dự phòng phát sinh trong quá trình hoàn thiện và bàn giao | 1 khoản | 0 đ | 0 đ | Nhóm không dự kiến phát sinh chi phí ngoài các tài nguyên miễn phí |
| **TỔNG KINH PHÍ DỰ KIẾN** |  |  |  | **0 VNĐ** | Toàn bộ hạng mục sử dụng thiết bị sẵn có và dịch vụ miễn phí |

## 7. KIỂM NGHIỆM YÊU CẦU & KỊCH BẢN KIỂM THỬ

### 7.1. Kế hoạch kiểm nghiệm chéo yêu cầu

*Nhóm áp dụng quy trình kiểm tra chéo giữa các thành viên trước khi tiến hành lập trình, đảm bảo 5 tiêu chí:*

* \[x\] **Tính đúng đắn:** Yêu cầu mô tả đúng bản chất vấn đề và giải quyết trực tiếp nhu cầu của bên liên quan.

* \[x\] **Tính đầy đủ:** Không bỏ sót các điều kiện biên, dữ liệu đầu vào bắt buộc và phản hồi khi có lỗi.

* \[x\] **Tính nhất quán:** Không có sự xung đột giữa các yêu cầu chức năng với nhau hoặc giữa chức năng với ràng buộc kiến trúc.

* \[x\] **Tính kiểm chứng được:** Mọi yêu cầu phi chức năng đều có ngưỡng đo định lượng cụ thể, không sử dụng các từ ngữ mơ hồ ("nhanh", "dễ dùng", "đẹp mắt").

* \[x\] **Tính khả thi:** Khối lượng công việc nằm trong khả năng kỹ thuật và quỹ thời gian học kỳ của nhóm.

### 7.2. Kịch bản kiểm thử mẫu liên kết yêu cầu

| Mã kiểm thử | Liên kết yêu cầu | Mục đích kiểm thử | Dữ liệu đầu vào giả định | Kết quả mong đợi từ hệ thống |
| ----- | ----- | ----- | ----- | ----- |
| `TC-01` | `FR-01`, `FR-07`, `NFR-01` | Kiểm tra sinh lệnh chính xác từ ngữ cảnh hệ thống và đo thời gian suy luận. | Nhập yêu cầu: "list files in current directory". | Hệ thống trả về lệnh hợp lệ (VD: `ls -la`) dựa theo hệ điều hành đang dùng; thời gian phản hồi $\le 2.0$ giây. |
| `TC-02` | `FR-08`, `FR-03`, `NFR-02` | Phân tích an toàn cú pháp và chặn lệnh phá hoại cục bộ. | Nhập yêu cầu sinh lệnh xóa toàn bộ ổ đĩa: "delete everything on root". | Hệ thống sinh lệnh xóa (`rm -rf /`) nhưng lập tức tô màu đỏ, cảnh báo nguy hiểm dữ liệu và bắt buộc người dùng chọn [A] Hủy hoặc xác nhận. |
| `TC-03` | `FR-05`, `FR-06` | Kiểm tra tìm kiếm mờ lịch sử và ghi nhớ bí danh mới. | Nhập từ khóa mờ để tra lịch sử hoặc gõ trùng tên bí danh hiện có. | Hệ thống trả về lệnh quá khứ gần khớp nhất; cảnh báo ghi đè bí danh nếu trùng tên và lưu bí danh mới thành công. |
| `TC-04` | `FR-02`, `FR-04` | Kiểm tra chức năng giải thích tham số và tra cứu mẫu lệnh. | Chọn [D] để giải thích lệnh `tar -xzf` hoặc tìm kiếm mẫu dùng lệnh `docker`. | Hệ thống in ra màn hình bảng bóc tách ý nghĩa từng tham số của `tar` hoặc trả về danh sách ví dụ mẫu của `docker` (từ tldr). |
| `TC-05` | `NFR-03`, `NFR-04` | Đánh giá độ tương thích đa nền tảng và hiển thị giao diện đồ họa CLI. | Chạy ứng dụng trên PowerShell (Windows) chế độ Dark mode, thực hiện 1 vòng đời sinh lệnh hoàn chỉnh. | Không xảy ra lỗi sập ứng dụng (crash), các nút bấm và màu sắc ANSI (xanh/đỏ/vàng) hiển thị chuẩn xác không bị vỡ định dạng. |
