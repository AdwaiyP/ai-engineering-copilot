from app.rag.embedder import Embedder
from app.rag.vector_store import VectorStore

class Retriever:

    def __init__(self):

        self.embedder = Embedder()
        self.vector_store = VectorStore()

    def index_chunks(self, chunks):

        texts = [
            chunk.content
            for chunk in chunks
        ]

        embeddings = self.embedder.encode(texts)

        self.vector_store.build(
            chunks,
            embeddings
        )
    def search(
            self,
            query: str,
            top_k: int = 5
    ):
        query_embedding = self.embedder.encode(
            [query]
        )[0]

        return self.vector_store.search(
            query_embedding,
            top_k
        )