import json
from pathlib import Path
#from dataset_builder.models import NormalizedDocument
#from dataset_builder.utils import sha256_text

from dataset_builder.io import load_sources, write_jsonl, read_jsonl, ensure_dir, load_chunks_jsonl
from dataset_builder.registry import ingest_source
from dataset_builder.pipeline import build_documents
from dataset_builder.chunking import Chunker
from dataset_builder.embedding import Embedder
from dataset_builder.ingest.text import TextIngester
from dataset_builder.ingest.pdf import PdfIngester
from dataset_builder.ingest.web import WebsiteIngester
from dataset_builder.ingest.youtube import YouTubeIngester

"""
IMPORTANT: 
Make embedding optional
Put the chunking policy (when that is implemented) in the schema?

"""

def main():
    # set output directory
    out_dir = ensure_dir("../output")
    
    # load sources
    sources = load_sources("../config/sources.json")
    documents, failures = build_documents(sources)
    
    path_to_documents = write_jsonl(documents, out_dir / "documents.jsonl")
    path_to_failures = write_jsonl(failures, out_dir / "failures.jsonl")
    
    # chunk sources
    chunker = Chunker(chunk_size=900, chunk_overlap=200, min_chunk_chars=100)
    chunks = chunker.chunk_documents(documents)
    
    # write chunks to jsonl file
    path_to_chunks = write_jsonl(chunks, out_dir / "chunks.jsonl")
    
    # read chunks from jsonl file
    chunks_for_embedding = load_chunks_jsonl(out_dir / "chunks.jsonl")
    
    # embed chunks
    embedder = Embedder()
    embedded_chunks = embedder.embed_chunks(chunks_for_embedding)

    # save embeddings
    write_jsonl(embedded_chunks, out_dir / "embeddings.jsonl")

if __name__ == "__main__":
    main()