from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

from app.schema.device import ExtractRequest, ExtractResponse, SearchRequest, SearchResponse, SearchResult
from app.services.extraction import extract_device
from app.services.search import hybrid_search
from app.utils.security import is_suspicious

load_dotenv()

app = FastAPI()

@app.post("/extract", response_model=ExtractResponse)
def extract(req: ExtractRequest):
    if is_suspicious(req.text):
        raise HTTPException(status_code=400, detail="Suspicious input detected.")
    try:
        device = extract_device(req.text)
        return device
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/search", response_model=SearchResponse)
def search(req: SearchRequest):
    results = hybrid_search(req.q)
    return SearchResponse(results=[SearchResult(document=document, score=score) for document, score in results])