# PROJECT PROPOSAL

> **Môn học:** Nhập môn Công nghệ Phần mềm\
> **Đơn vị:** Bộ môn Công nghệ Phần mềm -- Khoa Công nghệ Thông tin,
> Trường Đại học Khoa học Tự nhiên, ĐHQG-HCM\
> **Tên đề tài:** EZcli\
> **Mã nhóm / Lớp:** Nhóm 09 - 2024/3\
> **Giảng viên hướng dẫn:** TS. Ngô Ngọc Đăng Khoa\
> **Hạn nộp proposal:** 23:59, 03/11/2026

## 1. THÔNG TIN DỰ ÁN & ĐÁNH GIÁ THÀNH VIÊN

### 1.1. Danh sách thành viên & Phân công vai trò

  -------------------------------------------------------------------------
  STT           MSSV          Họ và Tên     Vai trò chính    \% Đóng góp dự
                                            trong dự án                kiến
  ------------- ------------- ------------- ------------- -----------------
  1             24120306      **Nguyễn Duy  **Trưởng                   100%
                              Hào**         nhóm**        

  2             24120304      **Trần Thị    Phát triển &               100%
                              Bích Hạnh**   Tài liệu      

  3             24120299      **Nguyễn Thị  TUI / UX                   100%
                              Ngọc Hà**                   

  4             24120044      **Bùi Thị     Kiểm thử &                 100%
                              Thùy Dương**  Safety        
  -------------------------------------------------------------------------

> **Ghi chú:** Tỷ lệ đóng góp được hiểu là mức độ tham gia của từng
> thành viên trong phạm vi phần việc được phân công, không phải tỷ lệ
> phân chia tổng effort của cả nhóm.

### 1.2. Công cụ và quy trình làm việc

Nhóm áp dụng Scrum với Sprint kéo dài một tuần. Daily Standup được tổ
chức ba ngày một lần, trực tuyến, khoảng 15 phút. Nhóm có Sprint
Planning, Sprint Review và Sprint Retrospective.

Công cụ sử dụng:

-   **Quản lý task:** Trello, Notion.
-   **Quản lý mã nguồn:** Git.
-   **CI:** GitHub Actions.
-   **Nhánh chính:** `main`, `develop`.
-   **Nhánh công việc:** `feat/*`, `fix/*`.

Nhóm ưu tiên tốc độ phát triển nhưng vẫn tách nhánh cho các feature và
bug fix để giảm xung đột trên nhánh chính.

## 2. PHÁT BIỂU BÀI TOÁN & PHẠM VI DỰ ÁN

### 2.1. Bối cảnh & Phát biểu bài toán

CLI là công cụ thường được sử dụng trong phát triển phần mềm và quản trị
hệ thống. Tuy nhiên, người dùng phải nhớ cú pháp, tham số và tùy chọn
của nhiều lệnh khác nhau. Khi gặp tác vụ ít sử dụng hoặc phức tạp, người
dùng thường phải tra cứu tài liệu hoặc hỏi công cụ AI bên ngoài
terminal.

Việc sử dụng LLM để sinh command cũng có rủi ro: command được sinh có
thể không phù hợp với shell hiện tại hoặc có thể gây ảnh hưởng đến dữ
liệu và hệ thống nếu được thực thi mà không kiểm tra.

EZcli được đề xuất như một TUI chạy cục bộ trên Linux, sử dụng LLM cục
bộ thông qua Ollama để chuyển yêu cầu bằng ngôn ngữ tự nhiên thành Bash
command. Trước khi thực thi, hệ thống hiển thị command, kiểm tra các
rule an toàn và yêu cầu người dùng xác nhận.

### 2.2. Vấn đề cần giải quyết

1.  Người dùng phải chuyển đổi giữa terminal và tài liệu/công cụ AI khi
    cần tìm command.
2.  Người dùng có thể gặp khó khăn khi nhớ cú pháp hoặc tham số của
    command.
3.  Command do LLM sinh có thể không phù hợp với context hiện tại hoặc
    có thể chứa thao tác nguy hiểm.
4.  Người dùng muốn sử dụng LLM cục bộ thay vì phụ thuộc vào cloud API
    cho chức năng sinh command.

### 2.3. Mục tiêu dự án

-   Xây dựng TUI cho phép người dùng nhập yêu cầu bằng ngôn ngữ tự
    nhiên.
-   Sử dụng `qwen2.5-coder:3b` thông qua Ollama để sinh Bash command.
-   Thu thập context cần thiết của môi trường hiện tại để hỗ trợ quá
    trình sinh command.
