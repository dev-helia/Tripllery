"""
Highlight LLM Engine · Multilingual + English Output

Uses OpenAI GPT to analyze travel content (in any language) and output
an English summary + 3–5 English highlight tags.

Output:
{
  "description": "...",
  "tags": ["...", "..."]
}
"""

from dotenv import load_dotenv
import os
import openai
import json
from typing import Dict

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_highlights(raw_text: str) -> Dict:
    """
    Call OpenAI to extract a descriptive summary and highlight tags from travel content.

    Args:
        raw_text (str): Crawled or generated content describing a place (any language).

    Returns:
        Dict: {
            "description": "Concise summary (English)",
            "tags": ["tag1", "tag2", "tag3"] (English only)
        }
    """

    if not raw_text.strip():
        return {"description": "No summary available.", "tags": []}

    prompt = f"""
You are a multilingual AI travel assistant.

Your task is to analyze a user-generated travel note or review, which may be written in any language (e.g. Chinese, Spanish, etc.), and generate **English-only** outputs.

🎯 Please extract:
1. A one-sentence English description of why this place is worth visiting.
2. A list of 3–5 concise **highlight tags** in English, describing features, vibe, or use case. (e.g. romantic, street food, family-friendly)

---

📝 Input Travel Note:
{raw_text}

---

✅ Output format (JSON only):
{{
  "description": "...",
  "tags": ["...", "..."]
}}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        content = response["choices"][0]["message"]["content"]
        return json.loads(content)
    except Exception as e:
        print("⚠️ OpenAI highlight failed:", e)
        return {"description": "Failed to extract highlights.", "tags": []}
