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

| STT | MSSV | Họ và Tên | Vai trò chính trong dự án | % Đóng góp dự kiến | 
| ----- | ----- | ----- | ----- | ----- | 
| 1 | 24120306 | **Nguyễn Duy Hào** | **Trưởng nhóm** / Quản lý sản phẩm (Product Owner) | 100% | 
| 2 | 24120304 | **Trần Thị Bích Hạnh** | Điều phối dự án (Scrum Master) / Lập trình viên Backend | 100% | 
| 3 | 24120299 | **Nguyễn Thị Ngọc Hà** | Trưởng nhóm Giao diện (Frontend Lead) / Thiết kế UI-UX | 100% | 
| 4 | 24120044 | **Bùi Thị Thùy Dương** | Quản lý chất lượng & Kiểm thử (QA/QC) / Lập trình viên Backend | 100% | 

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

  * Tạo và quản lý bí danh.

  * Cơ chế xử lý hoàn toàn cục bộ.

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
  * Tra cứu lệnh bằng tài liệu trên mạng hoặc hỏi AI
  * Cấu hình gợi ý lệnh mờ
  * Tạo và quản lý bí danh
  * Tìm trong lịch sử lệnh đã gõ

* **Giải pháp thương mại đóng gói sẵn:** 
  * Warp Terminal: ứng dụng GUI hỗ trợ chat với AI và gõ lệnh trực tiếp trong giao diện.
  * Shell GPT: tích hợp lệnh `sgpt` và cờ `-s` hỗ trợ gợi ý lệnh bằng ngôn ngữ tự nhiên.


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

* Có thể sử dụng mô hình cục bộ, không cần kết nối Internet hay tốn chi phí API.
* Dữ liệu cá nhân được xử lý hoàn toàn cục bộ, không rò rỉ dữ liệu ra ngoài.
* Tích hợp sâu cơ chế bảo vệ an toàn (chạy thử nghiệm và phân tích cú pháp tĩnh) giúp ngăn ngừa việc thực thi nhầm các lệnh phá hủy hệ thống.
* Giao diện đẹp mắt, tối ưu hóa trải nghiệm người dùng mà không cần phải tự tay tùy biến quá nhiều.

## 4. GIẢI PHÁP ĐỀ XUẤT & ĐẶC TẢ YÊU CẦU PHẦN MỀM (SRS)

### 4.1. Bảng câu chuyện người dùng

| Nhu cầu của bên liên quan (Cấu trúc: Là \[ai\], tôi muốn \[làm gì\] để \[đạt được gì\]) | Yêu cầu hệ thống giải quyết tương ứng | 
| ----- | ----- | 
| Là **người dùng không chuyên về công nghệ**, tôi muốn được gợi ý lệnh để không phải nhớ lệnh. | Gợi ý lệnh bằng ngôn ngữ tự nhiên `FR-01` & `FR-02` | 
| Là **Lập trình viên**, tôi muốn giao diện thân thiện hơn để dễ sử dụng | 
| Là **Lập trình viên**, tôi muốn sử dụng được mô hình llm cục bộ để không phải trả tiền API. | \[Tên yêu cầu chức năng hoặc mô-đun xử lý\] | 
| Là **\[Người dùng chung\]**, tôi muốn thời gian xử lý nhanh và dữ liệu được bảo vệ an toàn. | \[Yêu cầu về hiệu năng hệ thống và bảo mật dữ liệu\] | 

### 4.2. Danh mục yêu cầu chức năng (FR)

