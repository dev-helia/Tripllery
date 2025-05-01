"""
score_cards.py · Recommendation Card Scoring Engine

This module defines the scoring logic for ranking recommendation cards
returned from the fusion engine. Each card is evaluated using:

- Google Maps rating
- Number of extracted highlight tags
- Length of LLM-generated description

Main Use Case:
--------------
Used in `recommend_agent()` to sort POI cards before display.
The scoring system can later be made user-personalized or AI-tuned.

Key Features:
-------------
✅ Multi-factor scoring (rating + tags + text quality)  
✅ Score saved in card["score"]  
✅ Descending sort (high → low)  
✅ Easily extensible weight system

Author: Tripllery AI Backend
"""

from typing import List, Dict

def score_cards(cards: List[Dict]) -> List[Dict]:
    """
    Assigns a numeric score to each card and returns a sorted list (desc).

    Args:
        cards (List[Dict]): List of POI card dicts

    Returns:
        List[Dict]: Cards with added 'score', sorted by score descending
    """

    def compute_score(card: Dict) -> float:
        rating = card.get("rating", 0) or 0
        tag_count = len(card.get("highlight_tags", []))
        desc_len = len(card.get("description", ""))

        # ✨ Weight system: 1.5×rating + 1.0×tag_count + 1.0×desc_length (normalized)
        return rating * 1.5 + tag_count * 1.0 + (desc_len / 100.0)

    # Attach scores
    for card in cards:
        card["score"] = compute_score(card)

    # Sort descending by score
    return sorted(cards, key=lambda x: x["score"], reverse=True)
