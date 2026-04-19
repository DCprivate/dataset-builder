from __future__ import annotations

from pathlib import Path

import pandas as pd


def embed_chunks(chunks_path: str | Path, model_name: str, output_path: str | Path | None = None) -> Path:
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "Embedding support is not installed. Run: pip install -e .[embeddings]"
        ) from exc

    chunks_path = Path(chunks_path)
    output_path = Path(output_path) if output_path else chunks_path.with_name("embeddings.parquet")

    df = pd.read_parquet(chunks_path) if chunks_path.suffix == ".parquet" else pd.read_json(chunks_path, lines=True)
    model = SentenceTransformer(model_name)
    vectors = model.encode(df["text"].tolist(), normalize_embeddings=True, show_progress_bar=True)

    out = pd.DataFrame(
        {
            "chunk_id": df["chunk_id"],
            "doc_id": df["doc_id"],
            "text": df["text"],
            "embedding": list(vectors),
        }
    )
    out.to_parquet(output_path, index=False)
    return output_path
