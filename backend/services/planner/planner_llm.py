"""
planner_llm.py · Daily Timeline Builder (LLM-Based)

This module uses the OpenAI Chat API to split each day's list of POIs
into Morning and Afternoon blocks, based on the user's transportation method,
preferred pace (intensity), and optional wake/return time.

Main Use Case:
--------------
Called during `/preview` stage to generate structured timelines from a rough day plan.

Key Features:
-------------
✅ Supports car/public transport logic  
✅ Intensity-aware POI distribution  
✅ Optional time preferences: wake_up_time / return_time  
✅ Output in structured JSON format  
✅ Prints final timeline for debug

Author: Tripllery AI Backend
"""

import os
import json
import httpx
from typing import Dict, Optional

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}

async def plan_days_with_llm(
    rough_plan: Dict[str, list],
    transportation: str,
    intensity: str = "normal",
    wake_up_time: Optional[str] = None,
    return_time: Optional[str] = None
) -> Dict[str, Dict[str, list]]:
    """
    Splits each day's POIs into Morning / Afternoon blocks using LLM.

    Args:
        rough_plan (Dict[str, list]): A mapping of day → POI list (from /plan step)
        transportation (str): Either "car" or "public"
        intensity (str): Travel pace, one of "chill", "normal", "intense"
        wake_up_time (str, optional): Time user wakes up (e.g. "08:00")
        return_time (str, optional): Time user returns to hotel (e.g. "21:00")

    Returns:
        Dict[str, Dict[str, list]]: Nested timeline, e.g.
            {
                "Day 1": {
                    "Morning": ["POI A", "POI B"],
                    "Afternoon": ["POI C"]
                },
                ...
            }

    Raises:
        Exception: If OpenAI fails or returns bad format
    """
    if not rough_plan:
        raise ValueError("Invalid rough plan")

    # Step 1️⃣ Flatten day-to-names text for prompt
    plan_text = "\n".join([
        f"{day}: {[poi['name'] for poi in pois if isinstance(poi, dict)]}"
        for day, pois in rough_plan.items()
    ])

    # Step 2️⃣ Build transportation context
    transportation_context = (
        "The user has a car. Longer travel is acceptable."
        if transportation == "car"
        else "The user has no car. Prefer short distance travel."
    )

    # Step 3️⃣ Intensity context
    intensity_context = {
        "chill": "The user prefers a relaxed schedule. At most 1-2 POIs per half day.",
        "normal": "The user prefers a balanced schedule. 2-3 POIs per half day are fine.",
        "intense": "The user is okay with a packed schedule. Plan as many POIs as possible."
    }.get(intensity, "The user prefers a normal travel pace.")

    # Step 4️⃣ Time context (optional)
    time_context = ""
    if wake_up_time:
        time_context += f"The user wakes up around {wake_up_time}. "
    if return_time:
        time_context += f"The user prefers to return to the hotel around {return_time}. "

    # Step 5️⃣ Combine into prompt
    prompt = f"""
You are a travel assistant.

Split each day's POIs into Morning and Afternoon.
Context: {transportation_context}
Pace: {intensity_context}
Time Preference: {time_context.strip()}

Plan:
{plan_text}

Output JSON only:
{{"Day 1": {{"Morning": ["A"], "Afternoon": ["B"]}}}}
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
                raise ValueError("OpenAI missing choices")
            content = data["choices"][0]["message"]["content"]
            detailed_plan = json.loads(content)
            print("🧪 Final timeline plan =", json.dumps(detailed_plan, indent=2))
            return detailed_plan

    except Exception as e:
        print(f"⚠️ plan_days_with_llm fallback because: {e}")
        raise e