-   Kiểm tra command bằng tập rule an toàn trước khi thực thi.
-   Luôn yêu cầu người dùng xác nhận trước khi execute.
-   Cho phép giải thích command.
-   Lưu lịch sử thao tác cục bộ.
-   Đảm bảo các chức năng cốt lõi không phụ thuộc Internet.

### 2.4. Stakeholder

  --------------------------------------------------------------------------
  Mã             Bên liên quan  Vai trò        Nhu cầu chính  Mức độ ảnh
                                                              hưởng
  -------------- -------------- -------------- -------------- --------------
  `STK-01`       Người dùng ít  Người dùng     Nhập mô tả tự  Cao
                 kinh nghiệm    cuối           nhiên và nhận  
                                               command mà     
                                               không cần nhớ  
                                               toàn bộ cú     
                                               pháp.          

  `STK-02`       Lập trình viên Người dùng     Sinh và giải   Cao
                                nâng cao       thích command, 
                                               thực thi trực  
                                               tiếp, sử dụng  
                                               lịch sử và     
                                               alias.         

  `STK-03`       Giảng viên     Người đánh giá Đánh giá tính  Cao
                                               khả thi, chất  
                                               lượng kỹ thuật 
                                               và mức độ hoàn 
                                               thiện của đồ   
                                               án.            

  `STK-04`       Nhóm phát      Đội ngũ kỹ     Hiện thực,     Cao
                 triển          thuật          kiểm thử và    
                                               tài liệu hóa   
                                               hệ thống.      
  --------------------------------------------------------------------------

### 2.5. Phạm vi dự án

#### Trong phạm vi MVP --- Must Have

-   TUI.
-   Sinh Bash command từ ngôn ngữ tự nhiên.
-   Nhận diện context cần thiết của môi trường.
-   Safety checking bằng rule/regex.
-   Cảnh báo và yêu cầu xác nhận trước khi thực thi.
-   Block các command thuộc nhóm rule được định nghĩa là không cho phép
    thực thi.
-   Execute command trực tiếp trong EZcli.
-   Giải thích command.
-   Lưu lịch sử cục bộ.

#### Should Have

-   Alias.
-   Bổ sung shell context cho quá trình sinh command.

#### Could Have

-   Tìm kiếm mờ lịch sử.
-   Tra cứu tldr.
-   Tra cứu cheat.sh.
-   Hỗ trợ shell khác Bash.
-   Hỗ trợ hệ điều hành khác Linux.

Các chức năng Could Have không được xem là điều kiện bắt buộc để nghiệm
thu MVP.

#### Ngoài phạm vi

-   Cloud LLM hoặc tự động chuyển request lên API AI bên ngoài.
-   Remote command execution.
-   Tự động sửa command sau khi command thực thi thất bại.
-   Hỗ trợ arbitrary shell.
-   Đăng ký global hotkey trên hệ điều hành.

### 2.6. Bảng thuật ngữ

  -----------------------------------------------------------------------
  Thuật ngữ                           Giải nghĩa
  ----------------------------------- -----------------------------------
  `CLI`                               Command-Line Interface, giao diện
                                      tương tác với hệ điều hành bằng
                                      command.

  `TUI`                               Terminal User Interface, giao diện
                                      tương tác hiển thị trong terminal.

  `Shell`                             Chương trình tiếp nhận và phân tích
                                      command để yêu cầu hệ điều hành
                                      thực thi.

  `LLM`                               Large Language Model, mô hình ngôn
                                      ngữ lớn được sử dụng để xử lý yêu
                                      cầu tự nhiên và sinh command.

  `LLM cục bộ`                        LLM chạy trực tiếp trên máy người
                                      dùng thông qua runtime cục bộ.

  `Ollama`                            Runtime được sử dụng để chạy và
                                      giao tiếp với local LLM.

  `Safety rule`                       Rule dùng để xác định command có
                                      khả năng gây ảnh hưởng đến dữ liệu
                                      hoặc hệ thống.

  `DoD`                               Definition of Done, tiêu chí để xác
                                      định một task đã hoàn thành.
  -----------------------------------------------------------------------

## 3. SO SÁNH & ĐÁNH GIÁ CÁC GIẢI PHÁP HIỆN TẠI

### 3.1. Các hướng tiếp cận hiện tại

#### Tra cứu tài liệu hoặc hỏi AI bên ngoài terminal

