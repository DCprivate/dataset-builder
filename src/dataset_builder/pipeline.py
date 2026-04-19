from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from tqdm import tqdm

from dataset_builder.chunking import RecursiveCharacterChunker
from dataset_builder.config import BuildConfig, SourceSpec
from dataset_builder.io import ensure_dir, write_jsonl, write_parquet
from dataset_builder.models import ChunkRecord, NormalizedDocument
from dataset_builder.registry import resolve_ingester


class DatasetBuilderPipeline:
    def __init__(self, config: BuildConfig):
        self.config = config
        self.chunker = RecursiveCharacterChunker(config.chunking)

    def ingest_source(self, source: SourceSpec) -> NormalizedDocument:
        ingester_cls = resolve_ingester(source.kind)
        return ingester_cls().ingest(source.value)

    def build(self, output_dir: str | Path) -> dict[str, Path]:
        out_dir = ensure_dir(output_dir)

        documents: list[NormalizedDocument] = []
        chunks: list[ChunkRecord] = []
        failures: list[dict] = []

        for source in tqdm(self.config.sources, desc="Ingesting sources"):
            try:
                doc = self.ingest_source(source)
                documents.append(doc)
                chunks.extend(self.chunker.chunk_document(doc))
            except Exception as exc:  # noqa: BLE001
                failures.append({"kind": source.kind, "value": source.value, "error": str(exc)})

        docs_path = out_dir / "documents.jsonl"
        chunks_jsonl_path = out_dir / "chunks.jsonl"
        chunks_parquet_path = out_dir / "chunks.parquet"
        failures_path = out_dir / "failures.jsonl"

        write_jsonl((doc.to_dict() for doc in documents), docs_path)
        write_jsonl((chunk.to_dict() for chunk in chunks), chunks_jsonl_path)
        parquet_result = write_parquet([chunk.to_dict() for chunk in chunks], chunks_parquet_path)
        write_jsonl(failures, failures_path)

        return {
            "documents": docs_path,
            "chunks_jsonl": chunks_jsonl_path,
            "chunks_parquet": chunks_parquet_path if parquet_result == "parquet" else Path(parquet_result),
            "failures": failures_path,
        }


def build_config_from_args(
    websites: list[str],
    pdfs: list[str],
    texts: list[str],
    youtubes: list[str],
    base_config: BuildConfig | None = None,
) -> BuildConfig:
    config = base_config or BuildConfig()
    config.sources.extend([{"kind": "website", "value": v} for v in websites])
    config.sources.extend([{"kind": "pdf", "value": v} for v in pdfs])
    config.sources.extend([{"kind": "text", "value": v} for v in texts])
    config.sources.extend([{"kind": "youtube", "value": v} for v in youtubes])
    return BuildConfig.model_validate(asdict(config) if hasattr(config, "__dataclass_fields__") else config.model_dump())
