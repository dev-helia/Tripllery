"""
Fusion Engine · Full AI Version (Async)

Combines Google Maps POI data with Xiaohongshu reviews and OpenAI highlights
to produce full Tinder-style recommendation cards.
"""

from typing import List, Dict
import uuid
import asyncio
from agent.highlight_llm import extract_highlights_async
from crawler.xiaohongshu import fetch_reviews_for_poi

async def fuse_cards_async(maps_pois: List[Dict], review_lookup: Dict[str, Dict] = {}) -> List[Dict]:
    """
    Asynchronously combines POI info with human-style descriptions and tags from reviews or LLM.

    Args:
        maps_pois (List[Dict]): POI list from maps.fetcher
        review_lookup (Dict): Optional override for review data {poi_name: {...}}

    Returns:
        List[Dict]: Full Tinder card objects with LLM-generated summaries
    """

    async def build_card(poi: Dict) -> Dict:
        name = poi["name"]
        city = poi.get("city", "")
        review = review_lookup.get(name, {})

        # TODO Step 1️⃣：尝试用爬虫模拟内容（或真实后续补上）
        if not review.get("description"):
            scraped = fetch_reviews_for_poi(name, city)
            if scraped["raw_texts"]:
                highlight = await extract_highlights_async(scraped["raw_texts"][0])
                review = {
                    "description": highlight["description"],
                    "tags": highlight["tags"],
                    "links": scraped.get("links", [])
                }

        # TODO Step 2️⃣：如果依然失败，则 fallback 模板生成（兜底）
        if not review.get("description"):
            fallback_text = f"This is a place called {name} in {city}. It is a tourist spot with a rating of {poi.get('rating', '?')}."
            highlight = await extract_highlights_async(fallback_text)
            review = {
                "description": highlight["description"],
                "tags": highlight["tags"],
                "links": []
            }

        # TODO 构造卡片结构
        return {
            "id": f"poi_{uuid.uuid4().hex[:8]}",
            "name": name,
            "city": city,
            "lat": poi["lat"],
            "lng": poi["lng"],
            "rating": poi.get("rating"),
            "image_url": poi.get("image_url", "https://via.placeholder.com/400x300.png?text=No+Image"),
            "description": review["description"],
            "highlight_tags": review["tags"],
            "opening_hours": poi.get("opening_hours", []),
            "source": {
                "google_maps_url": poi.get("maps_url", f"https://www.google.com/maps/search/{name.replace(' ', '+')}"),
                "review_links": review["links"]
            }
        }

    # TODO 并发构造所有卡片
    return await asyncio.gather(*(build_card(poi) for poi in maps_pois))
