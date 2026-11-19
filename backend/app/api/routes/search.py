from fastapi import APIRouter
from app.schemas.search import SearchRequest, SearchResponse, SearchResultItem
from app.core.logging import logger

router = APIRouter(prefix="/search", tags=["Search"])


@router.post("", response_model=SearchResponse)
async def search_endpoint(request: SearchRequest):
    """
    Endpoint tra cứu trực tiếp tài liệu kỹ thuật (phục vụ debug và benchmark).
    Hỗ trợ các phương thức: 'dense', 'bm25', 'hybrid'.
    """
    logger.info(f"Searching with method='{request.method}' for query='{request.query}'")

    # Placeholder kết quả mẫu
    sample_results = [
        SearchResultItem(
            chunk_id="chunk-sample-001",
            document_title="PyTorch Documentation",
            heading="torch.autograd.backward",
            content="Computes the sum of gradients of given tensors with respect to graph leaves.",
            score=0.92,
            source_url="https://docs.pytorch.org/docs/stable/generated/torch.autograd.backward.html"
        )
    ]

    return SearchResponse(
        query=request.query,
        method=request.method,
        total_results=len(sample_results),
        results=sample_results
    )
