"""
Highlight LLM Engine · Async Version (OpenAI API v1)

Asynchronously calls OpenAI to extract highlight tags + description.
"""

import os
import json
import asyncio
import httpx
from typing import Dict

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}

async def extract_highlights_async(raw_text: str) -> Dict:
    """
    Asynchronously extract highlight info from travel review text.

    Args:
        raw_text (str): Input content

    Returns:
        Dict: {
            "description": "...",
            "tags": ["..."]
        }
    """
    if not raw_text.strip():
        return {"description": "No summary available.", "tags": []}

    prompt = f"""
You're a smart travel assistant.

Given a user travel note or comment, please extract:
1. A one-sentence summary of why the place is worth visiting.
2. 3-5 highlight tags (English only) that capture the vibe or features.

Input:
---
{raw_text}
---

Output format (JSON only):
{{
  "description": "...",
  "tags": ["...", "..."]
}}
"""

    payload = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        try:
            resp = await client.post(OPENAI_API_URL, headers=HEADERS, json=payload)
            content = resp.json()["choices"][0]["message"]["content"]
            return json.loads(content)
        except Exception as e:
            print("⚠️ Highlight async failed:", e)
            return {"description": "Failed to extract highlights.", "tags": []}
