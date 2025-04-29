"""
Card Scoring & Ranking Logic

Scores each recommendation card based on:
- Google Maps rating
- Number of highlight tags
- Length of description
"""

from typing import List, Dict

def score_cards(cards: List[Dict]) -> List[Dict]:
    """
    Assign a score to each card, and return sorted card list (desc).

    Args:
        cards (List[Dict]): Raw cards list

    Returns:
        List[Dict]: Sorted cards with scores embedded
    """

    def compute_score(card: Dict) -> float:
        rating = card.get("rating", 0) or 0
        tag_count = len(card.get("highlight_tags", []))
        desc_len = len(card.get("description", ""))
        
        # TODO 👉 权重可调（现在比较简单粗暴）
        return rating * 1.5 + tag_count * 1.0 + (desc_len / 100.0)

    # Attach score
    for card in cards:
        card["score"] = compute_score(card)

    # Sort descending by score
    return sorted(cards, key=lambda x: x["score"], reverse=True)
