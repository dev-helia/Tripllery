"""
formatter_llm.py · Intelligent Day-Split Formatter

This module provides a hybrid plan formatting strategy:
- First attempts to split POIs across days using LLM
- If LLM fails or returns invalid output, falls back to a deterministic splitter

It ensures that the final output is always a valid `{day → list of POI objects}` structure,
suitable for downstream scheduling (/preview) and frontend display.

Main Use Case:
--------------
Used during the `/plan` route after accepted POIs are selected,
to divide the trip into N days worth of activities.

Key Features:
-------------
✅ Async LLM-based pipeline call  
✅ Safe fallback to rule-based splitter  
✅ Converts string-based fallback back to real POI objects  
✅ Returns dict of `{Day N: [POIs]}`

Author: Tripllery AI Backend
"""

from typing import List, Dict
from services.formatter.pipeline import format_plan_pipeline
from services.formatter.splitter import simple_split_days

async def format_plan_with_llm(pois: List[Dict], days: int, transportation: str = "car") -> Dict[str, List[Dict]]:
    """
    Formats the travel plan by splitting POIs across days using LLM (with fallback).

    Args:
        pois (List[Dict]): List of POIs selected by the user.
        days (int): Total number of travel days.
        transportation (str): Travel mode ("car" or "public") (currently unused in splitting logic).

    Returns:
        Dict[str, List[Dict]]: A mapping of day labels to lists of POI objects:
            {
                "Day 1": [POI1, POI2],
                "Day 2": [POI3, POI4],
                ...
            }

    Fallback Logic:
        - If the LLM-based splitter fails or returns invalid output,
          falls back to rule-based splitter (`simple_split_days`) and resolves POI objects by name.
    """
    try:
        # 🌸 Step 1: Attempt LLM-based splitting
        formatted_plan = await format_plan_pipeline(pois, days)

        if not isinstance(formatted_plan, dict):
            raise ValueError("LLM returned invalid format.")

        return formatted_plan

    except Exception as e:
        print(f"⚠️ format_plan_with_llm fallback because: {e}")

        # 🌸 Step 2: Fallback to rule-based splitter
        fallback_day_name_to_names = simple_split_days(pois, days)

        # 🌸 Step 3: Build name → POI object mapping
        name_to_poi = {poi["name"]: poi for poi in pois}
        final_plan = {}

        # 🌸 Step 4: Resolve names to actual POI objects
        for day, poi_names in fallback_day_name_to_names.items():
            day_pois = []
            for name in poi_names:
                poi_obj = name_to_poi.get(name)
                if poi_obj:
                    day_pois.append(poi_obj)
                else:
                    print(f"⚠️ Warning: Fallback could not find POI object for name: {name}")
            final_plan[day] = day_pois

        # 🌸 Step 5: Return fallback {day → POIs}
        return final_plan
