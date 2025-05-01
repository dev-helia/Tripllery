"""
mapping.py · POI Name → Object Mapping Utility

This helper module provides a function to create a fast lookup map from POI names
to their corresponding full POI objects.

It is typically used in the fallback phase of day-plan generation, where a string-based
split (e.g. {"Day 1": ["MoMA", "Joe's Pizza"]}) must be resolved back into real POI dictionaries.

Main Use Case:
--------------
Used during fallback in `formatter_llm.py`, when splitting logic returns only POI names.

Key Features:
-------------
✅ Fast O(1) lookup for POI resolution  
✅ Clean helper function for reuse in multiple formatting modules  
✅ Supports all POIs with unique name fields (assumed unique)

Author: Tripllery AI Backend
"""

from typing import List, Dict

def build_name_to_poi_map(pois: List[Dict]) -> Dict[str, Dict]:
    """
    Builds a mapping from POI name to the corresponding POI object.

    Args:
        pois (List[Dict]): List of POI dictionaries, each with a unique "name" key.

    Returns:
        Dict[str, Dict]: A dictionary where keys are POI names and values are POI objects.

    Example:
        Input:
            [{"name": "MoMA", ...}, {"name": "Joe's Pizza", ...}]
        Output:
            {
                "MoMA": {...},
                "Joe's Pizza": {...}
            }
    """
    return {poi["name"]: poi for poi in pois}
