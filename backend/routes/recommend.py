"""
recommend.py · Tripllery V3 Route: /recommend

This module defines the recommendation entry point for the Tripllery system.
It receives user preference form data and returns a batch of AI-curated POI cards
along with supporting metadata such as selection thresholds.

The route also supports pagination (`/recommend/more`) to load additional cards
from a cached pool.

Main Use Case:
--------------
Frontend ➜ POST to `/recommend` when form is submitted.
Displays initial cards and stores all-pool locally.
Frontend ➜ GET `/recommend/more` to page more options.

Key Features:
-------------
✅ LLM-powered recommendation agent  
✅ Travel intensity-based `min_required` POI calculation  
✅ Smart fallback for meal settings  
✅ POI card pool cached server-side for pagination  
✅ Returns full POI metadata for plan generation

Author: Tripllery AI Backend
"""

from quart import Blueprint, request, jsonify
from backend.services.agent.recommender import recommend_agent
from backend.services.utils.recommend_pool import cache_card_pool, get_next_batch
from backend.services.utils.poi_math import get_min_required_pois

recommend_bp = Blueprint("recommend", __name__)

@recommend_bp.route("/recommend", methods=["POST"])
async def recommend_cards():
    """
    Endpoint: POST /recommend

    Receives:
        - form_data: Dict[str, Any]
            Must include fields like:
                - destination, start_datetime, end_datetime
                - interest_keywords, intensity, meal_options (optional)

    Returns:
        JSON: {
            cards: [first 12 cards for display],
            all_pois: [entire recommended POI pool],
            min_required: int (minimum number of POIs needed based on duration + intensity)
        }
    """
    try:
        form_data = await request.get_json()
        print("🧾 Received form_data:", form_data)

        # ✅ Default meal settings fallback
        meal_options = form_data.get("meal_options", {
            "include_breakfast": True,
            "include_lunch": True,
            "include_dinner": True
        })
        form_data["meal_options"] = meal_options

        # ✅ Calculate POI selection threshold
        start = form_data.get("start_datetime")
        end = form_data.get("end_datetime")
        intensity = form_data.get("intensity", "normal")
        min_required = get_min_required_pois(intensity, start, end)

        # ✅ LLM-based POI recommendation + cache
        card_pool = await recommend_agent(form_data)
        cache_card_pool(card_pool)

        return jsonify({
            "cards": card_pool[:12],         # Initial 12 for swipe or grid view
            "all_pois": card_pool,           # Full pool for selection / backup
            "min_required": min_required     # Frontend uses this to enforce limits
        })

    except Exception as e:
        print("💥 Recommend API error:", e)
        return jsonify({"error": str(e)}), 500


@recommend_bp.route("/recommend/more", methods=["GET"])
async def recommend_more_cards():
    """
    Endpoint: GET /recommend/more

    Provides paginated POI cards from the previously cached pool.
    Used when frontend scrolls or requests more cards.

    Query Params:
        - start: int → index to start from
        - size: int → number of cards to return

    Returns:
        JSON: {
            cards: [next N cards from server-side pool]
        }
    """
    try:
        start = int(request.args.get("start", 0))
        size = int(request.args.get("size", 6))
        more_cards = get_next_batch(start, size)

        return jsonify({
            "cards": more_cards
        })

    except Exception as e:
        print("💥 Recommend More error:", e)
        return jsonify({"error": str(e)}), 500
