# /services/formatter/pipeline.py

from typing import List, Dict
from services.formatter.splitter import intelligent_split_days
from services.formatter.optimizer import optimize_day_order
from services.formatter.mapping import build_name_to_poi_map

async def format_plan_pipeline(pois: List[Dict], days: int) -> Dict[str, List[Dict]]:
    """
    Pipeline: Smart day split + optimize each day.
    """
    if not pois or days <= 0:
        raise ValueError("Invalid POIs or days")

    # Step 1: Intelligent split
    day_plan = await intelligent_split_days(pois, days)

    # Step 2: Build name lookup
    name_to_poi = build_name_to_poi_map(pois)

    # Step 3: Assemble and optimize
    final_plan = {}

    for day, names in day_plan.items():
        day_pois = [name_to_poi[name] for name in names if name in name_to_poi]
        optimized_day = optimize_day_order(day_pois)
        final_plan[day] = optimized_day

    return final_plan
