"""
plan.py · Tripllery V3 Route: /plan

This module defines the /plan route, which receives user-selected POIs and trip metadata,
then returns a structured day-by-day travel plan.

It validates the input, applies intensity-based POI count constraints,
normalizes time settings, and generates a rough itinerary via LLM-based formatting.

Finally, it rebalances the rough plan using rule-based logic for better distribution.

Main Use Case:
--------------
Triggered after user finalizes POI selection and form inputs.
Called by frontend ➜ POST to `/plan`.

Key Features:
-------------
✅ LLM-based day splitting (via format_plan_with_llm)  
✅ Intensity-aware minimum POI requirement  
✅ Smart defaults for timing + transport fallback  
✅ Output includes timeline + all plan generation options  
✅ Unified error handling for all edge cases

Author: Tripllery AI Backend
"""

from quart import Blueprint, request, jsonify
from services.formatter.formatter_llm import format_plan_with_llm
from services.planner.resolver import rebalance_days
from services.utils.poi_math import get_min_required_pois
from datetime import datetime

plan_bp = Blueprint("plan", __name__)

def safe_int(value, default):
    """
    Safely cast a value to int with fallback.

    Args:
        value: Any value (possibly string or None)
        default: Fallback int value

    Returns:
        int
    """
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

def normalize_transportation(trans):
    """
    Normalize the transportation field to either 'car' or 'public'.

    Args:
        trans (Any): Raw transportation field

    Returns:
        str: "car" or "public"
    """
    if not isinstance(trans, str):
        return "car"
    trans = trans.lower()
    return "car" if "car" in trans else "public"

def clean_time_str(t: str, fallback: str) -> str:
    """
    Ensure a string time value is valid; if not, use fallback.

    Args:
        t (str): Input time string
        fallback (str): Default time string

    Returns:
        str
    """
    if isinstance(t, str) and t.strip():
        return t
    return fallback

@plan_bp.route("/plan", methods=["POST"])
async def generate_plan():
    """
    Endpoint: POST /plan

    Receives:
        - accepted_pois: List of selected POI IDs
        - all_pois: Full POI objects
        - start_datetime, end_datetime: ISO strings
        - intensity: "chill" / "normal" / "intense"
        - transportation: "car" / "public"
        - meal_options, wake_up_time, return_time, etc. (optional)

    Returns:
        JSON with:
        - plan: dict → day-by-day POI map
        - options: dict → all runtime settings and parameters used
    """
    try:
        data = await request.get_json()
        print("📥 Received /plan data:", data)

        accepted_poi_ids = data.get("accepted_pois", [])
        all_pois = data.get("all_pois", [])

        if not accepted_poi_ids:
            return jsonify({"error": "accepted_pois (id list) is missing"}), 400
        if not all_pois:
            return jsonify({"error": "all_pois (full poi objects) are missing"}), 400

        # ✅ Extract date and intensity settings
        start_datetime_raw = data.get("start_datetime")
        end_datetime_raw = data.get("end_datetime")
        intensity = data.get("intensity", "normal")

        if not start_datetime_raw or not end_datetime_raw:
            return jsonify({"error": "start_datetime and end_datetime are required."}), 400

        min_required = get_min_required_pois(intensity, start_datetime_raw, end_datetime_raw)
        if len(accepted_poi_ids) < min_required:
            return jsonify({"error": f"You need at least {min_required} POIs to generate a plan."}), 400

        # ✅ Match POI IDs to full objects
        id_to_poi = {poi["id"]: poi for poi in all_pois}
        accepted_pois = [id_to_poi[pid] for pid in accepted_poi_ids if pid in id_to_poi]

        # ✅ Normalize transportation
        transportation_raw = data.get("transportation")
        if not transportation_raw:
            return jsonify({"error": "transportation is required."}), 400
        transportation = normalize_transportation(transportation_raw)

        # 🧼 Optional time & logic fallback
        start_time_of_day = clean_time_str(data.get("start_time_of_day"), "09:00")
        wake_up_time = clean_time_str(data.get("wake_up_time"), start_time_of_day)
        return_time = clean_time_str(data.get("return_time"), "21:00")
        lunch_time = data.get("lunch_time", "12:30")
        flexible_block = safe_int(data.get("flexible_block"), 60)
        avg_transport_time = safe_int(data.get("avg_transport_time"), 20 if transportation == "car" else 45)
        avg_poi_duration = safe_int(data.get("avg_poi_duration"), 90)

        # ✅ Validate total trip length
        start_datetime = datetime.fromisoformat(start_datetime_raw)
        end_datetime = datetime.fromisoformat(end_datetime_raw)
        total_days = (end_datetime.date() - start_datetime.date()).days + 1
        if total_days <= 0:
            return jsonify({"error": "End date must be after start date."}), 400

        # 🔮 Generate rough LLM-based day split plan
        rough_plan = await format_plan_with_llm(accepted_pois, days=total_days, transportation=transportation)
        if not isinstance(rough_plan, dict):
            return jsonify({"error": "Generated rough_plan is not a valid dictionary."}), 500

        # 🔄 Rebalance using resolver logic
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
                "end_datetime": end_datetime_raw,
                "meal_options": data.get("meal_options", {
                    "include_breakfast": True,
                    "include_lunch": True,
                    "include_dinner": True
                }),
                "intensity": intensity,
                "wake_up_time": wake_up_time,
                "return_time": return_time
            }
        })

    except Exception as e:
        print("💥 PLAN ERROR (detailed):", repr(e))
        return jsonify({"error": str(e)}), 500
