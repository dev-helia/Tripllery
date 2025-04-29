from typing import Dict, List

def rebalance_days(plan: Dict[str, List[Dict]], max_pois_per_day: int = 5) -> Dict[str, List[Dict]]:
    """
    Rebalance the day plan to avoid overloading a single day.

    Args:
        plan (Dict[str, List[Dict]]): {'Day 1': [POI1, POI2, ...], 'Day 2': [...], ...}
        max_pois_per_day (int): Maximum allowed POIs per day

    Returns:
        Dict[str, List[Dict]]: Balanced plan
    """
    if not plan:
        return {}

    all_pois = []
    for day_pois in plan.values():
        for poi in day_pois:
            if isinstance(poi, dict):  # 🔥 只收POI对象
                all_pois.append(poi)
            else:
                print(f"⚠️ Skipped non-POI item during rebalance: {poi}")

    balanced_plan = {}
    day_idx = 1

    for i in range(0, len(all_pois), max_pois_per_day):
        chunk = all_pois[i:i + max_pois_per_day]
        balanced_plan[f"Day {day_idx}"] = chunk
        day_idx += 1

    print(f"✅ Rebalanced days: {len(balanced_plan)} days")

    return balanced_plan
