# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Lê Nguyễn Trâm Anh
> **Mã Sinh Viên / Mã Học viên:** 2A202602760
> **Chủ đề Lựa chọn:** Trợ lý Học vụ VinUni: Tra cứu thông tin sinh viên và đặt lịch tư vấn học vụ

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 4 / 5 | TC04 cần gọi `academic_query` lấy trường `advisor` của sinh viên, rồi dùng tên cố vấn đó cùng mã sinh viên và thời gian để gọi `schedule_appointment`. Đây là hai bước phụ thuộc nhau; `run_react_agent()` hiện đã đưa Observation trở lại context để LLM tiếp tục bước kế tiếp và hoàn tất chuỗi tra cứu -> đặt lịch. |
| **2. Tool Interaction** | 5 / 5 | TC02 và TC05 cần `academic_query` truy vấn `MOCK_DATABASE`; TC03 cần `schedule_appointment` tạo kết quả đặt lịch gồm `booking_id`, thời gian và cố vấn. Hai tool được công bố qua `MCPAcademicServer.list_tools()`; schema `schedule_appointment` đã hoàn thiện, MCP `call_tool()` đã dispatch tool và trả Observation thành công. TC02, TC03, TC04 và TC05 đã chạy qua MCP bằng provider thật trong lần nghiệm thu cuối. |
| **3. Dynamic Decision** | 4 / 5 | Với TC04, Agent dùng kết quả `academic_query` để xác định cố vấn `TS. Lê Thị B` trước khi gọi `schedule_appointment`. Với TC05, Agent gọi đúng `academic_query(SV9999999)`, nhận `NOT_FOUND` và trả lời không tìm thấy hồ sơ thay vì bịa dữ liệu. Dynamic decision đã được kiểm chứng qua trace thật, dù workflow vẫn giới hạn trong một phiên ngắn và chưa có memory dài hạn. |
| **4. Long Horizon Goal** | 2 / 5 | Yêu cầu TC04 cần giữ mục tiêu đặt lịch cùng mã sinh viên và thời gian xuyên suốt bước tra cứu rồi đặt lịch. Workflow chỉ kéo dài vài bước trong một yêu cầu; hiện mỗi lần gọi `run_react_agent()` tạo trace mới, chưa có bộ nhớ hội thoại hay theo dõi mục tiêu qua nhiều phiên. |
| **TỔNG ĐIỂM AGENTIC FIT** | **15 / 20** | *Tổng điểm > 12/20: Chủ đề phù hợp triển khai Agentic System; điểm đánh giá nhu cầu workflow, không xác nhận các TODO trong source đã hoàn thiện.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
  {
    "step": 1,
    "query": "Hãy tra cứu thông tin học vụ của sinh viên SV2026002 để xác định cố vấn học tập, sau đó đặt lịch hẹn tư vấn với đúng cố vấn vừa tra cứu vào lúc 10:00 ngày 16/09/2026 cho sinh viên này.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "academic_query",
    "arguments": {
      "student_id": "SV2026002"
    },
    "observation": {
      "status": "SUCCESS",
      "student_id": "SV2026002",
      "data": {
        "full_name": "Trần Thị Bình",
        "class": "AI-K4",
        "gpa": 3.6,
        "email": "binh.tt@vinuni.edu.vn",
        "status": "Đang học",
        "advisor": "TS. Lê Thị B"
      }
    },
    "latency_ms": 4642.24
  },
  {
    "step": 2,
    "query": "Hãy tra cứu thông tin học vụ của sinh viên SV2026002 để xác định cố vấn học tập, sau đó đặt lịch hẹn tư vấn với đúng cố vấn vừa tra cứu vào lúc 10:00 ngày 16/09/2026 cho sinh viên này.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "schedule_appointment",
    "arguments": {
      "advisor_name": "TS. Lê Thị B",
      "datetime_str": "10:00 16/09/2026",
      "student_id": "SV2026002"
    },
    "observation": {
      "status": "SUCCESS",
      "booking_id": "BK-SV2026002-99",
      "student_id": "SV2026002",
      "datetime": "10:00 16/09/2026",
      "advisor": "TS. Lê Thị B",
      "message": "Đặt lịch thành công cho sinh viên SV2026002 với TS. Lê Thị B vào lúc 10:00 16/09/2026."
    },
    "latency_ms": 7559.36
  },
  {
    "step": 3,
    "query": "Hãy tra cứu thông tin học vụ của sinh viên SV2026002 để xác định cố vấn học tập, sau đó đặt lịch hẹn tư vấn với đúng cố vấn vừa tra cứu vào lúc 10:00 ngày 16/09/2026 cho sinh viên này.",
    "action_type": "FINAL_ANSWER",
    "thought": "OpenAI phản hồi trực tiếp bằng văn bản (không cần gọi công cụ).",
    "output": "Tôi đã hoàn tất toàn bộ yêu cầu của bạn. Dưới đây là tổng hợp kết quả: tra cứu thông tin học vụ sinh viên SV2026002 và đặt lịch tư vấn thành công với đúng cố vấn TS. Lê Thị B vào 10:00 ngày 16/09/2026.",
    "latency_ms": 6374.05
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (OpenAIProvider).
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 5 lượt.
- **Kết quả đẩy Repo nộp bài:** [x] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
