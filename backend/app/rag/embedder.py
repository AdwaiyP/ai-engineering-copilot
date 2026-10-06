import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class Embedder:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=4096,
            token_pattern=r"(?u)\b[\w./_-]+\b",
            lowercase=False,
        )
        self.fitted = False

    def encode(self, texts: list[str]):
        if not texts:
            return np.empty((0, 0), dtype="float32")

        # First call is repository chunks → fit vocabulary.
        if not self.fitted:
            matrix = self.vectorizer.fit_transform(texts)
            self.fitted = True
        else:
            # Later calls, including user queries, use same vocabulary.
            matrix = self.vectorizer.transform(texts)

        embeddings = matrix.toarray().astype("float32")

        # Normalize so FAISS inner product behaves like cosine similarity.
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms[norms == 0] = 1.0

        return embeddings / norms