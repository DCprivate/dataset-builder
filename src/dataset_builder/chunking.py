from dataset_builder.schema import ARTIFACT_VERSION
from dataset_builder.models import NormalizedDocument, ChunkRecord, ChunkEmbedding


class Chunker:
    def __init__(self, chunk_size: int = 900, chunk_overlap: int = 150, min_chunk_chars: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_chars = min_chunk_chars

    @staticmethod
    def estimate_tokens(text: str) -> int:
        return max(1, len(text) // 4)

    @staticmethod
    def split_paragraphs(text: str) -> list[str]:
        return [part.strip() for part in text.split("\n\n") if part.strip()]


    def chunk_document(self, doc: NormalizedDocument) -> list[ChunkRecord]:
        if not isinstance(doc, NormalizedDocument):
            raise TypeError(f"Expected NormalizedDocument, got {type(doc)}")
        
        paragraphs = self.split_paragraphs(doc.text)
        chunks: list[ChunkRecord] = []

        buffer = ""
        chunk_index = 0

        for para in paragraphs:
            candidate = f"{buffer}\n\n{para}".strip() if buffer else para

            if len(candidate) <= self.chunk_size:
                buffer = candidate
                continue

            if buffer and len(buffer) >= self.min_chunk_chars:
                chunk_index += 1
                chunks.append(
                    ChunkRecord(
                        artifact_version=ARTIFACT_VERSION,
                        chunk_id=f"{doc.doc_id}:{chunk_index:04d}",
                        doc_id=doc.doc_id,
                        text=buffer,
                        token_estimate=self.estimate_tokens(buffer),
                        metadata={
                            "source_type": doc.source_type,
                            "source_uri": doc.source_uri,
                            "title": doc.title,
                            "chunk_index": chunk_index,
                        },
                    )
                )

                overlap = buffer[-self.chunk_overlap:] if self.chunk_overlap else ""
                buffer = f"{overlap}\n\n{para}".strip()
            else:
                # paragraph itself is too large; hard split it
                start = 0
                step = max(1, self.chunk_size - self.chunk_overlap)

                while start < len(candidate):
                    piece = candidate[start:start + self.chunk_size].strip()
                    if len(piece) >= self.min_chunk_chars:
                        chunk_index += 1
                        chunks.append(
                            ChunkRecord(
                                artifact_version=ARTIFACT_VERSION,
                                chunk_id=f"{doc.doc_id}:{chunk_index:04d}",
                                doc_id=doc.doc_id,
                                text=piece,
                                token_estimate=self.estimate_tokens(piece),
                                metadata={
                                    "source_type": doc.source_type,
                                    "source_uri": doc.source_uri,
                                    "title": doc.title,
                                    "chunk_index": chunk_index,
                                },
                            )
                        )
                    start += step

                buffer = ""

        if buffer and len(buffer) >= self.min_chunk_chars:
            chunk_index += 1
            chunks.append(
                ChunkRecord(
                    artifact_version=ARTIFACT_VERSION,
                    chunk_id=f"{doc.doc_id}:{chunk_index:04d}",
                    doc_id=doc.doc_id,
                    text=buffer,
                    token_estimate=self.estimate_tokens(buffer),
                    metadata={
                        "source_type": doc.source_type,
                        "source_uri": doc.source_uri,
                        "title": doc.title,
                        "chunk_index": chunk_index,
                    },
                )
            )

        return chunks
    
    
    def chunk_documents(self, documents: list[NormalizedDocument]) -> list[ChunkRecord]:
        all_chunks = []

        for doc in documents:
            all_chunks.extend(self.chunk_document(doc))

        return all_chunks
    

    def print_chunks(self, chunks: ChunkEmbedding):
        for chunk in chunks[:3]:
            print("-" * 80)
            print(f"chunk_id: {chunk.chunk_id}")
            print(f"token_estimate: {chunk.token_estimate}")
            print(f"text preview: {chunk.text[:200]}")
            print(f"metadata: {str(chunk.metadata)[:120]}")