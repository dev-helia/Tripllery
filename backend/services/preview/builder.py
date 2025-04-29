# /services/preview/builder.py

from datetime import datetime, timedelta
from services.preview.helper import (
    insert_breakfast, insert_lunch, insert_dinner,
    insert_poi_block, insert_transport_block,
    insert_flexible_block, insert_return_to_hotel
)
from services.preview.directions import batch_travel_times
from services.preview.flexible_time import smart_insert_flexible_blocks
from services.preview.constants import DEFAULT_LUNCH_TIME, DEFAULT_DINNER_TIME, DEFAULT_DAY_END_TIME

async def build_full_schedule(rough_plan: dict, options: dict) -> dict:
    """
    Build the full trip schedule from rough plan and user options.
    """
    start_datetime = datetime.fromisoformat(options.get("start_datetime"))
    end_datetime = datetime.fromisoformat(options.get("end_datetime"))
    start_time_of_day = options.get("start_time_of_day", "09:00")
    avg_poi_duration = int(options.get("avg_poi_duration", 90))
    flexible_block = int(options.get("flexible_block", 60))
    transportation_mode = options.get("transportation", "no_car")

    # Pre-calculate dates for each day
    total_days = (end_datetime.date() - start_datetime.date()).days + 1
    date_list = [(start_datetime.date() + timedelta(days=i)).isoformat() for i in range(total_days)]

    full_schedule = {}

    for day_idx, (day_name, pois) in enumerate(rough_plan.items()):
        current_day_date = date_list[day_idx]
        if day_idx == 0:
            current_time = start_datetime
        else:
            current_time = datetime.combine(
                start_datetime.date() + timedelta(days=day_idx),
                datetime.strptime(start_time_of_day, "%H:%M").time()
            )

        # 🌸 Pre-fetch all travel times
        travel_time_list, polyline_list = await batch_travel_times(pois, transportation_mode)

        # 🌸 Build day's basic schedule
        day_schedule = await build_day_schedule(
            pois, current_time, current_day_date, day_name,
            avg_poi_duration,
            travel_time_list, polyline_list
        )

        # 🌸 Smartly insert Flexible Blocks
        day_schedule = smart_insert_flexible_blocks(day_schedule, target_total_flexible_minutes=flexible_block)

        full_schedule[day_name] = day_schedule

    return full_schedule

async def build_day_schedule(pois, start_time, date, day_name, avg_poi_duration, travel_time_list, polyline_list):
    """
    Build the schedule for a single day (without flexible time first).
    """
    lunch_hour, lunch_minute = map(int, DEFAULT_LUNCH_TIME.split(":"))
    dinner_hour, dinner_minute = map(int, DEFAULT_DINNER_TIME.split(":"))
    day_end_hour, day_end_minute = map(int, DEFAULT_DAY_END_TIME.split(":"))

    day_schedule = []
    current_time = start_time

    # Insert Breakfast if early
    if current_time.hour <= 9:
        breakfast_block, current_time = insert_breakfast(current_time, day_name, date)
        day_schedule.append(breakfast_block)

    for idx, poi in enumerate(pois):
        # Insert Lunch if needed
        if (current_time.hour > lunch_hour or (current_time.hour == lunch_hour and current_time.minute >= lunch_minute)) and \
           not any(x for x in day_schedule if x["type"] == "Meal" and "Lunch" in x["activity"]):
            lunch_block, current_time = insert_lunch(current_time, day_name, date)
            day_schedule.append(lunch_block)

        # Insert POI block
        poi_block, current_time = insert_poi_block(current_time, poi, avg_poi_duration, day_name, date)
        day_schedule.append(poi_block)

        # Insert Transportation if not last POI
        if idx < len(pois) - 1:
            next_poi = pois[idx + 1]
            travel_time = travel_time_list[idx]
            polyline = polyline_list[idx]
            transport_block, current_time = insert_transport_block(current_time, poi, next_poi, travel_time, day_name, date, polyline)
            day_schedule.append(transport_block)

        # Insert Dinner if needed
        if (current_time.hour >= dinner_hour) and \
           not any(x for x in day_schedule if x["type"] == "Meal" and "Dinner" in x["activity"]):
            dinner_block, current_time = insert_dinner(current_time, day_name, date)
            day_schedule.append(dinner_block)

    # Insert Return to Hotel
    hotel_block = insert_return_to_hotel(
        current_time,
        datetime.combine(current_time.date(), datetime.strptime(DEFAULT_DAY_END_TIME, "%H:%M").time()),
        day_name, date
    )
    day_schedule.append(hotel_block)

    return day_schedule
