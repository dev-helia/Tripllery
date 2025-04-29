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

async def plan_days_with_llm(rough_plan: Dict[str, list], transportation: str) -> Dict[str, Dict[str, list]]:
    if not rough_plan:
        raise ValueError("Invalid rough plan")

    plan_text = "\n".join([f"{day}: {[poi['name'] for poi in pois if isinstance(poi, dict)]}" for day, pois in rough_plan.items()])

    transportation_context = (
        "The user has a car. Longer travel is acceptable."
        if transportation == "have_car"
        else "The user has no car. Prefer short distance travel."
    )

    prompt = f"""
You are a travel assistant.

Split each day's POIs into Morning and Afternoon.
Context: {transportation_context}
Plan:
{plan_text}

Output JSON only:
{{"Day 1": {{"Morning": ["A"], "Afternoon": ["B"]}}}}
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
                raise ValueError("OpenAI missing choices")
            content = data["choices"][0]["message"]["content"]
            detailed_plan = json.loads(content)
            return detailed_plan

    except Exception as e:
        print(f"⚠️ plan_days_with_llm fallback because: {e}")
        raise e
