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

async def learn_from_feedback(liked_pois: List[Dict], disliked_pois: List[Dict], current_tags: List[str] = None) -> Dict:
    if not liked_pois and not disliked_pois:
        return {"updated_tags": current_tags or []}

    liked_names = [poi["name"] for poi in liked_pois]
    disliked_names = [poi["name"] for poi in disliked_pois]
    base_tags = current_tags or []

    prompt = f"""
You are an intelligent travel preference learner.
Given:
- List of places a user liked
- List of places a user disliked
- Their current travel interest tags (optional)

Adjust the user's interest tags accordingly.

Output JSON only:
{{"updated_tags": ["Adventure", "Nature", "Local Food"]}}
Liked Places: {liked_names}
Disliked Places: {disliked_names}
Current Tags: {base_tags}
"""

    payload = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5
    }

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(OPENAI_API_URL, headers=HEADERS, json=payload)
            data = response.json()
            if "choices" not in data:
                raise ValueError("OpenAI API missing choices")
            content = data["choices"][0]["message"]["content"]
            feedback_result = json.loads(content)
            return feedback_result

    except Exception as e:
        print(f"⚠️ learn_from_feedback fallback because: {e}")
        return {"updated_tags": base_tags}
