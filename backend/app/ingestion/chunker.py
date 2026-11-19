from typing import List, Dict, Any


def chunk_document_by_heading_and_tokens(
    content: str,
    title: str,
    source_url: str,
    max_tokens: int = 500,
    overlap_tokens: int = 50
) -> List[Dict[str, Any]]:
    """
    Hàm phân đoạn văn bản kỹ thuật (Chunking):
    Ưu tiên tách theo Heading (#, ##, ###) để giữ trọn vẹn ngữ cảnh của từng phần/hàm/API.
    """
    # Khung sườn ban đầu, sẽ bổ sung tokenizer thực tế ở Ngày 5
    chunks = []
    paragraphs = content.split("\n\n")

    for idx, p in enumerate(paragraphs):
        p_clean = p.strip()
        if not p_clean:
            continue
        chunks.append({
            "chunk_id": f"chunk_{idx}",
            "title": title,
            "source_url": source_url,
            "content": p_clean,
        })
    return chunks
