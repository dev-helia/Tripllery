"""
style_classifier.py · Travel Style Inference Agent

This module defines an AI-powered classifier that infers a user's travel style
based on their free-form trip note and list of accepted POIs.

It uses the OpenAI Chat API to assign:
- A primary style label (e.g. "Explorer", "Relaxer", "Cultural Enthusiast")
- A short list of descriptive tags

Main Use Case:
--------------
Used in the recommendation pipeline after POIs are scored and selected.
Helps contextualize user preferences for downstream personalization or UI display.

Key Features:
-------------
✅ Combines natural language notes + semantic POI names  
✅ Outputs structured style label + tags (fully JSON)  
✅ Compatible with cold start (no POIs or notes)  
✅ Low temperature for deterministic classification

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

async def classify_travel_style(user_note: str, accepted_pois: List[Dict]) -> Dict:
    """
    Classifies the user's travel style based on notes and selected POIs.

    Args:
        user_note (str): Free-text input written by the user (preferences, ideas, etc.)
        accepted_pois (List[Dict]): POI cards the user selected as "liked"

    Returns:
        Dict: {
            "primary_style": str,
            "tags": List[str]
        }

    Example Output:
        {
            "primary_style": "Cultural Explorer",
            "tags": ["Museums", "Local Food", "Photography"]
        }

    Fallback:
        If input is missing or LLM fails, returns:
        {"primary_style": "Unknown", "tags": []}
    """

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
        "model": MODEL_NAME,
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
