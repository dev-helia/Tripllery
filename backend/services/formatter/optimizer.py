"""
optimizer.py · Intra-day POI Sequence Optimizer

This module optimizes the order of POIs scheduled within the same day
by loosely grouping them based on their geographic proximity using KMeans clustering.

This helps improve itinerary feasibility, especially when no real routing engine is used.

Main Use Case:
--------------
Applied during day-level formatting to make POI sequences feel more natural
and avoid unnecessary long-distance jumps.

Typically used post-splitting, pre-preview.

Key Features:
-------------
✅ KMeans clustering (1–3 groups)  
✅ Respects geographic grouping without strict pathing  
✅ Fast, lightweight optimization  
✅ Works best when POI count ≥ 3

Author: Tripllery AI Backend
"""

from typing import List, Dict
from sklearn.cluster import KMeans
import numpy as np

def optimize_day_order(pois: List[Dict]) -> List[Dict]:
    """
    Optimizes the order of POIs for a single day using spatial clustering.

    Args:
        pois (List[Dict]): List of POIs scheduled for one day,
                           each must include "lat" and "lng".

    Returns:
        List[Dict]: Re-ordered POIs, grouped roughly by proximity.

    Fallback:
        If POI count ≤ 2, returns input list unchanged.
    """
    if len(pois) <= 2:
        return pois

    # Step 1️⃣ Extract coordinates
    coords = np.array([[poi["lat"], poi["lng"]] for poi in pois])

    # Step 2️⃣ Determine number of clusters (max 3)
    n_clusters = min(3, len(pois))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(coords)

    # Step 3️⃣ Group POIs by cluster label
    clustered_pois = {i: [] for i in range(n_clusters)}
    for idx, label in enumerate(labels):
        clustered_pois[label].append(pois[idx])

    # Step 4️⃣ Recombine in cluster order
    ordered = []
    for cluster_id in sorted(clustered_pois.keys()):
        ordered.extend(clustered_pois[cluster_id])

    return ordered