Người dùng có thể tìm command trên tài liệu trực tuyến hoặc hỏi công cụ
AI. Cách này có thể làm gián đoạn thao tác terminal và yêu cầu người
dùng sao chép thông tin giữa các ứng dụng.

#### Công cụ tìm kiếm lịch sử command

Các công cụ như `fzf` hỗ trợ tìm lại command đã từng xuất hiện trong
history. Tuy nhiên, cách tiếp cận này chủ yếu hỗ trợ tìm command đã có,
không sinh command mới từ yêu cầu tự nhiên.

#### Shell GPT

Nhóm tham khảo `shell_gpt` thông qua repository và README của dự án.
Shell GPT cung cấp chức năng sinh và giải thích command trong terminal.
EZcli tập trung vào một workflow TUI riêng, local LLM và safety checking
trước execution.

#### Warp

Nhóm tham khảo Warp thông qua trang/repository tài liệu được sử dụng
trong quá trình khảo sát. Warp cung cấp terminal tích hợp AI. EZcli tập
trung vào một ứng dụng Linux local-first với local LLM và không sử dụng
cloud LLM trong phạm vi dự án.

### 3.2. Bảng so sánh

  --------------------------------------------------------------------------
  Tiêu chí       Hỏi AI bên     Shell GPT      Warp           EZcli
                 ngoài terminal                               
  -------------- -------------- -------------- -------------- --------------
  Sinh command   Có             Có             Có             Có
  từ ngôn ngữ tự                                              
  nhiên                                                       

  Tích hợp       Thấp           Có             Có             Có
  workflow                                                    
  terminal                                                    

  Local LLM      Phụ thuộc dịch Có thể cấu     Ngoài scope    Có
                 vụ             hình tùy môi   của EZcli      
                                trường                        

  Xử lý core     Không          Có thể         Không phải mục Có
  request cục bộ                               tiêu của EZcli 

  Safety         Không phải     Có             Có cơ chế hỗ   Có rule-based
  checking trước workflow chính confirmation   trợ execution  checking
  execution                                                   

  Confirmation   Phụ thuộc công Có             Có             Bắt buộc
  trước          cụ                                           
  execution                                                   

  Command        Không          Có             Có             Có
  execution                                                   
  trong ứng dụng                                              

  Target         ---            ---            ---            Linux + Bash
  platform của                                                
  đề tài                                                      

  Lịch sử cục bộ Phụ thuộc công Có             Có             Có
                 cụ                                           
  --------------------------------------------------------------------------

> Bảng trên chỉ so sánh theo phạm vi chức năng được nhóm khảo sát và mục
> tiêu của EZcli; không dùng để khẳng định một sản phẩm khác có hoặc
> không có một tính năng nếu nhóm chưa kiểm chứng.

### 3.3. Điểm khác biệt của EZcli

EZcli tập trung vào ba đặc điểm:

1.  **Local-first:** LLM và các chức năng cốt lõi chạy trên máy người
    dùng thông qua Ollama.
2.  **Safety trước execution:** command được kiểm tra theo rule trước
    khi thực thi và luôn yêu cầu xác nhận.
3.  **Tích hợp workflow:** người dùng có thể sinh, xem, giải thích, xác
    nhận và thực thi command ngay trong TUI.

## 4. GIẢI PHÁP ĐỀ XUẤT & ĐẶC TẢ YÊU CẦU PHẦN MỀM (SRS)

### 4.1. User Stories

  -----------------------------------------------------------------------
  ID                      User story              Yêu cầu liên quan
  ----------------------- ----------------------- -----------------------
  `US-01`                 Là người dùng, tôi muốn `FR-01`, `FR-02`
                          mô tả tác vụ bằng ngôn  
                          ngữ tự nhiên để nhận    
                          được Bash command tương 
                          ứng.                    

  `US-02`                 Là người dùng, tôi muốn `FR-03`
                          xem command trước khi   
                          chạy để kiểm tra kết    
                          quả sinh ra.            

  `US-03`                 Là người dùng, tôi muốn `FR-04`
                          được cảnh báo trước các 
                          command nguy hiểm.      

  `US-04`                 Là người dùng, tôi muốn `FR-05`
                          xác nhận trước khi      
                          command được thực thi.  

  `US-05`                 Là người dùng, tôi muốn `FR-06`
                          giải thích command để   
                          hiểu ý nghĩa của từng   
                          thành phần.             

  `US-06`                 Là người dùng, tôi muốn `FR-07`
                          xem lại các thao tác    
                          trước đó từ lịch sử cục 
                          bộ.                     

  `US-07`                 Là người dùng, tôi muốn `FR-08`
                          tạo alias cho command   
                          thường dùng.            
  -----------------------------------------------------------------------

