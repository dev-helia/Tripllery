"""
resolver.py · Final Plan Rebalancer (Post-Split Normalizer)

This module ensures that a generated day-to-POIs plan is valid,
by rebundling POIs into evenly distributed days.

It prevents:
- Empty days (e.g. {"Day 3": []})
- Overloaded days (e.g. {"Day 1": [8 POIs]})

Usually called at the end of the `/plan` route as a final adjustment pass.

Main Use Case:
--------------
Used after formatting or LLM-based splits to smooth out overfilled/underfilled days.

Key Features:
-------------
✅ Removes invalid POI entries (non-dict)  
✅ Splits into fixed-size chunks  
✅ Skips empty days  
✅ Consistent day labels: "Day 1", "Day 2", ...

Author: Tripllery AI Backend
"""

from typing import Dict, List

def rebalance_days(plan: Dict[str, List[Dict]], max_pois_per_day: int = 5) -> Dict[str, List[Dict]]:
    """
    Rebalances the day plan by distributing POIs evenly and avoiding empty days.

    Args:
        plan (Dict[str, List[Dict]]): Raw plan with possible imbalance, like:
            {
                "Day 1": [POI1, POI2, POI3, POI4, POI5, POI6],
                "Day 2": []
            }
        max_pois_per_day (int): Max number of POIs per day

    Returns:
        Dict[str, List[Dict]]: Cleaned and restructured plan with balanced POIs, e.g.:
            {
                "Day 1": [POI1, POI2, POI3],
                "Day 2": [POI4, POI5, POI6]
            }
    """
    if not plan:
        return {}

    # Step 1️⃣ Flatten all valid POIs
    all_pois = []
    for day_pois in plan.values():
        for poi in day_pois:
            if isinstance(poi, dict):
                all_pois.append(poi)
            else:
                print(f"⚠️ Skipped non-POI item during rebalance: {poi}")

    # Step 2️⃣ If no valid POIs, return empty plan
    if not all_pois:
        print("⚠️ No valid POIs found for rebalancing.")
        return {}

    # Step 3️⃣ Chunk POIs and reassign to new days
    balanced_plan = {}
    day_idx = 1

    for i in range(0, len(all_pois), max_pois_per_day):
        chunk = all_pois[i:i + max_pois_per_day]
        if chunk:  # Only non-empty days
            balanced_plan[f"Day {day_idx}"] = chunk
            day_idx += 1

    print(f"✅ Rebalanced days: {len(balanced_plan)} non-empty days")
    return balanced_plan
