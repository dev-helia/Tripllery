"""
recommend_pool.py · Global Recommendation Pool Cache

This module implements a lightweight in-memory caching layer for POI cards
recommended by the `/recommend` route. It exposes helpers to:

- Paginate POIs for lazy loading (`/recommend/more`)
- Look up POIs by ID (`/plan`)
- Reuse previously selected card data without hitting API again

Main Use Case:
--------------
Used by:
- `/recommend`: to store full card pool
- `/recommend/more`: to fetch next batch
- `/plan`: to find selected POIs by ID

Key Features:
-------------
✅ Caches full card list for frontend  
✅ Supports list-based pagination (e.g. 6 at a time)  
✅ Enables ID-based lookup for planning  
✅ Global state (reset every new /recommend call)

Author: Tripllery AI Backend
"""

# ✨ Global cache of recommended cards
recommend_pool_list = []   # Ordered card list for pagination
recommend_pool_dict = {}   # ID → card lookup for fast access


def cache_card_pool(pois: list):
    """
    Save full POI card objects into both list (for order) and dict (for lookup).

    Args:
        pois (list): List of POI cards returned by recommend_agent()
    """
    global recommend_pool_list, recommend_pool_dict
    recommend_pool_list = pois
    recommend_pool_dict = {poi["id"]: poi for poi in pois if "id" in poi}


def get_next_batch(start: int, size: int) -> list:
    """
    Paginate through cached POIs for lazy loading in frontend.

    Args:
        start (int): Starting index
        size (int): Number of cards to return

    Returns:
        list: Slice of cached POIs
    """
    return recommend_pool_list[start:start + size]


def get_pois_by_ids(ids: list) -> list:
    """
    Fetch selected POIs by ID for use in /plan step.

    Args:
        ids (list): List of POI IDs

    Returns:
        list: Corresponding POI dicts
    """
    result = []
    for id_ in ids:
        poi = recommend_pool_dict.get(id_)
        if poi:
            result.append(poi)
        else:
            print(f"⚠️ Warning: Cannot find POI object for id={id_}")
    return result