### 4.2. Danh mục yêu cầu chức năng

  ----------------------------------------------------------------------------
  Mã             Chức năng      Mô tả           Ưu tiên        Tiêu chí nghiệm
                                                               thu
  -------------- -------------- --------------- -------------- ---------------
  `FR-01`        Nhập yêu cầu   TUI tiếp nhận   Must           Input hợp lệ
                 tự nhiên       mô tả tác vụ                   được chuyển vào
                                bằng ngôn ngữ                  pipeline xử lý.
                                tự nhiên.                      

  `FR-02`        Sinh Bash      Hệ thống sử     Must           Command được
                 command        dụng local LLM                 hiển thị và
                                để sinh Bash                   thuộc cú pháp
                                command dựa                    Bash trong các
                                trên yêu cầu và                test case đã
                                context đã thu                 định nghĩa.
                                thập.                          

  `FR-03`        Hiển thị       TUI hiển thị    Must           Người dùng có
                 command        command được                   thể xem command
                                sinh trước khi                 trước khi chọn
                                thực thi.                      hành động.

  `FR-04`        Safety         Hệ thống kiểm   Must           Command thuộc
                 checking       tra command                    một rule nguy
                                bằng tập                       hiểm được cảnh
                                rule/regex đã                  báo hoặc block
                                định nghĩa và                  theo mức của
                                phân loại kết                  rule.
                                quả.                           

  `FR-05`        Xác nhận trước Hệ thống yêu    Must           Command không
                 execution      cầu người dùng                 được execute
                                xác nhận trước                 nếu người dùng
                                mọi command                    chọn hủy.
                                execution.                     

  `FR-06`        Giải thích     Hệ thống giải   Must           TUI hiển thị
                 command        thích cấu trúc,                phần giải thích
                                option và tham                 tương ứng với
                                số của command                 command đang
                                khi người dùng                 xem.
                                yêu cầu.                       

  `FR-07`        Lịch sử thao   Hệ thống lưu    Must           Dữ liệu được
                 tác            prompt,                        lưu và có thể
                                command,                       đọc lại sau khi
                                timestamp,                     khởi động lại
                                safety result                  ứng dụng.
                                và execution                   
                                status cục bộ.                 

  `FR-08`        Alias          Hệ thống cho    Should         Alias được lưu
                                phép tạo và                    cục bộ và có
                                quản lý alias                  thể được sử
                                cho command                    dụng lại.
                                thường dùng.                   

  `FR-09`        Shell context  Hệ thống thu    Should         Context được
                                thập context                   truyền vào
                                liên quan như                  pipeline sinh
                                shell và thư                   command.
                                mục hiện tại để                
                                hỗ trợ sinh                    
                                command.                       

  `FR-10`        Fuzzy history  Hệ thống tìm    Could          Tìm được các
                 search         command gần                    entry phù hợp
                                khớp trong                     với từ khóa
                                history.                       kiểm thử.

  `FR-11`        Knowledge      Hệ thống có thể Could          Hiển thị kết
                 lookup         tra cứu                        quả khi
                                tldr/cheat.sh                  Internet khả
                                khi người dùng                 dụng; core
                                yêu cầu.                       functionality
                                                               không phụ thuộc
                                                               chức năng này.
  ----------------------------------------------------------------------------

