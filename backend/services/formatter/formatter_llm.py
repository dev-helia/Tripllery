from typing import List, Dict
from services.formatter.pipeline import format_plan_pipeline
from services.formatter.splitter import simple_split_days

async def format_plan_with_llm(pois: List[Dict], days: int, transportation: str = "car") -> Dict[str, List[Dict]]:
    """
    Format the travel plan using LLM with fallback to simple splitting.
    Args:
        pois (List[Dict]): POIs.
        days (int): Total travel days (must be passed in).
        transportation (str): Transport mode.

    Returns:
        Dict[str, List[Dict]]: Day to POIs mapping.
    """
    try:
        # 🌸 Step 1: Try LLM intelligent splitting
        formatted_plan = await format_plan_pipeline(pois, days)

        if not isinstance(formatted_plan, dict):
            raise ValueError("LLM returned invalid format.")

        return formatted_plan

    except Exception as e:
        print(f"⚠️ format_plan_with_llm fallback because: {e}")

        # 🌸 Step 2: fallback到 simple_split_days
        fallback_day_name_to_names = simple_split_days(pois, days)

        # 🌸 Step 3: 建立名字到POI对象的mapping
        name_to_poi = {poi["name"]: poi for poi in pois}

        final_plan = {}

        # 🌸 Step 4: 通过名字补全成POI对象
        for day, poi_names in fallback_day_name_to_names.items():
            day_pois = []
            for name in poi_names:
                poi_obj = name_to_poi.get(name)
                if poi_obj:
                    day_pois.append(poi_obj)
                else:
                    print(f"⚠️ Warning: Fallback找不到POI对象：{name}")
            final_plan[day] = day_pois

        # 🌸 Step 5: 确保 fallback输出的是 {day: [POI对象]}
        return final_plan
