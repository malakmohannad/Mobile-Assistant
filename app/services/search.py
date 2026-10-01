from app.data.devices import DEVICE_DOCUMENTS
from app.utils.bm25_index import BM25Search
from app.utils.embeddings import DenseSearch

K=60
_bm25=BM25Search(DEVICE_DOCUMENTS)
_dense=DenseSearch(DEVICE_DOCUMENTS)

def hybrid_search(query: str,k: int=3) -> list[tuple[str, float]]:
    sparse_ranked = _bm25.search(query)
    dense_ranked = _dense.search(query)

    combined_results = {}
    for rank, idx in enumerate(sparse_ranked):
        combined_results[idx] = combined_results.get(idx, 0) + 1/ (K + rank)
    for rank, idx in enumerate(dense_ranked):
        combined_results[idx] = combined_results.get(idx, 0) + 1/ (K + rank)

    ranked = sorted(combined_results.items(), key=lambda x: x[1], reverse=True)
    top = ranked[:k]
    return [(DEVICE_DOCUMENTS[idx], score) for idx, score in top]