from typing import Dict, List, Any


def reciprocal_rank_fusion(
    dense_results: List[Dict[str, Any]],
    sparse_results: List[Dict[str, Any]],
    k: int = 60
) -> List[Dict[str, Any]]:
    """
    Thuật toán Reciprocal Rank Fusion (RRF) để kết hợp kết quả từ Dense và Sparse retrieval.

    Công thức:
        RRF(d) = sum( 1 / (k + rank(d)) )

    Args:
        dense_results: Danh sách các chunk từ Qdrant (đã sort theo score giảm dần)
        sparse_results: Danh sách các chunk từ BM25 (đã sort theo score giảm dần)
        k: Hằng số làm mịn (thường chọn 60)

    Returns:
        Danh sách chunk đã được xếp hạng lại theo điểm RRF giảm dần.
    """
    rrf_scores: Dict[str, float] = {}
    chunk_map: Dict[str, Dict[str, Any]] = {}

    # 1. Tính điểm từ Dense Retrieval (thứ hạng tính từ 1)
    for rank, item in enumerate(dense_results, start=1):
        chunk_id = item["chunk_id"]
        chunk_map[chunk_id] = item
        rrf_scores[chunk_id] = rrf_scores.get(chunk_id, 0.0) + (1.0 / (k + rank))

    # 2. Tính điểm từ Sparse Retrieval (BM25)
    for rank, item in enumerate(sparse_results, start=1):
        chunk_id = item["chunk_id"]
        if chunk_id not in chunk_map:
            chunk_map[chunk_id] = item
        rrf_scores[chunk_id] = rrf_scores.get(chunk_id, 0.0) + (1.0 / (k + rank))

    # 3. Sắp xếp các chunk theo điểm RRF giảm dần
    sorted_chunks = sorted(
        chunk_map.values(),
        key=lambda x: rrf_scores[x["chunk_id"]],
        reverse=True
    )

    # Gán lại điểm rrf_score vào kết quả trả về
    for item in sorted_chunks:
        item["rrf_score"] = rrf_scores[item["chunk_id"]]

    return sorted_chunks
