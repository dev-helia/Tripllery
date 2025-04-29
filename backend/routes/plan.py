# /routes/plan.py

from quart import Blueprint, request, jsonify
from services.formatter.formatter_llm import format_plan_with_llm
from services.planner.resolver import rebalance_days
from datetime import datetime

plan_bp = Blueprint("plan", __name__)

def safe_int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

def normalize_transportation(trans):
    if not isinstance(trans, str):
        return "car"
    trans = trans.lower()
    if "car" in trans:
        return "car"
    else:
        return "public"

@plan_bp.route("/plan", methods=["POST"])
async def generate_plan():
    try:
        data = await request.get_json()
        print("📥 Received /plan data:", data)

        accepted_poi_ids = data.get("accepted_pois", [])
        all_pois = data.get("all_pois", [])

        if not accepted_poi_ids:
            return jsonify({"error": "accepted_pois (id list) is missing"}), 400
        if not all_pois:
            return jsonify({"error": "all_pois (full poi objects) are missing"}), 400

        id_to_poi = {poi["id"]: poi for poi in all_pois}

        accepted_pois = []
        for poi_id in accepted_poi_ids:
            poi = id_to_poi.get(poi_id)
            if not poi:
                return jsonify({"error": f"ID not found in all_pois: {poi_id}"}), 400
            accepted_pois.append(poi)

        transportation_raw = data.get("transportation")
        start_datetime_raw = data.get("start_datetime")
        end_datetime_raw = data.get("end_datetime")

        if not transportation_raw or not start_datetime_raw or not end_datetime_raw:
            return jsonify({"error": "start_datetime, end_datetime, and transportation are required."}), 400

        transportation = normalize_transportation(transportation_raw)

        start_time_of_day = data.get("start_time_of_day", "09:00")
        lunch_time = data.get("lunch_time", "12:30")
        flexible_block = safe_int(data.get("flexible_block"), 60)
        avg_transport_time = safe_int(data.get("avg_transport_time"), 20 if transportation == "car" else 45)
        avg_poi_duration = safe_int(data.get("avg_poi_duration"), 90)

        start_datetime = datetime.fromisoformat(start_datetime_raw)
        end_datetime = datetime.fromisoformat(end_datetime_raw)
        total_days = (end_datetime.date() - start_datetime.date()).days + 1

        if total_days <= 0:
            return jsonify({"error": "Invalid travel dates. End date must be after start date."}), 400

        rough_plan = await format_plan_with_llm(accepted_pois, days=total_days, transportation=transportation)
        if not isinstance(rough_plan, dict):
            return jsonify({"error": "Generated rough_plan is not a valid dictionary."}), 500

        final_plan = rebalance_days(rough_plan)

        return jsonify({
            "plan": final_plan,
            "options": {
                "start_time_of_day": start_time_of_day,
                "avg_poi_duration": avg_poi_duration,
                "avg_transport_time": avg_transport_time,
                "lunch_time": lunch_time,
                "flexible_block": flexible_block,
                "transportation": transportation,
                "start_datetime": start_datetime_raw,
                "end_datetime": end_datetime_raw
            }
        })

    except Exception as e:
        print("💥 PLAN ERROR (detailed):", repr(e))
        return jsonify({"error": str(e)}), 500
