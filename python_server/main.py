from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests
from markitdown import MarkItDown
import os
from dotenv import load_dotenv
from google import genai

from utils.model import *
from utils.memory import MemoryManager
from utils.perception import perceive_input

#initialize the app
app = FastAPI()
markitdown_instance = MarkItDown()
memory_manager = MemoryManager()

# Load environment variables
load_dotenv("../token.env")
api_key = os.getenv("API_TOKEN")
client = genai.Client(api_key=api_key)

# Enable CORS for Chrome extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["chrome-extension://*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.put("/api/send_url")
async def send_url(request: URLRequest):
    print(f"Received URL for processing: {request.url}")
    try:
        # Fetch HTML content from the URL
        response = requests.get(request.url)
        response.raise_for_status()  # Raise exception for bad status codes
        html_content = response.text

        #save html content to a file and get absolute file path
        html_file_path = os.path.abspath("content.html")
        with open(html_file_path, "w") as file:
            file.write(html_content)
        
        # Convert HTML to markdown
        markdown_content = markitdown_instance.convert(html_file_path)

        #add the memory to the memory manager
        status = memory_manager.add_memory(markdown_content.text_content, request.url)

        #delete the html file
        os.remove(html_file_path)

        if status:
            return {
                "status": "success", 
                "message": "URL processed successfully"
            }
        else:
            return {
                "status": "error", 
                "message": "URL already exists"
            }

    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error fetching URL: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing content: {str(e)}")

@app.post("/api/get_context")
async def get_context(request: SearchRequest):
    print(f"Received search query: {request.query}")

    #Refine the query
    refined_query = perceive_input(client, request.query)
    print(f"Refined query: {refined_query}")

    # Get context from memory
    context = memory_manager.retrieve_memories(refined_query, 2)
    results = []
    for item in context:
        results.append(SearchResult(
            url=item["url"],
            text=item["data"]
        ))

    # Dummy response with example URLs and chunks
    return results

@app.get("/api/get_status")
async def get_status(url: str):
    print(f"Checking status for URL: {url}")
    # Dummy response
    return {"status": "processed", "message": "URL has been processed"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 