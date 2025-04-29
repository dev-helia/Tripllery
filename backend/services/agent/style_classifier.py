import os
import json
import httpx
from typing import List, Dict

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}

async def classify_travel_style(user_note: str, accepted_pois: List[Dict]) -> Dict:
    if not user_note.strip() and not accepted_pois:
        return {"primary_style": "Unknown", "tags": []}

    poi_names = [poi["name"] for poi in accepted_pois]

    prompt = f"""
You are an expert travel style classifier.

Given:
- User Description: {user_note}
- Liked Places: {poi_names}

Classify into one primary style and 2-4 tags.

JSON only:
{{"primary_style": "Explorer", "tags": ["Adventure", "Outdoor"]}}
"""

    payload = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4
    }

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(OPENAI_API_URL, headers=HEADERS, json=payload)
            data = response.json()
            if "choices" not in data:
                raise ValueError("OpenAI API missing choices")
            content = data["choices"][0]["message"]["content"]
            style_result = json.loads(content)
            return style_result

    except Exception as e:
        print(f"⚠️ classify_travel_style fallback because: {e}")
        return {"primary_style": "Unknown", "tags": []}