### 4.3. Yêu cầu phi chức năng

  ------------------------------------------------------------------------
  Mã                Nhóm              Yêu cầu           Phương pháp kiểm
                                                        chứng
  ----------------- ----------------- ----------------- ------------------
  `NFR-01`          Hiệu năng         Hệ thống          Đo thời gian từ
                                      **target** thời   lúc gửi request
                                      gian sinh command đến khi command
                                      ≤ 1 giây đối với  được trả về trên
                                      request điển      tập input được
                                      hình/đơn giản     định nghĩa trước.
                                      trên reference    
                                      environment.      
                                      Request phức tạp  
                                      có thể mất nhiều  
                                      thời gian hơn.    

  `NFR-02`          Local processing  Core command      Kiểm tra cấu
                                      generation và     hình/runtime và
                                      safety checking   network dependency
                                      được xử lý cục    của core flow.
                                      bộ; không sử dụng 
                                      cloud LLM.        

  `NFR-03`          Safety            Safety checker    Unit/integration
                                      phải phát hiện    tests trên safety
                                      các command thuộc rule dataset.
                                      tập rule nguy     
                                      hiểm đã định      
                                      nghĩa.            

  `NFR-04`          Execution safety  Mọi command đều   Integration test
                                      yêu cầu           với safe, warning
                                      confirmation      và blocked
                                      trước execution;  command.
                                      command thuộc     
                                      nhóm `blocked`    
                                      không được        
                                      execute.          

  `NFR-05`          Platform          MVP target Linux  Chạy test suite
                                      và Bash.          trên môi trường
                                                        Linux/Bash được
                                                        thống nhất.

  `NFR-06`          Data storage      History và        Kiểm tra file
                                      configuration     storage và khả
                                      được lưu cục bộ   năng đọc lại dữ
                                      dưới dạng JSON.   liệu sau khi
                                                        restart.

  `NFR-07`          Reliability       Lỗi từ LLM, file  Integration test
                                      storage hoặc      các trường hợp
                                      command execution lỗi.
                                      phải được xử lý   
                                      và hiển thị thay  
                                      vì làm ứng dụng   
                                      kết thúc ngoài dự 
                                      kiến.             

  `NFR-08`          Maintainability   Core logic được   Code review và
                                      tổ chức thành các automated test.
                                      module có thể     
                                      kiểm thử độc lập  
                                      và được kiểm tra  
                                      bằng pytest.      
  ------------------------------------------------------------------------

### 4.4. Đặc tả kịch bản sử dụng

*Mỗi kịch bản mô tả luồng chính và các trường hợp rẽ nhánh quan trọng.*

#### Kịch bản 1: Sinh và thực thi command (`SC-01`)

-   **Tác nhân:** Người dùng.
-   **Tiền điều kiện:** EZcli và Ollama đã được cài đặt; local model sẵn
    sàng.
-   **Kích hoạt:** Người dùng nhập yêu cầu bằng ngôn ngữ tự nhiên.

**Luồng chính:**

1.  Người dùng nhập yêu cầu.
2.  EZcli thu thập context cần thiết.
3.  EZcli gửi request tới local LLM thông qua Ollama.
4.  TUI hiển thị command được sinh.
5.  Safety checker kiểm tra command.
6.  TUI hiển thị kết quả kiểm tra và các hành động khả dụng.
7.  Người dùng chọn thực thi.
8.  EZcli yêu cầu confirmation.
9.  Nếu được xác nhận, command được thực thi qua Bash.
10. EZcli hiển thị stdout/stderr và execution status.
11. EZcli lưu thông tin vào history.

**Rẽ nhánh / Ngoại lệ:**

-   Người dùng chọn **Giải thích** → hiển thị giải thích command, sau đó
    quay lại màn hình hành động.
-   Người dùng chọn **Hủy** → không execute và trả quyền điều khiển cho
    TUI.
-   Safety checker trả về `warning` → hiển thị cảnh báo và yêu cầu
    confirmation.
-   Safety checker trả về `blocked` → không cho phép execute.
-   Ollama không khả dụng → hiển thị lỗi và không thực thi command.
-   Execution thất bại → hiển thị exit status và output lỗi; hệ thống
    không tự sửa hoặc chạy lại command.

**Hậu điều kiện:** Command được execute sau confirmation, hoặc không
được execute nếu người dùng hủy hoặc command bị block.

#### Kịch bản 2: Quản lý history và alias (`SC-02`)

-   **Tác nhân:** Người dùng.
-   **Tiền điều kiện:** EZcli có quyền đọc/ghi storage cục bộ.
-   **Luồng chính:**
    1.  Người dùng mở history hoặc alias.
    2.  Người dùng chọn entry hoặc nhập tên alias.
    3.  EZcli đọc dữ liệu JSON.
    4.  TUI hiển thị kết quả.
    5.  Người dùng tạo/sửa alias nếu cần.
    6.  EZcli kiểm tra và lưu dữ liệu.

**Rẽ nhánh / Ngoại lệ:**

-   Không tìm thấy entry → thông báo và cho phép tìm lại.
-   Alias đã tồn tại → yêu cầu xác nhận trước khi ghi đè.
-   Không thể ghi file → thông báo lỗi và giữ dữ liệu hiện tại.

### 4.5. Kiến trúc tổng thể phần mềm & Công nghệ đề xuất

EZcli sử dụng kiến trúc local-first. Core application chạy trên máy
người dùng và không cần server riêng.

