from pydantic import BaseModel
from typing import List, Optional

class URLRequest(BaseModel):
    url: str

class SearchRequest(BaseModel):
    query: str

class SearchResult(BaseModel):
    url: str
    text: str

class SearchResponse(BaseModel):
    results: List[SearchResult]
