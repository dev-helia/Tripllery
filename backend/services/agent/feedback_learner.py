"""
feedback_learner.py · Preference Feedback Engine

This module implements an intelligent feedback processor that learns from
user preferences (liked/disliked POIs) and updates their interest tags accordingly.

It sends structured input to the OpenAI Chat API and expects an updated list of
semantic tags representing the user’s evolving travel style.

Main Use Case:
--------------
Used after the user interacts with POI cards (like/dislike actions).
Enhances personalization for future recommendations.

Key Features:
-------------
✅ LLM-powered learning from user feedback  
✅ Works with or without existing tags (cold start friendly)  
✅ Graceful fallback if API fails  
✅ JSON-only output format

Author: Tripllery AI Backend
"""

import os
import json
import httpx
from typing import List, Dict

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}

async def learn_from_feedback(
    liked_pois: List[Dict],
    disliked_pois: List[Dict],
    current_tags: List[str] = None
) -> Dict:
    """
    Adjusts a user's travel interest tags based on liked/disliked POIs using OpenAI.

    Args:
        liked_pois (List[Dict]): List of POI objects the user liked
        disliked_pois (List[Dict]): List of POI objects the user disliked
        current_tags (List[str], optional): User's current interest tags

    Returns:
        Dict: {
            "updated_tags": List[str]
        }

    If the API call fails or input is empty, returns original tags as fallback.

    Example Output:
        {"updated_tags": ["Art", "Nature", "Coffee Shops"]}
    """
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
        "model": MODEL_NAME,
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
