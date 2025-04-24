"""
/recommend API · Tripllery Full Agent Flow

Receives form input → Parses user intent → Generates queries
→ Fetches POIs from Google Maps → Crawls review content
→ Generates LLM highlights → Returns Tinder-style card pool
"""

from flask import Blueprint, request, jsonify
from agent.llm_intent import parse_form_input
from agent.query_generator import generate_queries
from maps.fetcher import search_google_maps
from agent.fusion import fuse_cards
from crawler.xiaohongshu import fetch_reviews_for_poi
from agent.highlight_llm import extract_highlights

recommend_bp = Blueprint("recommend", __name__)

@recommend_bp.route("/recommend", methods=["POST"])
def recommend_cards():
    try:
        # 1️⃣ Parse user form input
        form_data = request.get_json()
        # TODO DEBUG
        print("🧾 Step 1: Got form_data ✅", form_data)

        intent = parse_form_input(form_data)
        # TODO DEBUG
        print("🔍 Step 2: Parsed intent ✅", intent)

        destination = intent["destination"]
        stopovers = intent.get("stopovers", [])
        interest_keywords = intent.get("interest_keywords", [])

        # 2️⃣ Generate queries per city
        all_queries = generate_queries(destination, stopovers, interest_keywords)
        # TODO DEBUG
        print("🔍 Step 3: Generated queries ✅", all_queries)

        # 3️⃣ Fetch Google Maps POIs
        all_pois = []
        for city, queries in all_queries.items():
            for query in queries:
                pois = search_google_maps(query=query, city=city)
                all_pois.extend(pois)
        # TODO DEBUG
        print("🗺️ Step 4: Total POIs fetched ✅", len(all_pois))

        # 4️⃣ Auto generate review lookup using Xiaohongshu + GPT
        review_lookup = {}

        for poi in all_pois:
            name = poi["name"]
            city = poi.get("city", "")

            scraped = fetch_reviews_for_poi(name, city)

            if scraped["raw_texts"]:
                # TODO DEBUG
                print(f"🧠 Calling highlight LLM for: {name}")
                highlight = extract_highlights(scraped["raw_texts"][0])
                review_lookup[name] = {
                    "description": highlight["description"],
                    "tags": highlight["tags"],
                    "links": scraped.get("links", [])
                }
                # TODO DEBUG
                print(f"✅ Highlight ready for: {name}")
        # TODO DEBUG
        print("🧠 Step 5: Fusing with reviews ✅")

        # 5️⃣ Fuse into card pool 
        card_pool = fuse_cards(all_pois, review_lookup)

        # ✅ 返回固定数量卡片（每次只返回前 5 个）
        return jsonify(card_pool[:5])

    except Exception as e:
        # TODO Error
        print("💥 ERROR:", e)
        return jsonify({"error": str(e)}), 500
