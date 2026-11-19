# 🚀 DevMate AI — LLM-Powered Engineering Knowledge Assistant

> **An Evaluated Hybrid & Agentic RAG System for Technical Documentation**  
> Dự án trợ lý tri thức kỹ thuật hỗ trợ lập trình viên tra cứu tài liệu chuyên sâu (Python, PyTorch) với cơ chế tìm kiếm kết hợp (Hybrid Search), trích dẫn minh bạch (Source Citation), tự động từ chối khi thiếu căn cứ (Abstention) và đo lường benchmark định lượng.

---

## 📌 Điểm nổi bật kỹ thuật (Key Highlights)

Khác với các ứng dụng "Naive RAG" (chỉ tìm kiếm vector cơ bản), **DevMate AI** được thiết kế theo chuẩn kỹ thuật AI Engineering:

1. **Hybrid Retrieval + Reciprocal Rank Fusion (RRF):**
   - Kết hợp **Dense Retrieval** (Vector Embedding đa ngôn ngữ với `BGE-M3` qua Qdrant) để hiểu ngữ nghĩa khái niệm.
   - Kết hợp **Sparse Retrieval** (BM25) để bắt chính xác các từ khóa kỹ thuật, tên hàm (`torch.autograd`, `model.eval()`).
   - Hợp nhất xếp hạng công bằng bằng giải thuật **RRF**.
2. **Grounded Generation & Source Citations:**
   - LLM bắt buộc phải trích dẫn nguồn theo thẻ `[S1]`, `[S2]` và ánh xạ trực tiếp đến URL / Heading tài liệu gốc.
3. **Abstention Mechanism (Phòng chống ảo giác):**
   - Tự động phát hiện khi tài liệu không đủ dữ liệu để trả lời và thông báo giới hạn thay vì bịa đặt (hallucination).
4. **Agentic Router (Định tuyến thông minh):**
   - Phân tích câu hỏi người dùng để lựa chọn chiến lược: Trả lời nhanh, Tra cứu tài liệu (RAG), hay Giải thích code.
5. **Đánh giá Benchmark định lượng:**
   - So sánh khoa học giữa các cấu hình: **BM25 vs. Dense vs. Hybrid vs. Reranker** qua các chỉ số **Recall@5, MRR@5, nDCG@5, Faithfulness**.

---

## 🏗️ Kiến trúc hệ thống (System Architecture)

```text
                  USER
                    │
                    ▼
          React + TypeScript UI
                    │
                    ▼
             FastAPI Backend
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
   Conversation Mgr      RAG Service
                              │
                              ▼
                      [Agentic Router]
                              │
                              ▼
                       Hybrid Retrieval
                         /          \
                        ▼            ▼
                  Dense Search   BM25 Search
                   (BGE-M3)       (Keyword)
                        │            │
                        ▼            ▼
                     Qdrant      BM25 Index
                        \            /
                         \          /
                          ▼        ▼
                        RRF Fusion
                             │
                             ▼
                    [Context Grader] ──(Thiếu ngữ cảnh)──► [Abstention]
                             │ (Đủ ngữ cảnh)
                             ▼
                       Top-K Context
                             │
                             ▼
                       LLM Provider (Local Ollama / API)
                             │
                             ▼
                    Answer + Citations
                             │
                             ▼
                       React UI
```

---

## 📂 Cấu trúc thư mục (Project Structure)

```text
DevMateAI/
├── backend/                  # FastAPI Backend & RAG Core
│   ├── app/
│   │   ├── api/routes/       # API Endpoints (chat, search, health)
│   │   ├── core/             # Cấu hình config & logging
│   │   ├── ingestion/        # Crawler, Parser, Chunker, Indexer
│   │   ├── retrieval/        # Dense, BM25, Hybrid, RRF Fusion
│   │   ├── generation/       # LLM provider, Prompt, Citations
│   │   ├── conversation/     # Quản lý phiên hội thoại
│   │   ├── evaluation/       # Benchmark runner & metrics
│   │   ├── schemas/          # Pydantic data schemas
│   │   └── main.py           # Entry point của FastAPI
│   ├── requirements.txt      # Thư viện Python
│   └── Dockerfile
├── frontend/                 # Giao diện React + TypeScript (UI)
├── data/                     # Thư mục chứa dữ liệu
│   ├── raw/                  # Tài liệu thô tải về (HTML, Markdown)
│   ├── processed/            # Dữ liệu chunks & BM25 index
│   └── evaluation/           # Bộ 80 câu hỏi test benchmark (dev.jsonl, test.jsonl)
├── docs/                     # Tài liệu thiết kế chi tiết (PROJECT_SPEC.md)
├── notebooks/                # Jupyter Notebooks thí nghiệm & phân tích
├── docker-compose.yml        # Chạy Qdrant Vector DB nhanh chóng
├── .env.example              # Mẫu biến môi trường
└── README.md
```

---

## ⚡ Hướng dẫn cài đặt nhanh (Quickstart)

### 1. Chuẩn bị môi trường
- Python 3.10+
- Docker & Docker Compose (để chạy Qdrant)
- [Ollama](https://ollama.com/) (để chạy LLM local, khuyến nghị model `qwen2.5:3b` hoặc `qwen2.5:7b`)

### 2. Khởi chạy Vector Database (Qdrant)
```bash
docker compose up -d
```
> Kiểm tra Qdrant Dashboard tại: [http://localhost:6333/dashboard](http://localhost:6333/dashboard)

### 3. Cài đặt Backend
```bash
cd backend
python -m venv venv

# Kích hoạt môi trường:
# Trên Windows:
.\venv\Scripts\activate
# Trên Linux/Mac:
# source venv/bin/activate

pip install -r requirements.txt
```

### 4. Cấu hình biến môi trường
Tạo file `.env` từ `.env.example`:
```bash
copy ..\.env.example .env
```

### 5. Khởi chạy FastAPI Server
```bash
uvicorn app.main:app --reload --port 8000
```
> Truy cập Swagger UI API Docs tại: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📊 Kế hoạch Benchmark (Thực nghiệm định lượng)

Dự án đo lường chất lượng trên tập 80 câu hỏi kỹ thuật:
- **E1: BM25 Only** (Từ khóa truyền thống).
- **E2: Dense Only** (Ngữ nghĩa thuần túy với BGE-M3).
- **E3: Hybrid Search (RRF)** (Kết hợp cả hai).
- **E4: Hybrid + Reranker** (Đánh giá lại top kết quả).

Chi tiết thiết kế và tiêu chí hoàn thành xem tại [docs/PROJECT_SPEC.md](docs/PROJECT_SPEC.md).

---

## 🛠️ Lộ trình 30 ngày "Vừa học vừa làm"
- **Tuần 1:** Setup hạ tầng, thu thập tài liệu PyTorch/Python, hoàn thiện Ingestion & Chunking pipeline.
- **Tuần 2:** Xây dựng Dense + BM25, tích hợp RRF và chạy Benchmark so sánh đầu tiên.
- **Tuần 3:** Tích hợp Local LLM (Ollama), Citation engine, Abstention và Agent Router.
- **Tuần 4:** Xây dựng giao diện Web (React), hoàn thiện Docker và báo cáo phân tích lỗi.

---

## 📜 License
MIT License.
