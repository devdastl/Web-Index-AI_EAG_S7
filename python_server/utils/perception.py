import json
from typing import Dict, Any
from google import genai
from utils.prompt import query_prompt

def clean_code_block(text: str) -> str:
    """Clean JSON code block from LLM response"""
    if text.startswith("```json"):
        text = text[len("```json"):]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

def generate_with_timeout(client: genai.Client, prompt: str, timeout: int = 10) -> str:
    """Generate content with a timeout"""
    print("Starting LLM generation...")
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        print("LLM generation completed")
        return response.text.strip()
    except Exception as e:
        print(f"Error in LLM generation: {e}")
        raise

def perceive_input(client: genai.Client, user_input: str) -> str:
    """
    Process user input and extract key information using LLM
    Returns a structured perception result
    """
    prompt = query_prompt.replace("_user_query_", user_input)
    try:
        response_text = generate_with_timeout(client, prompt)
        response_text = clean_code_block(response_text)
        print(f"INFO: perception response: {response_text}")
        return str(response_text)
    except Exception as e:
        print(f"Error in perception: {e}")
        raise 