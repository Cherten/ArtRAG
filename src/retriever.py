import json
import os
import faiss
from .embedder import Embedder

class Retriever:
    def __init__(self, index_dir="data/index"):
        self.index = faiss.read_index(os.path.join(index_dir, "art.index"))
        with open(os.path.join(index_dir, "chunks_meta.json"), "r") as f:
            self.chunks = json.load(f)
        with open(os.path.join(index_dir, "model_name.txt"), "r") as f:
            model_name = f.read().strip()
        self.embedder = Embedder(model_name)

    def retrieve(self, query, k=5):
        emb = self.embedder.encode([query])
        distances, indices = self.index.search(emb.astype('float32'), k)
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            results.append({
                "chunk": self.chunks[idx],
                "score": float(dist)
            })
        return results