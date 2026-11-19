from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse, Citation, RetrievalInfo
from app.core.logging import logger

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint chính xử lý câu hỏi người dùng qua RAG Pipeline.
    1. Query analysis & routing
    2. Hybrid Retrieval (Dense + BM25) & RRF Fusion
    3. Context evaluation & Abstention check
    4. LLM Generation + Citation Mapping
    """
    logger.info(f"Received chat message: '{request.message[:50]}...'")

    # Placeholder logic phục vụ khởi tạo sườn dự án (Tuần 1 & 2 sẽ nối RAG Service thực tế)
    mock_citations = [
        Citation(
            id="S1",
            document_title="PyTorch Autograd Overview",
            heading="How Autograd Works",
            source_url="https://docs.pytorch.org/docs/stable/autograd.html",
            chunk_id="chunk-sample-001"
        )
    ]

    return ChatResponse(
        conversation_id=request.conversation_id,
        answer=(
            "Xin chào! Đây là phản hồi mẫu từ khung sườn DevMate AI. "
            "Pipeline RAG (Hybrid Search + Citations) sẽ được kết nối trong các ngày tới. [S1]"
        ),
        citations=mock_citations,
        retrieval=RetrievalInfo(method="hybrid", returned_chunks=1),
        status="answered"
    )
