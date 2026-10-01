from sentence_transformers import SentenceTransformer
import numpy as np

class DenseSearch:
    def __init__(self,documents: list[str], model_name: str = 'BAAI/bge-small-en-v1.5'):
        self.documents = documents
        self.model = SentenceTransformer(model_name)
        self.doc_embeddings = self.model.encode(documents, normalize_embeddings=True)

    def search(self, query: str) -> list[int]:
        query_embedding = self.model.encode([query], normalize_embeddings=True)
        similarities = np.dot(self.doc_embeddings, query_embedding.T).flatten()
        ranked_indices = [i for i, score in sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)]
        return ranked_indices