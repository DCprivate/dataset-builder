from __future__ import annotations

from dataset_builder.config import ChunkingConfig
from dataset_builder.models import ChunkRecord, NormalizedDocument


class RecursiveCharacterChunker:
    def __init__(self, config: ChunkingConfig):
        self.chunk_size = config.chunk_size
        self.chunk_overlap = config.chunk_overlap
        self.min_chunk_chars = config.min_chunk_chars

    @staticmethod
    def estimate_tokens(text: str) -> int:
        return max(1, len(text) // 4)

    def _split_paragraphs(self, text: str) -> list[str]:
        return [part.strip() for part in text.split("\n\n") if part.strip()]

    def chunk_document(self, doc: NormalizedDocument) -> list[ChunkRecord]:
        paragraphs = self._split_paragraphs(doc.text)
        chunks: list[ChunkRecord] = []

        buffer = ""
        chunk_index = 0
        char_cursor = 0

        for para in paragraphs:
            candidate = f"{buffer}\n\n{para}".strip() if buffer else para
            if len(candidate) <= self.chunk_size:
                buffer = candidate
                continue

            if buffer and len(buffer) >= self.min_chunk_chars:
                chunk_index += 1
                start = max(0, char_cursor - len(buffer))
                end = start + len(buffer)
                chunks.append(
                    ChunkRecord(
                        chunk_id=f"{doc.doc_id}:{chunk_index:04d}",
                        doc_id=doc.doc_id,
                        text=buffer,
                        token_estimate=self.estimate_tokens(buffer),
                        metadata={
                            "source_type": doc.source_type,
                            "source_uri": doc.source_uri,
                            "title": doc.title,
                            "chunk_index": chunk_index,
                            "char_start": start,
                            "char_end": end,
                        },
                    )
                )
                overlap = buffer[-self.chunk_overlap :] if self.chunk_overlap else ""
                buffer = f"{overlap}\n\n{para}".strip()
            else:
                long_text = candidate
                start_idx = 0
                step = max(1, self.chunk_size - self.chunk_overlap)
                while start_idx < len(long_text):
                    piece = long_text[start_idx : start_idx + self.chunk_size].strip()
                    if len(piece) >= self.min_chunk_chars:
                        chunk_index += 1
                        chunks.append(
                            ChunkRecord(
                                chunk_id=f"{doc.doc_id}:{chunk_index:04d}",
                                doc_id=doc.doc_id,
                                text=piece,
                                token_estimate=self.estimate_tokens(piece),
                                metadata={
                                    "source_type": doc.source_type,
                                    "source_uri": doc.source_uri,
                                    "title": doc.title,
                                    "chunk_index": chunk_index,
                                    "char_start": start_idx,
                                    "char_end": min(len(long_text), start_idx + len(piece)),
                                },
                            )
                        )
                    start_idx += step
                buffer = ""

            char_cursor += len(candidate)

        if buffer and len(buffer) >= self.min_chunk_chars:
            chunk_index += 1
            chunks.append(
                ChunkRecord(
                    chunk_id=f"{doc.doc_id}:{chunk_index:04d}",
                    doc_id=doc.doc_id,
                    text=buffer,
                    token_estimate=self.estimate_tokens(buffer),
                    metadata={
                        "source_type": doc.source_type,
                        "source_uri": doc.source_uri,
                        "title": doc.title,
                        "chunk_index": chunk_index,
                        "char_start": max(0, len(doc.text) - len(buffer)),
                        "char_end": len(doc.text),
                    },
                )
            )

        return chunks