| Mã yêu cầu | Tên chức năng | Mô tả chi tiết hành vi của hệ thống | Mức ưu tiên | Nguồn gốc | Tiêu chí nghiệm thu | 
| ----- | ----- | ----- | ----- | ----- | ----- | 
| `FR-01` | Sinh lệnh từ ngôn ngữ tự nhiên | Tiếp nhận chuỗi văn bản mô tả và sinh ra câu lệnh tương ứng. | Must Have | STK-01, STK-02 | Sinh đúng câu lệnh thực thi hợp lệ theo môi trường hiện tại. | 
| `FR-02` | Giải thích chi tiết câu lệnh | Phân tích cấu trúc, cờ và tham số của câu lệnh vừa sinh ra theo yêu cầu của người dùng. | Should Have | STK-01 | Hiển thị mô tả rõ ràng từng tham số khi người dùng chọn lệnh giải thích. | 
| `FR-03` | Xác nhận trước khi thực thi | Cung cấp ba tùy chọn bắt buộc: Thực thi, Giải thích, hoặc Hủy bỏ trước khi chạy bất kỳ lệnh nào. | Must Have | STK-01, STK-02 | Lệnh chỉ được chạy vào hệ thống khi người dùng xác nhận thực thi. | 
| `FR-04` | Tra cứu mẫu tác vụ phổ biến | Tìm kiếm và hiển thị các trường hợp sử dụng chuẩn thông qua tích hợp dữ liệu tldr và cheat.sh. | Should Have | STK-02 | Trả về danh sách mẫu ví dụ tương ứng với tên lệnh tra cứu. | 
| `FR-05` | Tìm kiếm mờ lịch sử lệnh | Tìm kiếm các lệnh từng thực hiện trong quá khứ dựa trên thuật toán so khớp mờ. | Should Have | STK-02 | Danh sách kết quả gợi ý đúng câu lệnh gần khớp nhất theo thời gian thực. | 
| `FR-06` | Quản lý bí danh tự động | Hỗ trợ tạo mới, chỉnh sửa và ghi nhớ các bí danh rút gọn cho các lệnh dài. | Could Have | STK-02 | Bí danh mới được áp dụng ngay lập tức vào phiên làm việc hiện tại. | 
| `FR-07` | Nhận diện ngữ cảnh hệ thống | Tự động đọc thông tin về hệ điều hành, trình bao đang dùng, thư mục hiện tại để tối ưu câu lệnh sinh ra. | Must Have | STK-04 | Câu lệnh sinh ra khớp hoàn toàn với cú pháp của hệ điều hành và trình bao đang mở. | 
| `FR-08` | Phân tích an toàn cú pháp | Phân tích cú pháp tĩnh và tô màu cảnh báo nếu câu lệnh có nguy cơ xóa tệp hoặc can thiệp sâu quyền hệ thống. | Must Have | STK-01, STK-04 | Hiển thị cảnh báo trực quan với các câu lệnh có khả năng gây mất mát dữ liệu. | 

### 4.3. Danh mục yêu cầu phi chức năng (NFR)

| Mã yêu cầu | Nhóm chất lượng | Tiêu chí kỹ thuật định lượng | Phương pháp kiểm chứng | 
| ----- | ----- | ----- | ----- | 
| `NFR-01` | **Hiệu năng (Performance)** | Thời gian sinh câu lệnh từ văn bản tự nhiên $\le 2.0$ giây khi chạy LLM cục bộ trên cấu hình máy tính tiêu chuẩn (RAM 8GB, CPU 4 cores) trong 95% trường hợp. | Đo đạc tự động thời gian phản hồi (từ khi gửi yêu cầu đến khi in kết quả) bằng script kiểm thử với tập 100 câu lệnh đầu vào khác nhau. | 
| `NFR-02` | **Bảo mật & An toàn (Security)** | 100% dữ liệu xử lý cục bộ không truyền ra internet. Nhận diện và cảnh báo thành công 100% các câu lệnh phá hoại (vd: `rm -rf /`, `mkfs`) bằng phân tích cú pháp tĩnh. | Dùng Wireshark kiểm tra gói tin để đảm bảo không có kết nối ra ngoài. Chạy thử nghiệm tập 50 lệnh nguy hiểm (Malicious Dataset) để kiểm chứng cơ chế chặn. | 
| `NFR-03` | **Tương thích (Compatibility)** | Tỷ lệ sập ứng dụng (crash rate) $\le 1\%$. Lệnh sinh ra tương thích 100% trên 3 môi trường shell mục tiêu: Bash, Zsh (Linux/macOS) và PowerShell (Windows). | Thực thi 200 lượt test tự động trên máy ảo của 3 hệ điều hành tương ứng để xác nhận lệnh sinh ra chạy hợp lệ, không lỗi cú pháp shell. | 
| `NFR-04` | **Khả dụng (Usability)** | Số thao tác tối đa để xác nhận/thực thi lệnh sau khi sinh là 1 phím bấm (VD: nhấn 'E'). Giao diện render chính xác chuẩn màu ANSI. | Thống kê số bước phím bấm theo kịch bản sử dụng SC-01. Khảo sát 5 người dùng cuối trải nghiệm trực tiếp với mức độ hài lòng yêu cầu $\ge 4/5$. | 

