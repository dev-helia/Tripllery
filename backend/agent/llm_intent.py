"""
LLM Intent Parser (OpenAI Version, SDK 1.x)

Parses structured form input, and uses OpenAI to extract keyword tags from natural-language note.

- Input: Full form from user (with .get for each field)
- Output: Standard intent dict + LLM extracted interest keywords (EN)
"""

import os
import json
from typing import Dict, List
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def extract_keywords(note: str) -> List[str]:
    """
    Use OpenAI GPT to extract 3-5 concise English keywords from user notes.

    Args:
        note (str): Raw user description, e.g. "We want something chill and romantic."

    Returns:
        List[str]: Extracted keyword tags, e.g. ["relaxing", "romantic"]
    """
    if not note.strip():
        return []

    prompt = f"""
You are a travel assistant.

Given the following user travel description, extract 3 to 5 concise English keywords 
that describe their interests and travel style. Do not translate, and do not explain.

Return the output in a JSON list format.

---
User Note: "{note}"
---
Output (JSON List):
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print("⚠️ LLM extraction failed:", e)
        return []

def parse_form_input(form_data: Dict) -> Dict:
    """
    Parse raw user form into structured intent.

    Args:
        form_data (Dict): Raw input from frontend form.

    Returns:
        Dict: Parsed intent structure for recommendation pipeline.
    """
    note = form_data.get("trip_preferences", "")
    return {
        "departure_city": form_data.get("departure_city"),
        "destination": form_data.get("destination"),
        "days": form_data.get("days"),
        "travelers": form_data.get("travelers"),
        "budget": form_data.get("budget"),
        "transportation": form_data.get("transportation"),
        "stopovers": form_data.get("stopovers", []),
        "trip_preferences": note,
        "interest_keywords": extract_keywords(note),
        "round_trip": form_data.get("round_trip", False),
        "include_hotels": form_data.get("include_hotels", False)
    }
