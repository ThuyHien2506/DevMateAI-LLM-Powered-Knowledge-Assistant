from typing import List, Set


def recall_at_k(retrieved_chunk_ids: List[str], ground_truth_chunk_ids: Set[str], k: int = 5) -> float:
    """
    Tính Recall@K: Tỷ lệ các chunk liên quan có mặt trong Top-K kết quả truy xuất.
    """
    if not ground_truth_chunk_ids:
        return 0.0

    top_k = retrieved_chunk_ids[:k]
    hits = sum(1 for cid in top_k if cid in ground_truth_chunk_ids)
    return hits / len(ground_truth_chunk_ids)


def mrr_at_k(retrieved_chunk_ids: List[str], ground_truth_chunk_ids: Set[str], k: int = 5) -> float:
    """
    Tính Mean Reciprocal Rank (MRR@K): Đánh giá vị trí xuất hiện của kết quả đúng ĐẦU TIÊN.
    Nếu kết quả đúng đầu tiên nằm ở vị trí 1 -> score = 1/1 = 1.0
    Nếu ở vị trí 2 -> score = 1/2 = 0.5
    Nếu không xuất hiện trong Top K -> score = 0.0
    """
    top_k = retrieved_chunk_ids[:k]
    for rank, cid in enumerate(top_k, start=1):
        if cid in ground_truth_chunk_ids:
            return 1.0 / rank
    return 0.0