### 4.4. Đặc tả kịch bản sử dụng

*Mỗi kịch bản phải làm rõ luồng chính và tối thiểu 1 luồng ngoại lệ/rẽ nhánh.*

#### Kịch bản 1: Sinh câu lệnh từ văn bản tự nhiên và lựa chọn hành động (`SC-01`)

* **Tác nhân chính:** Người dùng cuối.

* **Tiền điều kiện:** Công cụ ezcli đã được cấu hình và mô hình xử lý cục bộ đang ở trạng thái sẵn sàng.

* **Sự kiện kích hoạt:** Người dùng gõ lệnh ezcli kèm theo yêu cầu bằng ngôn ngữ tự nhiên.

* **Luồng sự kiện chính:**

  1. Người dùng nhập câu lệnh yêu cầu (Ví dụ: tìm tất cả các tệp có đuôi json trong thư mục hiện tại).

  2. Hệ thống thu thập ngữ cảnh làm việc hiện tại (hệ điều hành, trình bao, thư mục) và chuyển vào bộ xử lý.

  3. Hệ thống trả về câu lệnh tương ứng trên màn hình và phân tích cú pháp tĩnh.

  4. Hệ thống đưa ra menu gồm ba lựa chọn: Thực thi [E], Giải thích [D], Hủy bỏ [A].

  5. Người dùng nhấn chọn phím E để thực thi.

  6. Hệ thống chuyển lệnh xuống trình bao để thực hiện và trả về kết quả cho người dùng.

* **Luồng rẽ nhánh / Ngoại lệ:**

  * *Rẽ nhánh tại bước 5 (Người dùng chọn D):* Hệ thống hiển thị bảng bóc tách ý nghĩa từng tham số của lệnh, sau đó quay lại menu ba lựa chọn.

  * *Rẽ nhánh tại bước 5 (Người dùng chọn A):* Hệ thống hủy bỏ câu lệnh và trả quyền điều khiển về dòng lệnh thông thường.

  * *Ngoại lệ tại bước 3 (Phát hiện lệnh nguy hiểm):* Hệ thống đổi màu cảnh báo nổi bật và yêu cầu xác nhận thêm một bước trước khi cho phép bấm thực thi.

* **Hậu điều kiện:** Lệnh được thực thi an toàn trên hệ thống hoặc phiên làm việc kết thúc theo lựa chọn của người dùng.

#### Kịch bản 2: \[Tên tình huống ngoại lệ / Hủy bỏ / Thay đổi\] (`SC-02`)

* **Tác nhân chính:** \[Người dùng thực hiện hành động\]

* **Tiền điều kiện:** \[Dữ liệu ban đầu đã tồn tại trong hệ thống\]

* **Sự kiện kích hoạt:** \[Tác nhân yêu cầu hủy hoặc thay đổi dữ liệu\]

