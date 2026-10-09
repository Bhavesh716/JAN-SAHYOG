"""
Starter knowledge-base update command.

Runs document ingestion and reports what was produced. In a later version,
add embedding generation, vector-store upserts, stale-document removal,
source validation, and scheduled updates.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
INGEST_SCRIPT = BASE_DIR / "scripts" / "ingest_documents.py"
MANIFEST = BASE_DIR / "data" / "processed" / "manifest.json"
CHUNKS = BASE_DIR / "data" / "processed" / "chunks.jsonl"


def main() -> int:
    result = subprocess.run([sys.executable, str(INGEST_SCRIPT)], cwd=BASE_DIR)
    if result.returncode != 0:
        print("Document ingestion failed. Knowledge base was not updated.")
        return result.returncode

    if not MANIFEST.exists() or not CHUNKS.exists():
        print("Expected ingestion outputs were not created.")
        return 1

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    print("\nKnowledge-base preparation complete.")
    print(f"Documents processed: {len(data.get('documents', []))}")
    print(f"Chunk file: {CHUNKS}")
    print("\nNext implementation steps:")
    print("1. Review source documents and metadata.")
    print("2. Generate embeddings for each chunk.")
    print("3. Upsert chunks into the configured vector store.")
    print("4. Remove outdated chunks and verify retrieval quality.")
    print("5. Record source versions and update timestamps.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
