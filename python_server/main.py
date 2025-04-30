from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI()

# Enable CORS for Chrome extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["chrome-extension://*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    url: str

class SearchRequest(BaseModel):
    query: str

class SearchResult(BaseModel):
    url: str
    text: str

class SearchResponse(BaseModel):
    results: List[SearchResult]

@app.put("/api/send_url")
async def send_url(request: URLRequest):
    print(f"Received URL for processing: {request.url}")
    # Dummy response
    return {"status": "success", "message": "URL received for processing"}

@app.post("/api/get_context")
async def get_context(request: SearchRequest):
    print(f"Received search query: {request.query}")
    # Dummy response with example URLs and chunks
    return SearchResponse(
        results=[
            SearchResult(
                url="https://www.hostinger.in/tutorials/what-is-ollama",
                text="By running models locally, you maintain full data ownership and avoid the potential security risks associated with cloud storage. Offline AI tools like Ollama also help reduce latency and reliance on external servers, making them faster and more reliable."
            )
        ]
    )

@app.get("/api/get_status")
async def get_status(url: str):
    print(f"Checking status for URL: {url}")
    # Dummy response
    return {"status": "processed", "message": "URL has been processed"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 