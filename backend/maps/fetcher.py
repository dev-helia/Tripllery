"""
fetcher.py · Google Maps POI Fetcher (Enhanced SDK Version)

This module connects to the Google Maps Places API via the official SDK
to fetch Points of Interest (POIs) based on user query keywords and cities.

It returns cleaned, structured POI data including:
- Name, coordinates, rating
- Address and Google Maps link
- Optional photo URL (from photo_reference)
- Opening hours (if available)

Main Use Case:
--------------
Used by the Tripllery backend to search real POIs for recommendation,
based on queries generated from user interests and city input.

Key Features:
-------------
✅ Uses official `googlemaps.Client` SDK  
✅ Auto-appends city to query for contextual accuracy  
✅ Fetches photo reference and constructs image URL  
✅ Includes opening hours and location info  
✅ Returns a unified POI dictionary format for downstream fusion

Author: Tripllery AI Backend
"""

import os
from dotenv import load_dotenv
import googlemaps
from typing import List, Dict

# 🔐 Load API key from environment
load_dotenv()
api_key = os.getenv("GOOGLE_MAPS_API_KEY")
gmaps = googlemaps.Client(key=api_key)

def search_google_maps(query: str, city: str, limit=5, radius=5000) -> List[Dict]:
    """
    Searches Google Maps for Points of Interest using a keyword query.

    Args:
        query (str): Keyword describing the place (e.g. "brunch", "museums", "cheap eats")
        city (str): City name to constrain the search (e.g. "Boston")
        limit (int): Maximum number of results to return (default: 5)
        radius (int): Search radius in meters from central point (default: 5000)

    Returns:
        List[Dict]: A list of POI dictionaries, each containing:
            - name: str
            - lat: float
            - lng: float
            - rating: float or None
            - address: str
            - maps_url: str (Google Maps link)
            - image_url: str (either real or fallback image)
            - opening_hours: List[str] (optional, weekday_text)
            - city: str
    """

    # Send search request to Google Places API
    response = gmaps.places(query=f"{query} in {city}", radius=radius)
    results = response.get("results", [])
    pois = []

    # DEBUG: Print API key use (remove or log in prod)
    print("🔑 GOOGLE_MAPS_API_KEY =", api_key)

    # Build structured result objects
    for place in results[:limit]:
        photo_ref = None
        image_url = None

        if "photos" in place:
            # Extract first photo reference and build static image URL
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
