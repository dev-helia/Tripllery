"""
directions.py · Google Maps Travel Time Engine

This module interfaces with the Google Maps Directions API to estimate
travel durations and polylines between pairs of POIs.

It provides both single-request and batch-request methods, as well as a fallback mechanism
in case of API failure, using default travel durations from constants.

Main Use Case:
--------------
Used during `/preview` to generate:
- Travel time estimates (in minutes) between POIs
- Polyline routes for map display

Key Features:
-------------
✅ Supports car and public transport modes  
✅ Batches route estimation for performance  
✅ Graceful fallback on API errors  
✅ Returns both minutes + map polyline per hop

Author: Tripllery AI Backend
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv
from services.preview.constants import (
    FALLBACK_TRANSPORT_MINUTES_CAR,
    FALLBACK_TRANSPORT_MINUTES_NO_CAR,
    TRANSPORT_MODE_HAVE_CAR,
    TRANSPORT_MODE_NO_CAR,
)

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
DIRECTIONS_API_URL = "https://maps.googleapis.com/maps/api/directions/json"


async def fetch_direction(origin: tuple, destination: tuple, transportation_mode: str = TRANSPORT_MODE_HAVE_CAR) -> dict:
    """
    Fetch travel time and polyline between two coordinates using Google Maps API.

    Args:
        origin (tuple): (lat, lng)
        destination (tuple): (lat, lng)
        transportation_mode (str): "have_car" or "no_car"

    Returns:
        dict: {
            "minutes": travel_time_minutes,
            "polyline": encoded_polyline_string or None
        }
    """
    if not GOOGLE_MAPS_API_KEY:
        raise Exception("Google Maps API Key not set!")

    if transportation_mode == TRANSPORT_MODE_HAVE_CAR:
        mode = "driving"
    elif transportation_mode == TRANSPORT_MODE_NO_CAR:
        mode = "transit"
    else:
        mode = "driving"

    params = {
        "origin": f"{origin[0]},{origin[1]}",
        "destination": f"{destination[0]},{destination[1]}",
        "mode": mode,
        "key": GOOGLE_MAPS_API_KEY
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(DIRECTIONS_API_URL, params=params)
            data = response.json()

            if data.get("status") != "OK":
                raise Exception(f"Directions API error: {data.get('status', 'Unknown error')}")

            duration_seconds = data["routes"][0]["legs"][0]["duration"]["value"]
            polyline = data["routes"][0]["overview_polyline"]["points"]

            duration_minutes = max(1, duration_seconds // 60)

            return {
                "minutes": duration_minutes,
                "polyline": polyline
            }

    except Exception as e:
        print(f"💥 Directions API fetch failed: {e}")
        fallback_minutes = (
            FALLBACK_TRANSPORT_MINUTES_CAR
            if transportation_mode == TRANSPORT_MODE_HAVE_CAR
            else FALLBACK_TRANSPORT_MINUTES_NO_CAR
        )
        return {
            "minutes": fallback_minutes,
            "polyline": None
        }


async def batch_fetch_directions(pairs: list, transportation_mode: str = TRANSPORT_MODE_HAVE_CAR) -> list:
    """
    Fetch multiple directions in parallel.

    Args:
        pairs (list): List of (origin, destination) tuples
        transportation_mode (str): "have_car" or "no_car"

    Returns:
        list of dicts: [{"minutes": ..., "polyline": ...}, ...]
    """
    tasks = [fetch_direction(origin, destination, transportation_mode) for origin, destination in pairs]
    results = await asyncio.gather(*tasks)
    return results


async def batch_travel_times(pois: list, transportation_mode: str = TRANSPORT_MODE_HAVE_CAR) -> tuple:
    """
    Given a list of POIs, fetch travel durations and polylines between each adjacent pair.

    Args:
        pois (list): List of POIs (with 'lat' and 'lng')
        transportation_mode (str): "have_car" or "no_car"

    Returns:
        Tuple:
            - travel_times: list of minutes
            - polylines: list of encoded polyline strings
    """
    if not pois or len(pois) < 2:
        return [], []

    poi_pairs = []
    for i in range(len(pois) - 1):
        origin = (pois[i]['lat'], pois[i]['lng'])
        destination = (pois[i + 1]['lat'], pois[i + 1]['lng'])
        poi_pairs.append((origin, destination))

    directions_results = await batch_fetch_directions(poi_pairs, transportation_mode)

    travel_times = []
    polylines = []

    for result in directions_results:
        travel_times.append(result.get('minutes', 10))  # fallback 10 min
        polylines.append(result.get('polyline'))

    return travel_times, polylines
