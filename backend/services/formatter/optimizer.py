# /services/formatter/optimizer.py

from typing import List, Dict
from sklearn.cluster import KMeans
import numpy as np

def optimize_day_order(pois: List[Dict]) -> List[Dict]:
    """
    Optimize the order of POIs for a day by geographic clustering.
    """
    if len(pois) <= 2:
        return pois

    coords = np.array([[poi["lat"], poi["lng"]] for poi in pois])

    n_clusters = min(3, len(pois))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(coords)

    clustered_pois = {i: [] for i in range(n_clusters)}
    for idx, label in enumerate(labels):
        clustered_pois[label].append(pois[idx])

    ordered = []
    for cluster_id in sorted(clustered_pois.keys()):
        ordered.extend(clustered_pois[cluster_id])

    return ordered
