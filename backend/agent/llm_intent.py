from typing import Dict, List
import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def extract_keywords(note: str) -> List[str]:
    """
    Use OpenAI to extract interest keywords from user notes.
    """
    if not note.strip():
        return []

    prompt = f"""
You are a travel assistant.

Given the following user description, extract 3-5 concise English keywords that represent interests or trip style.

Output in JSON array format.

---
"{note}"
---
Output:
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
        print(f"Keyword extraction failed: {e}")
        return []

def parse_form_input(form_data: Dict) -> Dict:
    """
    Parse user form data into structured intent.
    """
    note = form_data.get("trip_preferences", "").strip()
    keywords = extract_keywords(note)

    if not keywords:
        keywords = ["sightseeing", "food", "landmarks", "nature", "cafes"]

    intent = {
        "departure_city": form_data.get("departure_city"),
        "destination": form_data.get("destination"),
        "start_datetime": form_data.get("start_datetime"),  # 🆕 新增
        "end_datetime": form_data.get("end_datetime"),      # 🆕 新增
        "travelers": form_data.get("travelers"),
        "budget": form_data.get("budget"),
        "transportation": form_data.get("transportation"),
        "stopovers": form_data.get("stopovers", []),
        "trip_preferences": note,
        "interest_keywords": keywords,
        "round_trip": form_data.get("round_trip", False),
        "include_hotels": form_data.get("include_hotels", False)
    }

    print("✅ Parsed user intent:", intent)

    return intent
