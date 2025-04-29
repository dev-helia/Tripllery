# /services/formatter/mapping.py

from typing import List, Dict

def build_name_to_poi_map(pois: List[Dict]) -> Dict[str, Dict]:
    """
    Build a mapping from POI name to POI object.
    """
    return {poi["name"]: poi for poi in pois}
