"""
poi_cleaner.py · POI Geolocation Filter

This module post-processes raw POIs retrieved from external sources
(e.g. Google Maps API) by filtering out geographically distant outliers.

It computes a rough city center by averaging all POI coordinates,
then removes entries that fall outside a defined radius.

Main Use Case:
--------------
Used in Tripllery's POI preparation phase to improve location precision
and avoid suggesting irrelevant or faraway places.

Key Features:
-------------
✅ Dynamic center calculation (mean latitude & longitude)  
✅ Outlier detection via geodesic distance (km)  
✅ Safety fallback: reverts to original list if too many are removed  
✅ Useful in cities with noisy or scattered data results

Recommended Pairing:
--------------------
Place this module immediately after `fetcher.py` to sanitize POI results
before feeding them to the recommendation fusion engine.

Author: Tripllery AI Backend
"""

from typing import List, Dict
from geopy.distance import geodesic

def clean_pois(pois: List[Dict], max_distance_km: float = 50.0, min_required: int = 5) -> List[Dict]:
    """
    Cleans a list of POIs by removing those too far from the city center estimate.

    This function:
    - Computes a rough geographic center from all POIs
    - Filters out POIs whose distance exceeds `max_distance_km`
    - Ensures a minimum number of POIs is kept, or falls back to the original list

    Args:
        pois (List[Dict]): Raw list of POIs (must contain lat/lng for each entry)
        max_distance_km (float): Max distance from center in kilometers (default: 50.0)
        min_required (int): Minimum number of POIs needed after filtering (default: 5)

    Returns:
        List[Dict]: Cleaned list of POIs within acceptable distance, or original list if fallback triggered.
    """

    if not pois:
        return []

    # Step 1️⃣ Estimate rough center of city based on average coordinates
    avg_lat = sum(poi["lat"] for poi in pois) / len(pois)
    avg_lng = sum(poi["lng"] for poi in pois) / len(pois)
    center = (avg_lat, avg_lng)

    print(f"📍 Estimated center: {center}")

    # Step 2️⃣ Filter out POIs too far from estimated center
    cleaned = []
    for poi in pois:
        poi_loc = (poi["lat"], poi["lng"])
        distance = geodesic(center, poi_loc).kilometers
        if distance <= max_distance_km:
            cleaned.append(poi)
        else:
            print(f"⚠️ Removed outlier POI: {poi['name']} ({distance:.1f} km away)")

    # Step 3️⃣ Fallback: If too few remain, return the original unfiltered list
    if len(cleaned) < min_required:
        print(f"⚠️ Cleaned POIs too few ({len(cleaned)} left), reverting to original list.")
        return pois

    print(f"✅ Cleaned POIs: {len(cleaned)} kept.")
    return cleaned
