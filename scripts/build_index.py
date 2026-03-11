import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

def main():
    with open("data/processed/chunks_sample.jsonl", "r") as f:
        chunks = [json.loads(line) for line in f]

    texts = [chunk["content"] for chunk in chunks]

    model_name = "all-MiniLM-L6-v2"
    model = SentenceTransformer(model_name)

    embeddings = model.encode(texts, show_progress_bar=True, batch_size=64)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype('float32'))

    os.makedirs("data/index", exist_ok=True)
    faiss.write_index(index, "data/index/art.index")

    with open("data/index/chunks_meta.json", "w") as f:
        json.dump(chunks, f)

    with open("data/index/model_name.txt", "w") as f:
        f.write(model_name)

    print(f"Индекс построен. Всего чанков: {len(chunks)}")

if __name__ == "__main__":
    main()