# DevMate AI — Technical Specification & Architecture

**Project Type:** AI Engineering / Hybrid & Evaluated RAG  
**Target Users:** Developers & Students  
**Initial Domain:** AI/ML Engineering (Python & PyTorch)  
**Development Duration:** 30 days  
**Deployment:** Local (Docker + Ollama) + Google Colab  
**Project Scope:** Production-grade RAG with Hybrid Retrieval (Dense + BM25 + RRF), Citation Verification, Abstention, Quantitative Evaluation & Agentic Routing.

---

## 1. Tổng quan dự án

### 1.1. Giới thiệu
DevMate AI là hệ thống trợ lý tri thức kỹ thuật ứng dụng Large Language Model (LLM) và Retrieval-Augmented Generation (RAG), hỗ trợ người học và lập trình viên tra cứu, tiếp cận và vận dụng kiến thức kỹ thuật từ các tài liệu chuyên ngành (Python, PyTorch).

Khác biệt với các ứng dụng Naive RAG (chỉ tìm kiếm vector đơn giản), DevMate AI áp dụng:
1. **Hybrid Retrieval:** Kết hợp Dense Retrieval (BGE-M3 qua Qdrant) và Sparse Retrieval (BM25) sử dụng thuật toán Reciprocal Rank Fusion (RRF).
2. **Grounded Generation & Citation:** Trích dẫn chính xác nguồn tài liệu (`[S1]`, `[S2]`) kèm URL và heading.
3. **Abstention Mechanism:** Tự động phát hiện khi tài liệu không đủ bằng chứng và chủ động từ chối trả lời thay vì ảo giác (hallucination).
4. **Agentic Router & Verification:** Phân loại ý định người dùng (Documentation Search vs. Concept Explanation vs. Code Debug) và tự kiểm chứng mức độ phù hợp của ngữ cảnh.
5. **Thực nghiệm Benchmark định lượng:** Đánh giá đa chiều (Recall@5, MRR@5, nDCG@5, Faithfulness, Answer Relevance).

---

## 2. Kiến trúc hệ thống

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
                      (Intent & Query)
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
                       LLM Provider (Qwen3 4B / Ollama)
                             │
                             ▼
                    Answer + Citations
                             │
                             ▼
                       FastAPI Backend ──► React UI
```

---

## 3. Data Ingestion Pipeline

```text
Official Documentation (Python / PyTorch)
          │
          ▼
     Web Crawler / Source Parser
          │
          ▼
   Content Cleaning (Remove nav/footer/scripts)
          │
          ▼
    Heading-aware & Token Chunking (400-600 tokens)
          │
          ▼
   Metadata Extraction (URL, Title, Heading, Version)
          │
          ▼
    BGE-M3 Embedding
          │
          ▼
       Qdrant (Vector) + BM25 Inverted Index (Disk)
```

---

## 4. Kế hoạch thực nghiệm (Benchmark Matrix)

Dự án thiết kế bộ thực nghiệm để so sánh định lượng chất lượng truy xuất:

| Experiment | Retrieval Method | Mục đích | Metrics chính |
|---|---|---|---|
| **E1** | BM25 (Sparse) | Baseline tìm kiếm từ khóa kỹ thuật (API, hàm) | Recall@5, MRR@5 |
| **E2** | Dense (BGE-M3) | Đánh giá tìm kiếm ngữ nghĩa khái niệm | Recall@5, MRR@5 |
| **E3** | Hybrid (Dense + BM25 + RRF) | Đánh giá hiệu quả kết hợp | Recall@5, nDCG@5 |
| **E4 (Mở rộng)** | Hybrid + Reranker (Cross-Encoder) | Đánh giá cải thiện khi re-score Top-K | Recall@5, Latency |

### Generation Metrics:
- **Faithfulness:** Câu trả lời có đúng với ngữ cảnh truy xuất không?
- **Answer Relevance:** Câu trả lời có trả lời đúng trọng tâm câu hỏi?
- **Abstention Accuracy:** Hệ thống có từ chối đúng khi gặp câu hỏi không có tài liệu?

---

## 5. Roadmap 30 ngày (Vừa học vừa làm)

- **Tuần 1 (Ngày 1–7): Foundation & Ingestion**
  - Setup repository, Docker Compose (Qdrant), FastAPI.
  - Thu thập tài liệu Python & PyTorch cơ bản.
  - Chunking & Indexing vào Qdrant với model BGE-M3.
- **Tuần 2 (Ngày 8–14): Hybrid Retrieval & Benchmark**
  - Cài đặt BM25, kết hợp RRF (Reciprocal Rank Fusion).
  - Chuẩn bị tập câu hỏi test (80 câu).
  - Chạy benchmark E1, E2, E3; ghi nhận số liệu.
- **Tuần 3 (Ngày 15–21): LLM, Citation & Router**
  - Tích hợp Ollama (Qwen 4B / Qwen 2.5 / DeepSeek).
  - Xây dựng Prompt Grounding, Citation Mapping (`[S1]`, `[S2]`) và Abstention logic.
  - Xây dựng Agent Router phân loại truy vấn.
- **Tuần 4 (Ngày 22–30): Full-Stack, UI & Portfolio Finish**
  - Xây dựng UI React/TypeScript hiển thị Citation panel.
  - Đóng gói Docker Compose, viết báo cáo Benchmark.
  - Hoàn thiện tài liệu, video demo và README cho portfolio.
