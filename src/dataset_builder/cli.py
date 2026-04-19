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
    
"""import sys
from pathlib import Path

from dataset_builder.config import BuildConfig, load_config
from dataset_builder.embeddings import embed_chunks
from dataset_builder.pipeline import DatasetBuilderPipeline


def parse_multi_flag(args: list[str], flag: str) -> list[str]:
    values = []
    i = 0
    while i < len(args):
        if args[i] == flag and i + 1 < len(args):
            values.append(args[i + 1])
            i += 2
        else:
            i += 1
    return values


def parse_single_flag(args: list[str], flag: str, default=None):
    i = 0
    while i < len(args):
        if args[i] == flag and i + 1 < len(args):
            return args[i + 1]
        i += 1
    return default


def run_build(args: list[str]) -> None:
    config_path = parse_single_flag(args, "--config")
    output_dir = parse_single_flag(args, "--output-dir", "output")

    websites = parse_multi_flag(args, "--website")
    pdfs = parse_multi_flag(args, "--pdf")
    texts = parse_multi_flag(args, "--text")
    youtubes = parse_multi_flag(args, "--youtube")

    cfg = load_config(config_path) if config_path else BuildConfig()

    for value in websites:
        cfg.sources.append({"kind": "website", "value": value})
    for value in pdfs:
        cfg.sources.append({"kind": "pdf", "value": value})
    for value in texts:
        cfg.sources.append({"kind": "text", "value": value})
    for value in youtubes:
        cfg.sources.append({"kind": "youtube", "value": value})

    pipeline = DatasetBuilderPipeline(BuildConfig.model_validate(cfg.model_dump()))
    results = pipeline.build(output_dir)

    print("Build complete")
    for name, path in results.items():
        print(f"- {name}: {Path(path)}")


def run_embed(args: list[str]) -> None:
    chunks = parse_single_flag(args, "--chunks")
    model = parse_single_flag(
        args,
        "--model",
        "sentence-transformers/all-MiniLM-L6-v2",
    )
    output = parse_single_flag(args, "--output")

    if not chunks:
        print("Error: --chunks is required for embed")
        sys.exit(1)

    path = embed_chunks(chunks_path=chunks, model_name=model, output_path=output)
    print(f"Embeddings written to: {path}")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python cli_manual.py build [options]")
        print("  python cli_manual.py embed [options]")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    if command == "build":
        run_build(args)
    elif command == "embed":
        run_embed(args)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()"""
