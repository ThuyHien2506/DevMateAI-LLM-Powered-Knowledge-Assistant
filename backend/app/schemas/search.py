from typing import List, Optional
from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Từ khóa hoặc câu hỏi cần tìm kiếm")
    top_k: int = Field(default=5, ge=1, le=50)
    method: str = Field(default="hybrid", description="'dense' | 'bm25' | 'hybrid'")


class SearchResultItem(BaseModel):
    chunk_id: str
    document_title: str
    heading: Optional[str] = None
    content: str
    score: float
    source_url: str


class SearchResponse(BaseModel):
    query: str
    method: str
    total_results: int
    results: List[SearchResultItem]
