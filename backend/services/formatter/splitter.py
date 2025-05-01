"""
splitter.py · POI Day Split Engine (LLM + Heuristic)

This module handles splitting a flat list of POIs into multiple travel days.

It first attempts intelligent distribution using OpenAI LLMs,
and if that fails (due to API error, invalid format, etc.), it falls back to
a simple round-robin heuristic based on POI rating.

Main Use Case:
--------------
Called during Tripllery's `/plan` step via `formatter_llm.py`
to distribute accepted POIs over N days.

Key Features:
-------------
✅ Intelligent clustering via GPT (balanced, themed, diverse)  
✅ Fast fallback with round-robin + rating sort  
✅ Consistent JSON output: { "Day 1": ["POI A", "POI B"], ... }  
✅ Supports graceful fallback with no disruption

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

async def intelligent_split_days(pois: List[Dict], days: int) -> Dict[str, List[str]]:
    """
    Uses OpenAI to split POIs into N days intelligently.

    Args:
        pois (List[Dict]): List of POI objects (must contain "name")
        days (int): Number of travel days

    Returns:
        Dict[str, List[str]]: Mapping of day labels to POI names.

    Fallback:
        If LLM fails or returns invalid format, uses `simple_split_days`.

    Example Output:
        {
            "Day 1": ["MoMA", "Joe's Pizza"],
            "Day 2": ["Central Park", "Empire State Building"]
        }
    """
    poi_names = [poi["name"] for poi in pois]

    prompt = f"""
You are a smart travel planner.

Given the following list of places, and a total of {days} travel days, distribute them into days logically.

Requirements:
- Group similar types if possible.
- Balance number of places per day.
- Avoid empty days.
- Return JSON only.

Places:
{poi_names}

Output format (strictly JSON):
{{"Day 1": ["Place A", "Place B"], "Day 2": ["Place C", "Place D"]}}
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
                raise ValueError("OpenAI API returned invalid format (missing choices)")
            content = data["choices"][0]["message"]["content"]
            plan = json.loads(content)
            if not isinstance(plan, dict):
                raise ValueError("LLM returned non-dict format")
            return plan

    except Exception as e:
        print(f"⚠️ intelligent_split_days fallback because: {e}")
        return simple_split_days(pois, days)


def simple_split_days(pois: List[Dict], days: int) -> Dict[str, List[str]]:
    """
    Fallback day splitter that assigns POIs round-robin by rating.

    Args:
        pois (List[Dict]): List of POIs
        days (int): Number of travel days

    Returns:
        Dict[str, List[str]]: Day → POI name list
    """
    # Sort by rating descending
    pois_sorted = sorted(pois, key=lambda x: x.get("rating", 0), reverse=True)

    result = {f"Day {i+1}": [] for i in range(days)}

    # Round-robin distribute
    for idx, poi in enumerate(pois_sorted):
        result[f"Day {idx % days + 1}"].append(poi["name"])

    return result
