# /maps/poi_cleaner.py

from typing import List, Dict
from geopy.distance import geodesic

def clean_pois(pois: List[Dict], max_distance_km: float = 50.0, min_required: int = 5) -> List[Dict]:
    """
    Clean up POIs by removing geographically distant outliers.
    If too few POIs remain, return original list (with warning).

    Args:
        pois (List[Dict]): List of raw POIs
        max_distance_km (float): Maximum allowed distance from city center
        min_required (int): Minimum number of POIs to keep

    Returns:
        List[Dict]: Cleaned POIs
    """
    if not pois:
        return []

    # Step 1️⃣ Estimate a rough city center (average lat/lng)
    avg_lat = sum(poi["lat"] for poi in pois) / len(pois)
    avg_lng = sum(poi["lng"] for poi in pois) / len(pois)
    center = (avg_lat, avg_lng)

    print(f"📍 Estimated center: {center}")

    # Step 2️⃣ Filter out POIs too far from center
    cleaned = []
    for poi in pois:
        poi_loc = (poi["lat"], poi["lng"])
        distance = geodesic(center, poi_loc).kilometers
        if distance <= max_distance_km:
            cleaned.append(poi)
        else:
            print(f"⚠️ Removed outlier POI: {poi['name']} ({distance:.1f} km away)")

    # Step 3️⃣ If cleaning made POIs too few, fallback to original list
    if len(cleaned) < min_required:
        print(f"⚠️ Cleaned POIs too few ({len(cleaned)} left), reverting to original list.")
        return pois

    print(f"✅ Cleaned POIs: {len(cleaned)} kept.")
    return cleaned
