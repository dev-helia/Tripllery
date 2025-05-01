"""
builder.py · Full-Day Timeline Generator (LLM-Based + Rule-Based Blocks)

This module builds the full daily schedule from a rough day-to-POI plan,
using a combination of user preferences, default constants, LLM-based timeline splits,
travel time estimation, and conditional block insertion (meals, transit, return, etc).

Main Use Case:
--------------
Invoked in `/preview` to finalize a full trip timeline (hourly itinerary)
from an accepted rough plan.

Key Features:
-------------
✅ Applies wake-up, return time preferences  
✅ Handles travel times + routing polylines  
✅ Conditionally inserts breakfast, lunch, dinner  
✅ Adds flexible time blocks and final hotel return  
✅ Filters invalid blocks (missing start/end)

Author: Tripllery AI Backend
"""

from datetime import datetime, timedelta
from services.preview.helper import (
    insert_breakfast, insert_lunch, insert_dinner,
    insert_poi_block, insert_transport_block,
    insert_flexible_block, insert_return_to_hotel
)
from services.preview.directions import batch_travel_times
from services.preview.flexible_time import smart_insert_flexible_blocks
from services.preview.constants import (
    DEFAULT_LUNCH_TIME, DEFAULT_DINNER_TIME,
    DEFAULT_DAY_END_TIME, DEFAULT_START_TIME_OF_DAY
)

async def build_full_schedule(rough_plan: dict, options: dict) -> dict:
    """
    Converts a rough plan (Day → POIs) into a full time-based schedule per day.

    Args:
        rough_plan (dict): {"Day 1": [POIs], ...}
        options (dict): Includes all user preferences like:
            - wake_up_time, return_time
            - avg_poi_duration, flexible_block
            - meal_options, transportation
            - start_datetime, end_datetime

    Returns:
        dict: {"Day 1": [block1, block2, ...], ...}
    """
    start_datetime = datetime.fromisoformat(options.get("start_datetime"))
    end_datetime = datetime.fromisoformat(options.get("end_datetime"))

    wake_up_time = options.get("wake_up_time") or DEFAULT_START_TIME_OF_DAY
    return_time = options.get("return_time") or DEFAULT_DAY_END_TIME

    avg_poi_duration = int(options.get("avg_poi_duration", 90))
    flexible_block = int(options.get("flexible_block", 60))
    transportation_mode = options.get("transportation", "no_car")

    meal_options = options.get("meal_options", {
        "include_breakfast": True,
        "include_lunch": True,
        "include_dinner": True
    })

    total_days = (end_datetime.date() - start_datetime.date()).days + 1
    date_list = [(start_datetime.date() + timedelta(days=i)).isoformat() for i in range(total_days)]

    full_schedule = {}
    day_counter = 0

    for day_name, pois in rough_plan.items():
        if not pois or not isinstance(pois, list):
            print(f"⚠️ Skipping empty day: {day_name}")
            continue

        current_day_date = date_list[day_counter]

        # Determine start time
        if day_counter == 0:
            current_time = start_datetime
        else:
            current_time = datetime.combine(
                start_datetime.date() + timedelta(days=day_counter),
                datetime.strptime(wake_up_time, "%H:%M").time()
            )

        # Get travel time + routing for POIs
        travel_time_list, polyline_list = await batch_travel_times(pois, transportation_mode)

        # Build base day schedule with meals and transport
        day_schedule = await build_day_schedule(
            pois, current_time, current_day_date, day_name,
            avg_poi_duration,
            travel_time_list, polyline_list,
            meal_options,
            return_time
        )

        # Insert flexible time blocks (e.g. rest/shopping)
        day_schedule = smart_insert_flexible_blocks(day_schedule, target_total_flexible_minutes=flexible_block)

        # Filter invalid blocks
        valid_schedule = []
        for block in day_schedule:
            if not block or not isinstance(block, dict):
                print(f"⚠️ Invalid block skipped in {day_name}: {block}")
                continue
            if not block.get("start_time") or not block.get("end_time"):
                print(f"⚠️ Missing time block skipped in {day_name}: {block}")
                continue
            valid_schedule.append(block)

        full_schedule[day_name] = valid_schedule
        day_counter += 1

    return full_schedule


async def build_day_schedule(pois, start_time, date, day_name, avg_poi_duration,
                             travel_time_list, polyline_list, meal_options, return_time):
    """
    Constructs a time-based day schedule from ordered POIs.

    Args:
        pois: List of POI dicts for this day
        start_time: datetime object (day start time)
        date: str, e.g. "2025-05-01"
        day_name: "Day 1"
        avg_poi_duration: minutes per POI
        travel_time_list: list of minutes between POIs
        polyline_list: routing polylines for frontend map
        meal_options: includes breakfast/lunch/dinner bools
        return_time: str, e.g. "21:00"

    Returns:
        List[Dict]: Timeline blocks, e.g.:
            [
                {type: "Meal", time: "09:00", label: "Breakfast"},
                {type: "Sightseeing", time: "10:00", poi: {...}},
                {type: "Transportation", time: "11:30", from: A, to: B, ...},
                ...
            ]
    """
    lunch_hour, lunch_minute = map(int, DEFAULT_LUNCH_TIME.split(":"))
    dinner_hour, dinner_minute = map(int, DEFAULT_DINNER_TIME.split(":"))

    day_schedule = []
    current_time = start_time

    # 🍳 Insert breakfast
    if current_time.hour <= 9 and meal_options.get("include_breakfast", True):
        breakfast_block, current_time = insert_breakfast(current_time, day_name, date)
        day_schedule.append(breakfast_block)

    for idx, poi in enumerate(pois):
        # 🥗 Insert lunch if needed
        if (
            meal_options.get("include_lunch", True) and
            (current_time.hour > lunch_hour or
             (current_time.hour == lunch_hour and current_time.minute >= lunch_minute)) and
            not any(x for x in day_schedule if x["type"] == "Meal" and "Lunch" in x["activity"])
        ):
            lunch_block, current_time = insert_lunch(current_time, day_name, date)
            day_schedule.append(lunch_block)

        # 📍 Insert POI visit block
        poi_block, current_time = insert_poi_block(current_time, poi, avg_poi_duration, day_name, date)
        day_schedule.append(poi_block)

        # 🚗 Insert transport block
        if idx < len(pois) - 1:
            next_poi = pois[idx + 1]
            travel_time = travel_time_list[idx]
            polyline = polyline_list[idx]
            transport_block, current_time = insert_transport_block(
                current_time, poi, next_poi, travel_time, day_name, date, polyline
            )
            day_schedule.append(transport_block)

        # 🍽️ Insert dinner if needed
        if (
            meal_options.get("include_dinner", True) and
            (current_time.hour >= dinner_hour) and
            not any(x for x in day_schedule if x["type"] == "Meal" and "Dinner" in x["activity"])
        ):
            dinner_block, current_time = insert_dinner(current_time, day_name, date)
            day_schedule.append(dinner_block)

    # 🏨 Final return to hotel
    hotel_block = insert_return_to_hotel(
        current_time,
        datetime.combine(current_time.date(), datetime.strptime(return_time, "%H:%M").time()),
        day_name, date
    )
    day_schedule.append(hotel_block)

    return day_schedule
