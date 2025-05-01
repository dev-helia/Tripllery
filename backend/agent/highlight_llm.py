"""
highlight_llm.py · OpenAI-powered Highlight Extractor

This module provides an asynchronous function to extract high-quality travel highlights
from raw text content such as user reviews or fallback POI descriptions.

It leverages the OpenAI Chat API to generate:
- A one-sentence summary suitable for display in a POI recommendation card
- 3 to 5 concise English tags describing the POI's vibe or unique features

Main Use Case:
-------------
Used in the card generation pipeline (e.g. fuse_cards_async) to enrich POIs with
human-readable descriptions and semantic tags based on AI understanding of raw inputs.

Key Features:
-------------
✅ Supports async calls for concurrent processing  
✅ Gracefully handles empty input or API failures with fallback defaults  
✅ Unified OpenAI model config (via `MODEL_NAME` in config module)  
✅ Output is always in JSON: {"description": "...", "tags": ["...", "..."]}

Example:
--------
Input:
    "A tranquil riverside park with blooming cherry blossoms and lots of families walking dogs."

Output:
    {
        "description": "A peaceful riverside park popular among families.",
        "tags": ["relaxing", "nature", "family-friendly"]
    }

Author: Tripllery AI Backend
"""

import os
import json
import httpx
from typing import Dict

# ✅ Load unified model config from shared config
from services.utils.config import MODEL_NAME

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}

async def extract_highlights_async(raw_text: str) -> Dict:
    """
    Extracts a short summary and 3–5 English tags from a given raw text using OpenAI API.

    Args:
        raw_text (str): Raw text input such as a user review or fallback POI description.

    Returns:
        Dict: A dictionary with the following structure:
            - description (str): One-sentence summary of the input text
            - tags (List[str]): A list of 3–5 English keywords or tags
    """
    if not raw_text.strip():
        return {"description": "No summary available.", "tags": []}

    prompt = f"""
You're a smart travel assistant.

Extract:
- One-sentence summary
- 3-5 English tags

Input:
{raw_text}

Output JSON only:
{{"description": "...", "tags": ["...", "..."]}}
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(OPENAI_API_URL, headers=HEADERS, json=payload)
            data = response.json()
            if "choices" not in data:
                raise ValueError("OpenAI missing choices")
            content = data["choices"][0]["message"]["content"]
            highlight_result = json.loads(content)
            return highlight_result

    except Exception as e:
        print(f"⚠️ extract_highlights_async fallback because: {e}")
        return {"description": "Failed to extract highlights.", "tags": []}
