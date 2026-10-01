from typing import Dict,List, Literal
from pydantic import BaseModel, Field,field_validator
MAX_INPUT_CHARS=500
class Device(BaseModel):
    brand: str = Field(..., min_length=1,examples=["Samsung"])
    model: str = Field(..., min_length=1,examples=["Galaxy S24 Ultra"])
    specs: Dict[str, str] = Field(default_factory=dict,examples=[{"display": "6.8 inch OLED"}])
    release_year: int = Field(..., ge=2000, le=2100,examples=[2024])
    price_tier: Literal["budget", "mid-range", "flagship"] = Field(...,examples=["flagship"])

    @field_validator("brand", "model")
    @classmethod
    def strip(cls, v: str) -> str:
        v=v.strip()
        if not v:
            raise ValueError("Field cannot be empty or whitespace")
        return v

class ExtractRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=MAX_INPUT_CHARS)

class ExtractResponse(Device):
    pass

class SearchRequest(BaseModel):
    q: str = Field(..., min_length=1, max_length=MAX_INPUT_CHARS)

class SearchResult(BaseModel):
    document:str
    score:float

class SearchResponse(BaseModel):
    results: List[SearchResult]