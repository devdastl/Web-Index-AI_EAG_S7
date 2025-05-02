import json
from typing import Dict, Any
from google import genai
import logging
import traceback

# Configure logger
logger = logging.getLogger(__name__)

def clean_code_block(text: str) -> str:
    """Clean JSON code block from LLM response"""
    try:
        if text.startswith("```json"):
            text = text[len("```json"):]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()
    except Exception as e:
        logger.error(f"Error cleaning code block: {str(e)}")
        raise

def generate_with_timeout(client: genai.Client, prompt: str, timeout: int = 10) -> str:
    """Generate content with a timeout"""
    logger.info("Starting LLM generation...")
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        logger.info("LLM generation completed successfully")
        return response.text.strip()
    except genai.GenerativeError as e:
        logger.error(f"Error in LLM generation: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in LLM generation: {str(e)}\n{traceback.format_exc()}")
        raise

def perceive_input(client: genai.Client, prompt: str) -> str:
    """
    Process user input and extract key information using LLM
    Returns a structured perception result
    """
    try:
        response_text = generate_with_timeout(client, prompt)
        response_text = clean_code_block(response_text)
        logger.info(f"Successfully processed perception response")
        return str(response_text)
    except Exception as e:
        logger.error(f"Error in perception: {str(e)}\n{traceback.format_exc()}")
        raise 