"""
Google Maps Fetcher · Enhanced SDK Version

Uses googlemaps.Client to fetch POIs, and includes photo + opening_hours.
"""

import os
from dotenv import load_dotenv
import googlemaps
from typing import List, Dict

load_dotenv()
api_key = os.getenv("GOOGLE_MAPS_API_KEY")
gmaps = googlemaps.Client(key=api_key)

def search_google_maps(query: str, city: str, limit=5, radius=5000) -> List[Dict]:
    """
    Uses Google Places API to search POIs.

    Args:
        query (str): Keywords like "cheap eats"
        city (str): e.g. "New York"
        limit (int): Max number of POIs to return
        radius (int): Search radius in meters

    Returns:
        List[Dict]: Cleaned POI list with optional image + hours
    """

    response = gmaps.places(query=f"{query} in {city}", radius=radius)
    results = response.get("results", [])
    pois = []
    # TODO DEBUG
    print("🔑 GOOGLE_MAPS_API_KEY =", api_key)
    for place in results[:limit]:
        photo_ref = None
        image_url = None

        if "photos" in place:
            # Get the first photo reference
            photo_ref = place["photos"][0]["photo_reference"]
            image_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=600&photoreference={photo_ref}&key={api_key}"

        opening_hours = place.get("opening_hours", {}).get("weekday_text", [])

        pois.append({
            "name": place.get("name"),
            "lat": place["geometry"]["location"]["lat"],
            "lng": place["geometry"]["location"]["lng"],
            "rating": place.get("rating"),
            "address": place.get("formatted_address"),
            "maps_url": f"https://www.google.com/maps/search/{place.get('name').replace(' ', '+')}",
            "image_url": image_url or "https://via.placeholder.com/400x300.png?text=No+Image",
            "opening_hours": opening_hours,
            "city": city
        })

    return pois
