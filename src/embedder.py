from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts, batch_size=64, show_progress_bar=False):
        return self.model.encode(texts, batch_size=batch_size, show_progress_bar=show_progress_bar)