``` text
┌──────────────────────────────┐
│          Textual TUI         │
│  Input / Command / Warning   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      Application Logic       │
│ Context / Workflow / Config  │
└───────┬──────────────┬───────┘
        │              │
        ▼              ▼
┌──────────────┐  ┌──────────────┐
│ Ollama Client│  │Safety Checker│
│ qwen2.5-     │  │ Rule / Regex │
│ coder:3b     │  └──────┬───────┘
└──────┬───────┘         │
       └──────────┬──────┘
                  ▼
        ┌──────────────────┐
        │ Confirmation     │
        └────────┬─────────┘
                 ▼
        ┌──────────────────┐
        │ Command Executor │
        │ subprocess → Bash│
        └────────┬─────────┘
                 ▼
        ┌──────────────────┐
        │ Local JSON Store │
        │ History / Config │
        └──────────────────┘
```

**Công nghệ chính:**

  Thành phần    Công nghệ
  ------------- ----------------------------
  Language      Python
  TUI           Textual
  LLM           `qwen2.5-coder:3b`
  LLM runtime   Ollama
  Safety        Rule/regex matching
  Execution     Python `subprocess` → Bash
  Storage       JSON
  Testing       pytest
  CI            GitHub Actions

### 4.6. Yêu cầu môi trường & Phần cứng

EZcli không yêu cầu máy chủ riêng.

**Reference development environment:**

  Thành phần   Cấu hình
  ------------ ---------------
  CPU          Intel Core i5
  RAM          16 GB
  GPU          4 GB VRAM
  Storage      512 GB
  OS           Linux
  Shell        Bash

EZcli đã được nhóm kiểm thử trên môi trường tham chiếu này với local
model đã chọn. Cấu hình trên được dùng làm **reference environment**,
không được xem là mức phần cứng tối thiểu của hệ thống.

**Internet:** Không bắt buộc cho core functionality. Các chức năng tra
cứu tldr/cheat.sh nếu được triển khai yêu cầu Internet.

## 5. KẾ HOẠCH PHÁT TRIỂN THEO MÔ HÌNH SCRUM

### 5.1. Thiết lập quy trình phát triển

Nhóm áp dụng Scrum với Sprint kéo dài một tuần.

-   **Sprint Planning:** đầu mỗi Sprint.
-   **Daily Standup:** ba ngày một lần, trực tuyến, khoảng 15 phút.
-   **Sprint Review:** cuối Sprint.
-   **Sprint Retrospective:** cuối Sprint, sau Review.
-   **Task management:** Trello và Notion.
-   **Definition of Done:** task được code/review, có test phù hợp, chạy
    được trên môi trường mục tiêu và tài liệu liên quan được cập nhật.

Mỗi task được gắn với FR/NFR hoặc một hạng mục tài liệu và có trạng thái
`To Do`, `In Progress`, `Review`, `Done`.

### 5.2. Lộ trình phát triển

Ngày **05/10/2026** là ngày nhóm bắt đầu xây dựng proposal và Mini-SRS.
Tại thời điểm bắt đầu kế hoạch, project chưa có implementation.

  --------------------------------------------------------------------------
  Giai đoạn          Thời gian         Mục tiêu          Sản phẩm
  ------------------ ----------------- ----------------- -------------------
  **Proposal**       05/10 -- trước    Hoàn thiện        Proposal/Mini-SRS
                     03/11             proposal +        
                                       Mini-SRS          

  **Sprint 1**       Sau khi proposal  Khởi tạo project, Prototype chạy được
                     được chốt         TUI skeleton,     
                                       Ollama            
                                       integration,      
                                       context           
                                       collection        

  **Sprint 2**       1 tuần            NL → command,     Core workflow
                                       explain,          
                                       confirmation,     
                                       execution         

  **Sprint 3**       1 tuần            Safety checker,   MVP tích hợp
                                       history, alias và 
                                       các chức năng     
                                       được ưu tiên      

  **Sprint 4**       1 tuần            Integration       Release candidate
                                       testing, sửa lỗi, 
                                       hoàn thiện UX và  
                                       packaging         

  **Finalization**   02/11 -- 03/11    Regression test,  Bản bàn giao
                                       hoàn thiện tài    
                                       liệu và chuẩn bị  
                                       vấn đáp           
  --------------------------------------------------------------------------

> Ngày bắt đầu cụ thể của Sprint 1--4 phụ thuộc vào thời điểm proposal
> được hoàn thiện. Vì deadline cuối là 03/11/2026, nhóm không đặt Sprint
> kéo dài vượt quá thời hạn này.

### 5.3. Quy trình tiếp nhận & xử lý thay đổi yêu cầu

