from .retriever import Retriever
from .generator import Generator

class RAGPipeline:
    def __init__(self, retriever=None, generator=None):
        self.retriever = retriever if retriever is not None else Retriever()
        self.generator = generator if generator is not None else Generator()

    def answer(self, question, k=5):
        chunks = self.retriever.retrieve(question, k)
        answer = self.generator.generate(question, chunks)
        return {
            "question": question,
            "answer": answer,
            "sources": [c["chunk"]["url"] for c in chunks]
        }