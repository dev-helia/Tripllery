# /services/utils/recommend_pool.py
# 全局推荐池：保存/recommend生成的所有POI对象，供/plan查找

recommend_pool = {}

def cache_recommend_pois(pois: list):
    """
    Save full POI objects into the recommend pool.
    """
    recommend_pool.clear()
    for poi in pois:
        if "id" in poi:
            recommend_pool[poi["id"]] = poi

def get_pois_by_ids(ids: list) -> list:
    """
    Fetch POI objects from ids.
    """
    result = []
    for id_ in ids:
        poi = recommend_pool.get(id_)
        if poi:
            result.append(poi)
        else:
            print(f"⚠️ Warning: Cannot find POI object for id={id_}")
    return result
