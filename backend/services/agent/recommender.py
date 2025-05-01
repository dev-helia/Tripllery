"""
recommender.py · Tripllery V3 Full Recommendation Agent

This module defines the intelligent pipeline behind the Tripllery recommendation system.

It processes user form input through:
- Intent parsing (from LLM or form)
- Query generation for Google Maps searches
- POI fetching and cleaning
- Xiaohongshu mock scraping
- LLM-powered highlight fusion
- Card scoring and travel style classification
- Feedback learning for interest tags

The result is a sorted list of personalized POI cards that reflect the user's interests and trip context.

Main Use Case:
--------------
Called by the `/recommend` API to generate an initial card pool.

Author: Tripllery AI Backend
"""

from agent.llm_intent import parse_form_input
from agent.query_generator import generate_queries
from maps.fetcher import search_google_maps
from maps.poi_cleaner import clean_pois
from crawler.xiaohongshu import fetch_reviews_for_poi
from agent.fusion import fuse_cards_async
from backend.services.utils.score_cards import score_cards
from backend.services.agent.style_classifier import classify_travel_style
from backend.services.agent.feedback_learner import learn_from_feedback

async def recommend_agent(form_data: dict) -> list:
    """
    Runs the full multi-stage recommendation process for a user's trip preferences.

    Args:
        form_data (dict): Raw form input submitted by the frontend, containing:
            - destination, stopovers, interest_keywords
            - transportation, start/end dates, trip_preferences, etc.

    Returns:
        list: A sorted list of Tinder-style POI card dictionaries, ready for display and selection.
    """
    try:
        # Step 1️⃣ Parse form into structured intent
        intent = parse_form_input(form_data)
        destination = intent.get("destination")
        stopovers = intent.get("stopovers", [])
        interest_keywords = intent.get("interest_keywords", [])
        trip_note = form_data.get("trip_preferences", "")
        transportation = intent.get("transportation")
        start_datetime = intent.get("start_datetime")
        end_datetime = intent.get("end_datetime")

        # Step 2️⃣ Generate search queries for all cities
        all_queries = generate_queries(destination, stopovers, interest_keywords)

        # Step 3️⃣ Run Google Maps searches
        all_pois = []
        for city, queries in all_queries.items():
            for query in queries:
                pois = search_google_maps(query=query, city=city)
                all_pois.extend(pois)

        print(f"🗺️ Total POIs fetched: {len(all_pois)}")

        # Step 4️⃣ Clean geographically distant POIs
        all_pois = clean_pois(all_pois)
        print(f"🧹 POIs cleaned: {len(all_pois)}")

        # Step 5️⃣ Simulate Xiaohongshu review crawling
        review_lookup = {}
        for poi in all_pois:
            name = poi["name"]
            city = poi.get("city", "")
            scraped = fetch_reviews_for_poi(name, city)
            if scraped["raw_texts"]:
                review_lookup[name] = {
                    "raw_text": scraped["raw_texts"][0],
                    "links": scraped.get("links", [])
                }

        print(f"🧠 Crawled reviews for {len(review_lookup)} POIs")

        # Step 6️⃣ Fuse POIs + reviews into highlight-rich cards
        raw_card_pool = await fuse_cards_async(all_pois, review_lookup)
        print(f"🎴 Built raw card pool: {len(raw_card_pool)} cards")

        # Step 7️⃣ Score and sort cards
        scored_card_pool = score_cards(raw_card_pool)
        print(f"🏆 Scored and sorted cards")

        # Step 8️⃣ Classify user's travel style (theme, tone, tags)
        style_info = await classify_travel_style(trip_note, scored_card_pool)
        print(f"🎨 Classified user style: {style_info}")

        # Step 9️⃣ Update tags via feedback (empty click history for now)
        feedback_info = await learn_from_feedback(
            liked_pois=[],
            disliked_pois=[],
            current_tags=style_info.get("tags", [])
        )
        print(f"🔄 Updated feedback tags: {feedback_info}")

        # ✅ Return final scored and sorted card pool
        return scored_card_pool

    except Exception as e:
        print(f"💥 Recommender error: {e}")
        raise e
