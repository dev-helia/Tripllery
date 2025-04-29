import os
import json
import httpx
from typing import Dict

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}

async def extract_highlights_async(raw_text: str) -> Dict:
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
        "model": "gpt-4",
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
