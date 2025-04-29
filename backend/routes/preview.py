# /routes/preview.py

from quart import Blueprint, request, jsonify
from services.preview.builder import build_full_schedule

preview_bp = Blueprint("preview", __name__)

@preview_bp.route("/preview", methods=["POST"])
async def generate_preview():
    try:
        data = await request.get_json()

        rough_plan = data.get("plan")
        options = data.get("options")

        if not rough_plan:
            return jsonify({"error": "Missing rough plan."}), 400
        if not options:
            return jsonify({"error": "Missing options."}), 400

        # 更细致保护 options
        required_fields = ["start_time_of_day", "avg_poi_duration", "avg_transport_time", 
                           "lunch_time", "flexible_block", "transportation", "start_datetime", "end_datetime"]
        missing_fields = [field for field in required_fields if field not in options]

        if missing_fields:
            return jsonify({"error": f"Options missing fields: {missing_fields}"}), 400

        full_schedule = await build_full_schedule(rough_plan, options)

        return jsonify(full_schedule)

    except Exception as e:
        print("💥 PREVIEW ERROR (detailed):", repr(e))
        return jsonify({"error": str(e)}), 500
