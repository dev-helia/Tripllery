from quart import Blueprint, request, jsonify
from backend.services.agent.recommender import recommend_agent

recommend_bp = Blueprint("recommend", __name__)

@recommend_bp.route("/recommend", methods=["POST"])
async def recommend_cards():
    try:
        form_data = await request.get_json()
        print("🧾 Received form_data:", form_data)

        card_pool = await recommend_agent(form_data)

        # 🆕 分页参数
        page = int(form_data.get("page", 1))
        page_size = int(form_data.get("page_size", 5))

        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size

        paginated_cards = card_pool[start_idx:end_idx]

        return jsonify({
            "cards": paginated_cards,
            "all_pois": card_pool
        })

    except Exception as e:
        print("💥 Recommend API error:", e)
        return jsonify({"error": str(e)}), 500
