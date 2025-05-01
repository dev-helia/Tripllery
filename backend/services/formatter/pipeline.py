"""
pipeline.py · Tripllery Day-Split Pipeline

This module defines the full formatting pipeline to convert a list of POIs
into a multi-day plan. It combines:

- LLM-based intelligent splitting (`intelligent_split_days`)
- Mapping from POI names to full POI objects
- Intra-day spatial optimization (`optimize_day_order`)

This pipeline ensures both logical day grouping and geographical order,
preparing a structured output ready for preview scheduling.

Main Use Case:
--------------
Called by `formatter_llm.py` as the primary splitter method.
Activated when LLM-based day plans are desired.

Key Features:
-------------
✅ Combines multiple formatter utilities in sequence  
✅ Day-level splitting based on semantic diversity  
✅ Spatial sorting within each day  
✅ Output: Dict[Day → List[POI objects]]

Author: Tripllery AI Backend
"""

from typing import List, Dict
from services.formatter.splitter import intelligent_split_days
from services.formatter.optimizer import optimize_day_order
from services.formatter.mapping import build_name_to_poi_map

async def format_plan_pipeline(pois: List[Dict], days: int) -> Dict[str, List[Dict]]:
    """
    Runs the full formatting pipeline: smart split ➜ mapping ➜ day optimization.

    Args:
        pois (List[Dict]): List of POIs to distribute across days.
        days (int): Total number of trip days.

    Returns:
        Dict[str, List[Dict]]: Final multi-day plan with optimized POI lists per day.
            {
                "Day 1": [POI1, POI2],
                "Day 2": [POI3, POI4],
                ...
            }

    Raises:
        ValueError: If POIs list is empty or days ≤ 0.
    """
    if not pois or days <= 0:
        raise ValueError("Invalid POIs or days")

    # Step 1️⃣ Intelligent day splitting (LLM or heuristic)
    day_plan = await intelligent_split_days(pois, days)

    # Step 2️⃣ Build mapping: POI name → POI object
    name_to_poi = build_name_to_poi_map(pois)

    # Step 3️⃣ For each day: resolve names + optimize order
    final_plan = {}

    for day, names in day_plan.items():
        day_pois = [name_to_poi[name] for name in names if name in name_to_poi]
        optimized_day = optimize_day_order(day_pois)
        final_plan[day] = optimized_day

    return final_plan
