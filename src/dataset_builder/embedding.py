from sentence_transformers import SentenceTransformer

from dataset_builder.schema import ARTIFACT_VERSION
from dataset_builder.models import ChunkRecord, ChunkEmbedding


class Embedder:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_chunks(self, chunks: list[ChunkRecord]) -> list[ChunkEmbedding]:
        texts = [chunk.text for chunk in chunks]

        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True,
        )

        embedded_chunks: list[ChunkEmbedding] = []

        for chunk, vector in zip(chunks, vectors):
            embedded_chunks.append(
                ChunkEmbedding(
                    artifact_version=ARTIFACT_VERSION,
                    chunk_id=chunk.chunk_id,
                    doc_id=chunk.doc_id,
                    #text=chunk.text,
                    embedding=vector.tolist(),
                    metadata=chunk.metadata,
                )
            )

        return embedded_chunks