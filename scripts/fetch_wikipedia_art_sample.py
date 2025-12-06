from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable, List

from datasets import load_dataset


KEYWORDS = ("painting", "painter", "art", "sculpture", "museum", "gallery")
DEFAULT_SPLIT = "train[:0.02%]"
RAW_PATH = Path("data/raw/wikipedia_art_sample.jsonl")
CHUNKS_PATH = Path("data/processed/chunks_sample.jsonl")


def ensure_dirs() -> None:
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    CHUNKS_PATH.parent.mkdir(parents=True, exist_ok=True)


def chunk_text(text: str, max_chars: int = 500) -> List[str]:
    words = text.split()
    chunks: List[str] = []
    buf: List[str] = []
    size = 0
    for word in words:
        word_len = len(word) + 1  # include space
        if buf and size + word_len > max_chars:
            chunks.append(" ".join(buf).strip())
            buf = [word]
            size = len(word)
        else:
            buf.append(word)
            size += word_len
    if buf:
        chunks.append(" ".join(buf).strip())
    return [c for c in chunks if c]


def save_jsonl(rows: Iterable[dict], path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main(sample_split: str = DEFAULT_SPLIT, max_chars: int = 500) -> None:
    ensure_dirs()
    ds = load_dataset(
        "legacy-datasets/wikipedia",
        "20220301.en",
        split=sample_split,
        trust_remote_code=True,
    )

    def keep(row: dict) -> bool:
        text = (row.get("title", "") + " " + row.get("text", "")).lower()
        return any(k in text for k in KEYWORDS)

    filtered = ds.filter(keep)

    raw_rows = [
        {
            "id": row["id"],
            "title": row["title"],
            "source_url": row.get("url"),
            "text": row["text"],
        }
        for row in filtered
    ]
    save_jsonl(raw_rows, RAW_PATH)

    chunk_rows = []
    for row in filtered:
        chunks = chunk_text(row["text"], max_chars=max_chars)
        for idx, chunk in enumerate(chunks):
            chunk_rows.append(
                {
                    "doc_id": row["id"],
                    "chunk_id": f"{row['id']}_{idx}",
                    "content": chunk,
                    "source_url": row.get("url"),
                }
            )
    save_jsonl(chunk_rows, CHUNKS_PATH)

    print(f"Saved {len(raw_rows)} raw docs to {RAW_PATH}")
    print(f"Saved {len(chunk_rows)} chunks to {CHUNKS_PATH}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch Wikipedia art subset, filter, and chunk for RAG."
    )
    parser.add_argument(
        "--split",
        dest="sample_split",
        default=DEFAULT_SPLIT,
        help="HF split to load (e.g., 'train', 'train[:1%]', default train[:0.02%]).",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=500,
        help="Max characters per chunk (length-based split).",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(sample_split=args.sample_split, max_chars=args.max_chars)

