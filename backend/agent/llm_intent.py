"""
llm_intent.py · LLM-powered Form Intent Parser

This module handles the interpretation of user-submitted form data into structured travel intent,
including AI-assisted keyword extraction from natural language notes.

It uses OpenAI Chat API to extract interest-based tags, which are added to the parsed intent object
to enhance downstream recommendation and planning modules.

Main Use Case:
--------------
Used in the backend `/recommend` endpoint as the first step in converting a form submission
into a structured format, containing location, timing, user preferences, and AI-enriched interests.

Key Features:
-------------
✅ Extracts meaningful travel keywords from free-form user notes using OpenAI  
✅ Fallback to default interest tags if extraction fails  
✅ Normalizes and structures all form input into a consistent schema  
✅ Supports future expansion with more preference dimensions

Author: Tripllery AI Backend
"""

from typing import Dict, List
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# ✅ Load model config
from services.utils.config import MODEL_NAME

# 🔐 Load OpenAI key from environment
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def extract_keywords(note: str) -> List[str]:
    """
    Uses OpenAI to extract 3–5 concise interest keywords from a user note.

    This function transforms user-written preferences (e.g. "I want to visit museums and eat local food")
    into a list of semantic tags useful for downstream personalization.

    Args:
        note (str): Free-text trip preference written by the user.

    Returns:
        List[str]: A list of English keywords representing interest tags.
                   If extraction fails, returns an empty list.
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
            model=MODEL_NAME,  # ✅ Use unified model config
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print(f"⚠️ Keyword extraction failed: {e}")
        return []

def parse_form_input(form_data: Dict) -> Dict:
    """
    Parses raw form data submitted by the user into structured intent format.

    This function:
    - Extracts text input such as city, dates, and personal notes
    - Calls LLM-based keyword extractor for interest tagging
    - Applies fallback defaults when necessary
    - Returns a consistent intent schema used by the recommendation engine

    Args:
        form_data (Dict): Raw form submission data (typically from frontend DesignPage).

    Returns:
        Dict: Normalized intent dictionary with structured fields including:
            - departure_city, destination, start_datetime, end_datetime
            - travelers, budget, transportation, stopovers
            - trip_preferences (raw notes)
            - interest_keywords (AI-extracted or fallback)
            - round_trip, include_hotels, meal_options, intensity
    """
    note = form_data.get("trip_preferences", "").strip()
    keywords = extract_keywords(note)

    if not keywords:
        keywords = ["sightseeing", "food", "landmarks", "nature", "cafes"]

    intent = {
        "departure_city": form_data.get("departure_city"),
        "destination": form_data.get("destination"),
        "start_datetime": form_data.get("start_datetime"),
        "end_datetime": form_data.get("end_datetime"),
        "travelers": form_data.get("travelers"),
        "budget": form_data.get("budget"),
        "transportation": form_data.get("transportation"),
        "stopovers": form_data.get("stopovers", []),
        "trip_preferences": note,
        "interest_keywords": keywords,
        "round_trip": form_data.get("round_trip", False),
        "include_hotels": form_data.get("include_hotels", False),
        "meal_options": form_data.get("meal_options", {}),
        "intensity": form_data.get("intensity", "normal")
    }

    print("✅ Parsed user intent:", intent)
    return intent
