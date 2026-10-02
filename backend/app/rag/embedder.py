from sentence_transformers import SentenceTransformer

from app.config import settings

class Embedder:

    def __init__(self):
        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL
        )
    def encode(self, texts: list[str]):
        return self.model.encode(
            texts,
            normalize_embeddings=True
        )