* **Luồng sự kiện chính:**

  1. Tác nhân chọn đối tượng cần điều chỉnh \[Bước 1\].

  2. Hệ thống kiểm tra điều kiện cho phép điều chỉnh \[Bước 2\].

  3. Tác nhân xác nhận yêu cầu thay đổi \[Bước 3\].

  4. Hệ thống cập nhật bản ghi và giải phóng tài nguyên liên quan \[Bước 4\].

  5. Hệ thống thông báo kết quả cập nhật thành công \[Bước 5\].

* **Luồng rẽ nhánh / Ngoại lệ:**

  * *Rẽ nhánh tại bước 2 (Quá hạn cho phép thay đổi):* Hệ thống từ chối thao tác, thông báo lý do vi phạm quy định cho tác nhân.

* **Hậu điều kiện:** \[Dữ liệu được cập nhật trạng thái mới hoặc bị thu hồi thành công\]

### 4.5. Kiến trúc tổng thể phần mềm & Công nghệ đề xuất

* **Mô hình kiến trúc phần mềm:** \[Ví dụ: Kiến trúc 3 tầng (3-Tier) hoặc Kiến trúc Client-Server tách biệt giao tiếp qua RESTful API\].

* **Công nghệ phía Giao diện (Frontend):** \[Ví dụ: React.js / Vue.js / Flutter, Tailwind CSS\].

* **Công nghệ phía Máy chủ (Backend):** \[Ví dụ: Node.js (Express/NestJS) / Python (FastAPI/Django) / Java Spring Boot\].

* **Hệ quản trị Cơ sở dữ liệu:** \[Ví dụ: PostgreSQL / MySQL / MongoDB\].

* **Giải pháp triển khai & Hạ tầng:** \[Ví dụ: Đóng gói Docker Container, máy chủ ảo Cloud VPS / Vercel\].

### 4.6. Yêu cầu môi trường & Phần cứng

* **Phía Máy chủ:**

  * CPU: Tối thiểu 2 vCPU.

  * RAM: Tối thiểu 2 GB - 4 GB.

  * Dung lượng ổ đĩa: Tối thiểu 20 GB SSD.

  * Môi trường thực thi: Linux (Ubuntu Server LTS) có cài đặt môi trường chạy mã nguồn và tường lửa cơ bản.

* **Phía Người dùng (Client):**

  * Thiết bị: Máy tính cá nhân hoặc điện thoại thông minh.

  * Trình duyệt web hiện đại hỗ trợ HTML5/CSS3/JavaScript (Google Chrome, Edge, Safari, Firefox).

  * Đường truyền kết nối Internet ổn định.

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
| `N-01` | STK-01 | `FR-01`, `NFR-02` | `SC-01` | `TC-01` | Sprint 1 | \- | 
| `N-02` | STK-01 | `FR-02`, `FR-03` | `SC-01` | `TC-02` | Sprint 2 | \- | 
| `N-03` | STK-02 | `FR-04`, `FR-05` | `SC-02` | `TC-03` | Sprint 2 | \- | 
| `N-04` | STK-03 | `FR-06`, `FR-09` | `SC-03` | `TC-04` | Sprint 3 | `CR-01` (nếu có) | 

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
| `TC-01` | `FR-01`, `NFR-02` | Kiểm tra phản hồi bảo mật khi nhập sai thông tin xác thực | Nhập sai mật khẩu liên tiếp quá 5 lần | Hệ thống từ chối đăng nhập, hiển thị thông báo khóa tạm thời và ghi nhật ký cảnh báo. | 
| `TC-02` | `FR-02`, `FR-03` | Kiểm tra ràng buộc dữ liệu tại giá trị biên | Nhập dữ liệu vượt quá giới hạn cho phép | Hệ thống hiển thị cảnh báo lỗi cụ thể tại ô nhập liệu, không cho phép gửi yêu cầu. | 
| `TC-03` | `NFR-01` | Đo lường thời gian phản hồi khi chịu tải đồng thời | Gửi 50 yêu cầu đồng thời đến hệ thống trong 30 giây | 100% yêu cầu được xử lý thành công với thời gian phản hồi $\le 1.5$ giây. | 
