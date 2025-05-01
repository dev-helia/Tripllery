"""
helper.py · Time Block Constructors

This module provides reusable helper functions for creating individual
time blocks (meals, sightseeing, transport, free time, return) used
in the daily itinerary.

Each function returns a block dictionary (with start_time, end_time, type, etc.)
and an updated current_time for chaining.

Main Use Case:
--------------
Used in `build_day_schedule()` inside `/preview` to construct
hour-by-hour trip timeline from POI data and user preferences.

Key Features:
-------------
✅ Consistent time format ("HH:MM")  
✅ Supports location + POI IDs  
✅ Works with polyline for transport  
✅ Chainable (returns block + updated time)

Author: Tripllery AI Backend
"""

from datetime import datetime, timedelta

def insert_breakfast(current_time, day, date):
    breakfast_start = current_time
    breakfast_end = breakfast_start + timedelta(minutes=30)
    block = {
        "day": day,
        "date": date,
        "start_time": breakfast_start.strftime("%H:%M"),
        "end_time": breakfast_end.strftime("%H:%M"),
        "type": "Meal",
        "activity": "Breakfast",
        "location": None
    }
    return block, breakfast_end


def insert_lunch(current_time, day, date):
    lunch_start = current_time
    lunch_end = lunch_start + timedelta(minutes=60)
    block = {
        "day": day,
        "date": date,
        "start_time": lunch_start.strftime("%H:%M"),
        "end_time": lunch_end.strftime("%H:%M"),
        "type": "Meal",
        "activity": "Lunch Break",
        "location": None
    }
    return block, lunch_end


def insert_dinner(current_time, day, date):
    dinner_start = current_time
    dinner_end = dinner_start + timedelta(minutes=60)
    block = {
        "day": day,
        "date": date,
        "start_time": dinner_start.strftime("%H:%M"),
        "end_time": dinner_end.strftime("%H:%M"),
        "type": "Meal",
        "activity": "Dinner Break",
        "location": None
    }
    return block, dinner_end


def insert_poi_block(current_time, poi, duration_minutes, day, date):
    poi_start = current_time
    poi_end = poi_start + timedelta(minutes=duration_minutes)
    block = {
        "day": day,
        "date": date,
        "start_time": poi_start.strftime("%H:%M"),
        "end_time": poi_end.strftime("%H:%M"),
        "type": "Sightseeing",
        "activity": poi["name"],
        "id": poi.get("id"),
        "location": {
            "lat": poi.get("lat"),
            "lng": poi.get("lng")
        }
    }
    return block, poi_end


def insert_transport_block(current_time, from_poi, to_poi, transport_time_minutes, day, date, polyline=None):
    transport_start = current_time
    transport_end = transport_start + timedelta(minutes=transport_time_minutes)

    if transport_time_minutes <= 1:
        activity_name = f"Transportation (~1 min) {from_poi['name']} ➔ {to_poi['name']}"
    else:
        activity_name = f"Transportation ({transport_time_minutes} min) {from_poi['name']} ➔ {to_poi['name']}"

    block = {
        "day": day,
        "date": date,
        "start_time": transport_start.strftime("%H:%M"),
        "end_time": transport_end.strftime("%H:%M"),
        "type": "Transportation",
        "activity": activity_name,
        "from_id": from_poi.get("id"),
        "to_id": to_poi.get("id"),
        "from_location": {
            "lat": from_poi.get("lat"),
            "lng": from_poi.get("lng")
        },
        "to_location": {
            "lat": to_poi.get("lat"),
            "lng": to_poi.get("lng")
        },
        "polyline": polyline
    }
    return block, transport_end


def insert_flexible_block(current_time, flexible_minutes, day, date):
    flex_start = current_time
    flex_end = flex_start + timedelta(minutes=flexible_minutes)
    block = {
        "day": day,
        "date": date,
        "start_time": flex_start.strftime("%H:%M"),
        "end_time": flex_end.strftime("%H:%M"),
        "type": "Flexible",
        "activity": "Free Time / Explore",
        "location": None
    }
    return block, flex_end


def insert_return_to_hotel(current_time, day_end_time, day, date):
    return_start = current_time
    return_end = day_end_time
    block = {
        "day": day,
        "date": date,
        "start_time": return_start.strftime("%H:%M"),
        "end_time": return_end.strftime("%H:%M"),
        "type": "Return",
        "activity": "Return to Hotel",
        "location": None
    }
    return block
