from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests
from markitdown import MarkItDown
import os
from dotenv import load_dotenv
from google import genai
import logging
import traceback

from utils.model import *
from utils.memory import MemoryManager
from utils.perception import perceive_input
from utils.prompt import query_prompt, result_prompt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

#initialize the app
app = FastAPI()
markitdown_instance = MarkItDown()
memory_manager = MemoryManager(chunk_size=256, overlap=40)

# Load environment variables
try:
    load_dotenv("../token.env")
    api_key = os.getenv("API_TOKEN")
    if not api_key:
        raise ValueError("API_TOKEN not found in environment variables")
    client = genai.Client(api_key=api_key)
    logger.info("Successfully initialized Google AI client")
except Exception as e:
    logger.error(f"Failed to initialize environment: {str(e)}")
    raise

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
    logger.info(f"Received URL for processing: {request.url}")
    try:
        # Fetch HTML content from the URL
        response = requests.get(request.url)
        response.raise_for_status()
        html_content = response.text
        logger.info(f"Successfully fetched HTML content from {request.url}")

        #save html content to a file and get absolute file path
        html_file_path = os.path.abspath("content.html")
        try:
            with open(html_file_path, "w") as file:
                file.write(html_content)
            logger.info(f"Saved HTML content to {html_file_path}")
        except IOError as e:
            logger.error(f"Failed to write HTML file: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error saving content: {str(e)}")
        
        # Convert HTML to markdown
        try:
            markdown_content = markitdown_instance.convert(html_file_path)
            logger.info("Successfully converted HTML to markdown")
        except Exception as e:
            logger.error(f"Failed to convert HTML to markdown: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error converting content: {str(e)}")

        #add the memory to the memory manager
        try:
            status = memory_manager.add_memory(markdown_content.text_content, request.url)
            logger.info(f"Memory addition status: {status}")
        except Exception as e:
            logger.error(f"Failed to add memory: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error adding memory: {str(e)}")

        #delete the html file
        try:
            os.remove(html_file_path)
            logger.info(f"Cleaned up temporary HTML file: {html_file_path}")
        except OSError as e:
            logger.warning(f"Failed to remove temporary HTML file: {str(e)}")

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
        logger.error(f"Request error for URL {request.url}: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error fetching URL: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error processing URL {request.url}: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error processing content: {str(e)}")

@app.post("/api/get_context")
async def get_context(request: SearchRequest):
    logger.info(f"Received search query: {request.query}")

    try:
        #Refine the query
        refined_query = perceive_input(client, query_prompt.replace("_user_query_", request.query))
        logger.info(f"Refined query: {refined_query}")

        # Get context from memory
        context = memory_manager.retrieve_memories(refined_query, 1)
        logger.info(f"Retrieved {len(context)} context items")

        #join the context into a single string
        joined_context = "\n".join([item["data"] for item in context])

        #query with context
        context_query = result_prompt.replace("_user_query_", request.query).replace("_context_", joined_context)
        query_result = perceive_input(client, context_query)
        logger.info(f"Generated result for query")

        urls = [item["url"] for item in context]
        result = SearchResult(
                url=list(set(urls)),
                text=query_result
            )
        return result
    except Exception as e:
        logger.error(f"Error processing search query: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error processing search: {str(e)}")

@app.get("/api/get_status")
async def get_status(url: str):
    logger.info(f"Checking status for URL: {url}")
    try:
        # Dummy response
        return {"status": "processed", "message": "URL has been processed"}
    except Exception as e:
        logger.error(f"Error checking status for URL {url}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error checking status: {str(e)}")

@app.get("/api/health")
async def health():
    logger.info("Health check requested")
    return {"status": "ok"}

if __name__ == "__main__":
    logger.info("Starting FastAPI server")
    uvicorn.run("agent:app", host="0.0.0.0", port=8000, reload=True) 