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

async def intelligent_split_days(pois: List[Dict], days: int) -> Dict[str, List[str]]:
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
        "model": "gpt-4",
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
    pois_sorted = sorted(pois, key=lambda x: x.get("rating", 0), reverse=True)
    result = {f"Day {i+1}": [] for i in range(days)}
    for idx, poi in enumerate(pois_sorted):
        result[f"Day {idx % days + 1}"].append(poi["name"])
    return result
