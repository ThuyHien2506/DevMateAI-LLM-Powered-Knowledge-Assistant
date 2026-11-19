from typing import List, Optional
from pydantic import BaseModel, Field
import uuid


class Citation(BaseModel):
    id: str = Field(..., description="Mã trích dẫn (ví dụ: S1, S2)")
    document_title: str
    heading: Optional[str] = None
    source_url: str
    chunk_id: str


class ChatOptions(BaseModel):
    top_k: int = Field(default=5, ge=1, le=20)
    use_hybrid_search: bool = True


class ChatRequest(BaseModel):
    conversation_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    message: str = Field(..., min_length=1, description="Nội dung câu hỏi của người dùng")
    language: str = Field(default="auto")
    options: ChatOptions = Field(default_factory=ChatOptions)


class RetrievalInfo(BaseModel):
    method: str = "hybrid"
    returned_chunks: int


class ChatResponse(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    conversation_id: str
    answer: str
    citations: List[Citation] = []
    retrieval: RetrievalInfo
    status: str = Field(..., description="'answered' | 'insufficient_context' | 'error'")
