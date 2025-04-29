# /services/clustering.py

from typing import List, Dict
from sklearn.cluster import KMeans
import numpy as np

def sort_pois_by_location(pois: List[Dict], transportation: str = "no_car") -> List[Dict]:
    """
    Sort POIs by proximity (basic clustering).

    Args:
        pois (List[Dict]): POI list
        transportation (str): "car" or "no_car"

    Returns:
        List[Dict]: Sorted POIs
    """
    if len(pois) <= 2:
        return pois

    coords = np.array([[poi["lat"], poi["lng"]] for poi in pois])

    # KMeans clustering
    kmeans = KMeans(n_clusters=min(2, len(pois)), random_state=42).fit(coords)
    labels = kmeans.labels_

    sorted_pois = []
    for cluster in range(max(labels) + 1):
        cluster_pois = [poi for idx, poi in enumerate(pois) if labels[idx] == cluster]
        sorted_pois.extend(cluster_pois)

    return sorted_pois