1.  **Tiếp nhận:** ghi nhận thay đổi và lý do.
2.  **Phân tích tác động:** đánh giá ảnh hưởng đến scope, requirement,
    code và tiến độ.
3.  **Quyết định:** trưởng nhóm và các thành viên thống nhất mức ưu
    tiên.
4.  **Cập nhật:** cập nhật requirement, task và traceability matrix nếu
    thay đổi được chấp nhận.

Thay đổi làm tăng đáng kể scope phải được ưu tiên sau các Must Have của
MVP.

### 5.4. Ma trận truy vết yêu cầu

  --------------------------------------------------------------------------
  Mã nhu cầu     Stakeholder    Requirement    Scenario       Test
  -------------- -------------- -------------- -------------- --------------
  `N-01`         `STK-01`,      `FR-01`,       `SC-01`        `TC-01`,
                 `STK-02`       `FR-02`,                      `TC-02`
                                `FR-09`                       

  `N-02`         `STK-01`,      `FR-03`,       `SC-01`        `TC-03`
                 `STK-02`       `FR-04`,                      
                                `FR-05`                       

  `N-03`         `STK-01`,      `FR-06`,       `SC-02`        `TC-04`
                 `STK-02`       `FR-07`,                      
                                `FR-08`                       

  `N-04`         `STK-03`,      `NFR-01` --    `SC-01`,       `TC-05`,
                 `STK-04`       `NFR-08`       `SC-02`        `TC-06`

  `N-05`         `STK-02`       `FR-10`,       `SC-02`        `TC-07`,
                                 `FR-11`                       `TC-08` (nếu
                                                               triển khai)
  --------------------------------------------------------------------------

## 6. KẾ HOẠCH NHÂN SỰ & NGÂN SÁCH DỰ KIẾN

### 6.1. Phân bổ trách nhiệm (RACI)

> **R** --- thực hiện chính; **A** --- chịu trách nhiệm; **C** --- tham
> vấn; **I** --- được thông báo.

  Hạng mục                             Hào   Hạnh   Hà    Dương
  ------------------------------------ ----- ------ ----- -------
  Yêu cầu, scope và điều phối nhóm     A/R   C      C     C
  Proposal & Mini-SRS                  A     R      R     C
  TUI / UX                             C     C      A/R   C
  LLM integration & command pipeline   A/R   R      C     C
  Context collection                   A/R   C      C     R
  Safety checker                       A     C      C     R
  History / Alias                      C     R      A/R   C
  Testing                              A     C      R     R
  CI / repository                      A/R   C      C     R
  Review & integration                 A/R   R      R     R
  Tài liệu bàn giao / vấn đáp          A     R      R     R

### 6.2. Dự toán ngân sách

  -------------------------------------------------------------------------
  Danh mục                    Số lượng      Chi phí dự kiến Ghi chú
  --------------- -------------------- -------------------- ---------------
  Máy tính phát                      4                0 VNĐ Sử dụng thiết
  triển/kiểm thử                                            bị sẵn có

  Ollama và local                 1 bộ                0 VNĐ Sử dụng trong
  model                                                     phạm vi đồ án

  Thư viện phần                   1 bộ                0 VNĐ Sử dụng thư
  mềm                                                       viện phù hợp
                                                            với giấy phép

  GitHub / CI                        1                0 VNĐ Sử dụng gói
                                                            miễn phí

  Trello / Notion                    1                0 VNĐ Sử dụng gói
                                                            hiện có

  Cloud VPS                          0                0 VNĐ Không sử dụng

  Domain                             0                0 VNĐ Không sử dụng

  **Tổng**                                        **0 VNĐ** 
  -------------------------------------------------------------------------

## 7. KIỂM NGHIỆM YÊU CẦU & KỊCH BẢN KIỂM THỬ

### 7.1. Tiêu chí kiểm nghiệm yêu cầu

Trước khi implement, nhóm kiểm tra requirement theo các tiêu chí:

-   **Đúng:** giải quyết vấn đề đã xác định.
-   **Đầy đủ:** có input, behavior và expected result cần thiết.
-   **Nhất quán:** không mâu thuẫn với requirement hoặc architecture
    khác.
-   **Kiểm chứng được:** có cách test hoặc đo.
-   **Khả thi:** phù hợp scope, thời gian và môi trường của nhóm.

