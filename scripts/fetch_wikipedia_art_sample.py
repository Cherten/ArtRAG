import json
import logging
import os
import re
from datasets import load_dataset
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ART_KEYWORDS = [
    "painting", "painter", "artist", "sculpture", "sculptor",
    "art movement", "renaissance", "baroque", "impressionism",
    "cubism", "surrealism", "abstract art", "portrait", "landscape"
]

def is_art_related(title, text):
    combined = (title + " " + text[:2000]).lower()
    return any(re.search(rf"\b{kw}\b", combined) for kw in ART_KEYWORDS)

def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = []
    current_chunk = []
    current_len = 0
    for word in words:
        current_chunk.append(word)
        current_len += len(word) + 1
        if current_len >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_len = 0
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def main(limit=100000, language="20220301.en"):
    logger.info(f"Загрузка датасета wikipedia/{language}...")
    dataset = load_dataset("wikipedia", language, split="train")

    if limit > 0:
        dataset = dataset.shuffle(seed=42).select(range(limit))

    art_articles = []
    all_chunks = []

    logger.info("Фильтрация статей об искусстве и чанкинг...")
    for idx, article in enumerate(tqdm(dataset)):
        title = article["title"]
        text = article["text"]
        if is_art_related(title, text):
            art_articles.append({
                "id": article["id"],
                "title": title,
                "url": article["url"],
                "text": text
            })
            for cid, chunk in enumerate(chunk_text(text)):
                all_chunks.append({
                    "doc_id": article["id"],
                    "chunk_id": cid,
                    "title": title,
                    "content": chunk,
                    "url": article["url"]
                })

    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/wikipedia_art_sample.jsonl", "w") as f:
        for a in art_articles:
            f.write(json.dumps(a) + "\n")

    os.makedirs("data/processed", exist_ok=True)
    with open("data/processed/chunks_sample.jsonl", "w") as f:
        for c in all_chunks:
            f.write(json.dumps(c) + "\n")

    logger.info(f"Сохранено статей: {len(art_articles)}, чанков: {len(all_chunks)}")

if __name__ == "__main__":
    import sys
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
    main(limit=limit)