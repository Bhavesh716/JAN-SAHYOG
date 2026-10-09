"""
Starter document-ingestion pipeline for JAN SAHYOG.

Reads PDF, TXT, and Markdown files from data/source_documents, extracts text,
splits it into simple chunks, and writes JSONL records to data/processed.

This script does NOT automatically verify whether a document is official.
Only place documents from sources you have reviewed and are permitted to use.
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

BASE_DIR = Path(__file__).resolve().parents[1]
SOURCE_DIR = BASE_DIR / os.getenv("KNOWLEDGE_SOURCE_DIR", "data/source_documents")
OUTPUT_DIR = BASE_DIR / os.getenv("KNOWLEDGE_PROCESSED_DIR", "data/processed")
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 180
SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf"}


def read_text(path: Path) -> str:
    """Extract text from a supported file. PDF support requires pypdf."""
    if path.suffix.lower() in {".txt", ".md"}:
        return path.read_text(encoding="utf-8", errors="replace")

    if path.suffix.lower() == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise RuntimeError(
                "PDF ingestion requires pypdf. Install it with: pip install pypdf"
            ) from exc

        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    raise ValueError(f"Unsupported file type: {path.suffix}")


def split_into_chunks(text: str, size: int = CHUNK_SIZE,
                      overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Simple character-based chunking; replace with token-aware chunking later."""
    cleaned = "\n".join(line.strip() for line in text.splitlines() if line.strip())
    if not cleaned:
        return []
    if overlap >= size:
        raise ValueError("CHUNK_OVERLAP must be smaller than CHUNK_SIZE")

    chunks = []
    start = 0
    while start < len(cleaned):
        end = min(start + size, len(cleaned))
        chunk = cleaned[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(cleaned):
            break
        start = end - overlap
    return chunks


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def iter_source_files() -> Iterable[Path]:
    if not SOURCE_DIR.exists():
        SOURCE_DIR.mkdir(parents=True, exist_ok=True)
        return []
    return sorted(
        path for path in SOURCE_DIR.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def ingest() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "chunks.jsonl"
    manifest_path = OUTPUT_DIR / "manifest.json"
    records = []
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_directory": str(SOURCE_DIR.relative_to(BASE_DIR)),
        "documents": [],
        "notes": [
            "Source trust and current validity must be reviewed by a human.",
            "Scanned PDFs may require OCR; this starter only extracts embedded PDF text."
        ],
    }

    for path in iter_source_files():
        try:
            text = read_text(path)
        except Exception as exc:
            print(f"[WARN] Skipping {path.name}: {exc}")
            continue

        doc_id = sha256_file(path)
        chunks = split_into_chunks(text)
        relative_path = str(path.relative_to(BASE_DIR))

        manifest["documents"].append({
            "document_id": doc_id,
            "file": relative_path,
            "sha256": doc_id,
            "chunk_count": len(chunks),
            "characters": len(text),
            "ingested_at": datetime.now(timezone.utc).isoformat(),
        })

        for index, chunk in enumerate(chunks):
            records.append({
                "chunk_id": f"{doc_id[:16]}-{index:04d}",
                "document_id": doc_id,
                "source_file": relative_path,
                "chunk_index": index,
                "text": chunk,
                "metadata": {
                    "file_name": path.name,
                    "file_type": path.suffix.lower(),
                    "source_reviewed": False,
                },
            })

    with output_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Ingested {len(manifest['documents'])} documents into {len(records)} chunks.")
    print(f"Chunks: {output_path}")
    print(f"Manifest: {manifest_path}")
    return len(records)


if __name__ == "__main__":
    ingest()