### 7.2. Kịch bản kiểm thử mẫu

  ------------------------------------------------------------------------------------------------------
  ID             Requirement    Mục đích              Input                               Expected
                                                                                          result
  -------------- -------------- --------------------- ----------------------------------- --------------
  `TC-01`        `FR-01`,       Kiểm tra sinh command `list files in current directory`   Hệ thống trả
                 `FR-02`,                                                                 về một Bash
                 `FR-09`                                                                  command hợp lệ
                                                                                          cho context
                                                                                          hiện tại và
                                                                                          hiển thị trên
                                                                                          TUI.

  `TC-02`        `FR-02`,       Kiểm tra latency      Tập request đơn giản đã định nghĩa  Request điển
                 `NFR-01`                                                                 hình đạt
                                                                                          target ≤ 1
                                                                                          giây trên
                                                                                          reference
                                                                                          environment;
                                                                                          kết quả đo
                                                                                          được ghi nhận.

  `TC-03`        `FR-04`,       Kiểm tra safety +     Command thuộc safety rule dataset   Hệ thống cảnh
                 `FR-05`,       confirmation                                              báo hoặc block
                 `NFR-04`                                                                 theo rule;
                                                                                          không execute
                                                                                          nếu chưa được
                                                                                          xác nhận.

  `TC-04`        `FR-07`,       Kiểm tra              Prompt và command mẫu               History được
                 `FR-08`        history/alias                                             lưu vào JSON;
                                                                                          alias được tạo
                                                                                          và đọc lại
                                                                                          thành công.

  `TC-05`        `NFR-02`,      Kiểm tra local        Chạy core flow trên Linux/Bash      Core flow sử
                 `NFR-05`       processing/platform                                       dụng local LLM
                                                                                          và chạy trên
                                                                                          target
                                                                                          environment.

  `TC-06`        `NFR-06`,      Kiểm tra              File storage lỗi hoặc Ollama không  Hệ thống hiển
                 `NFR-07`,      storage/error         khả dụng                            thị lỗi phù
                 `NFR-08`       handling                                                  hợp, không
                                                                                          crash ngoài dự
                                                                                          kiến và không
                                                                                          làm mất dữ
                                                                                          liệu hiện có.
  ------------------------------------------------------------------------------------------------------

### 7.3. Safety test policy

Không thực thi command phá hoại thật trong test.

Ví dụ `rm -rf /` chỉ được dùng như **chuỗi đầu vào cho safety checker**
hoặc fixture của unit test. Test phải kiểm tra kết quả phân loại mà
không chuyển command đó tới Bash.

Safety dataset được xây dựng theo các nhóm rule đã định nghĩa, ví dụ:

-   Recursive/destructive file deletion.
-   Disk/filesystem operations.
-   System shutdown/reboot.
-   Permission changes có rủi ro cao.
-   Các command/pipeline được nhóm xác định là nguy hiểm.

## 8. RỦI RO & GIỚI HẠN

  -----------------------------------------------------------------------
  Rủi ro                  Ảnh hưởng               Biện pháp
  ----------------------- ----------------------- -----------------------
  LLM sinh command không  Cao                     Context + hiển thị
  phù hợp                                         command + explanation +
                                                  confirmation

  LLM hallucination       Cao                     Không tự động execute;
                                                  safety checking và user
                                                  confirmation

  Safety rule bỏ sót      Cao                     Xây dựng rule dataset
  pattern                                         và kiểm thử riêng;
                                                  không claim phát hiện
                                                  mọi command nguy hiểm

  Local model chạy chậm   Trung bình              Target ≤1s chỉ áp dụng
  với request phức tạp                            request điển hình/đơn
                                                  giản; đo trên reference
                                                  environment

  Ollama/model không khả  Cao                     Hiển thị lỗi và không
  dụng                                            execute command

  Khác biệt shell         Trung bình              MVP chỉ target Linux +
                                                  Bash

  Scope tăng trong quá    Cao                     Ưu tiên Must Have trước
  trình phát triển                                Should/Could

  Online lookup không khả Thấp                    Không ảnh hưởng core
  dụng                                            functionality
  -----------------------------------------------------------------------

## 9. GIỚI HẠN CỦA PHIÊN BẢN MVP

MVP không nhằm giải quyết toàn bộ các vấn đề của command generation.

-   Chỉ target Linux + Bash.
-   Không đảm bảo command do LLM sinh luôn phù hợp với mọi tình huống.
-   Safety checker chỉ kiểm tra các pattern/rule đã được định nghĩa.
-   Không tự sửa command sau khi execution thất bại.
-   Không sử dụng cloud LLM.
-   Không remote execution.
-   tldr, cheat.sh, fuzzy search và multi-platform/multi-shell chỉ được
    triển khai nếu còn nguồn lực sau Must Have.
