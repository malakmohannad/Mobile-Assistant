from rank_bm25 import BM25Okapi

class BM25Search:
    def __init__(self, documents: list[str]):
        self.documents = documents
        tokenized=[doc.lower().split() for doc in documents]
        self.bm25 = BM25Okapi(tokenized)

    def search(self, query: str) -> list[int]:
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)
        ranked_indices = [i for i, score in sorted(enumerate(scores), key=lambda x: x[1], reverse=True)]
        return ranked_indices