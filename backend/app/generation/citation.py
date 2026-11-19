import re
from typing import List, Dict, Any


def extract_citations_from_answer(answer_text: str, available_chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Tìm kiếm các thẻ citation dạng [S1], [S2] trong câu trả lời của LLM
    và ánh xạ chính xác về chunk/document nguồn tương ứng.
    """
    # Tìm tất cả pattern [S1], [S2], ...
    matches = re.findall(r"\[S(\d+)\]", answer_text)
    citation_indices = sorted(list(set(int(m) for m in matches)))

    citations = []
    for idx in citation_indices:
        # Index bắt đầu từ 1, map về danh sách available_chunks (0-indexed)
        chunk_idx = idx - 1
        if 0 <= chunk_idx < len(available_chunks):
            chunk = available_chunks[chunk_idx]
            citations.append({
                "id": f"S{idx}",
                "document_title": chunk.get("title", "Unknown"),
                "heading": chunk.get("heading"),
                "source_url": chunk.get("source_url", ""),
                "chunk_id": chunk.get("chunk_id", "")
            })

    return citations
