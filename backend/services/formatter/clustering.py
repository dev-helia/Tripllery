"""
clustering.py · POI Location-Based Sorter (Mini Clustering)

This module provides lightweight geographic clustering for POIs based on
their latitude and longitude, using KMeans.

It groups POIs into up to 2 clusters, then returns a merged list that preserves
local proximity — useful for generating plans with fewer long-distance jumps.

Main Use Case:
--------------
Optional enhancement during /plan or /preview logic to sort POIs
in a way that mimics location-aware route optimization (especially when no real map routing is used).

Key Features:
-------------
✅ Uses lat/lng to group nearby POIs  
✅ KMeans clustering (min(2, N)) for simplicity  
✅ Returns sorted POIs across clusters  
✅ Works even without car (adaptive to low-mobility trips)

Author: Tripllery AI Backend
"""

from typing import List, Dict
from sklearn.cluster import KMeans
import numpy as np

def sort_pois_by_location(pois: List[Dict], transportation: str = "no_car") -> List[Dict]:
    """
    Sorts POIs based on rough geographic proximity using basic clustering.

    This function groups POIs using KMeans (up to 2 clusters),
    then returns a reordered list to favor intra-cluster transitions.

    Args:
        pois (List[Dict]): List of POIs (each with "lat" and "lng")
        transportation (str): User mobility context, "car" or "no_car"

    Returns:
        List[Dict]: Sorted POI list based on cluster membership

    Note:
        - For ≤2 POIs, original list is returned.
        - Does not perform actual routing — just loose spatial grouping.
    """
    if len(pois) <= 2:
        return pois

    coords = np.array([[poi["lat"], poi["lng"]] for poi in pois])

    # Cluster into 1 or 2 groups depending on count
    kmeans = KMeans(n_clusters=min(2, len(pois)), random_state=42).fit(coords)
    labels = kmeans.labels_

    sorted_pois = []
    for cluster in range(max(labels) + 1):
        cluster_pois = [poi for idx, poi in enumerate(pois) if labels[idx] == cluster]
        sorted_pois.extend(cluster_pois)

    return sorted_pois
