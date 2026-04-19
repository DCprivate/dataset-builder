from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from dataset_builder.config import BuildConfig, load_config
from dataset_builder.embeddings import embed_chunks
from dataset_builder.pipeline import DatasetBuilderPipeline

app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command()
def build(
    config: Annotated[str | None, typer.Option(help="Path to YAML config")] = None,
    output_dir: Annotated[str, typer.Option(help="Output directory")] = "output",
    website: Annotated[list[str] | None, typer.Option(help="Website URL(s)")] = None,
    pdf: Annotated[list[str] | None, typer.Option(help="PDF file path(s)")] = None,
    text: Annotated[list[str] | None, typer.Option(help="Text file path(s)")] = None,
    youtube: Annotated[list[str] | None, typer.Option(help="YouTube URL(s)")] = None,
) -> None:
    cfg = load_config(config) if config else BuildConfig()

    for value in website or []:
        cfg.sources.append({"kind": "website", "value": value})
    for value in pdf or []:
        cfg.sources.append({"kind": "pdf", "value": value})
    for value in text or []:
        cfg.sources.append({"kind": "text", "value": value})
    for value in youtube or []:
        cfg.sources.append({"kind": "youtube", "value": value})

    pipeline = DatasetBuilderPipeline(BuildConfig.model_validate(cfg.model_dump()))
    results = pipeline.build(output_dir)

    typer.echo("Build complete")
    for name, path in results.items():
        typer.echo(f"- {name}: {Path(path)}")


@app.command()
def embed(
    chunks: Annotated[str, typer.Option(help="Path to chunks.parquet or chunks.jsonl")],
    model: Annotated[str, typer.Option(help="SentenceTransformers model name")] = "sentence-transformers/all-MiniLM-L6-v2",
    output: Annotated[str | None, typer.Option(help="Output parquet path")] = None,
) -> None:
    path = embed_chunks(chunks_path=chunks, model_name=model, output_path=output)
    typer.echo(f"Embeddings written to: {path}")


if __name__ == "__main__":
    app()
