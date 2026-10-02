import faiss
import numpy as np

from app.rag.chunker import CodeChunk

class VectorStore:
    def __init__(self):
        self.index = None
        self.chunks: list[CodeChunk] = []
    def build(
            self,
            chunks: list[CodeChunk],
            embeddings
    ):
        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)

        self.index.add(embeddings)

        self.chunks = chunks
    def search(
            self,
            query_embedding,
            top_k: int = 5
    ):
        if self.index is None:
            return []
        
        query_embedding = np.asarray(
            [query_embedding],
            dtype="float32"
        )

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0] 
        ):
            if index == -1:
                continue
            results.append(
                {
                    "score": float(score),
                    "chunk": self.chunks[index]
                }
            )
        return results