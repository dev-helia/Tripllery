"""
poi_math.py · Minimum Required POI Calculator

This utility module defines a helper function to calculate
the minimum number of POIs a user must select before a valid trip plan
can be generated, based on trip duration and selected intensity.

Main Use Case:
--------------
Used in both:
- `/recommend` API (to compute `min_required` and pass to frontend)
- Frontend validation before allowing "Proceed to Plan"

Key Features:
-------------
✅ Computes based on date range (inclusive)  
✅ Supports 'chill', 'normal', 'intense' intensities  
✅ Fallback to 1 day if date parsing fails  
✅ Consistent across frontend/backend

Author: Tripllery AI Backend
"""

from datetime import datetime

def get_min_required_pois(intensity: str, start_date: str, end_date: str) -> int:
    """
    Calculate the minimum number of POIs required based on trip duration and intensity.

    Args:
        intensity (str): One of 'chill', 'normal', 'intense'
        start_date (str): ISO format start date (e.g. '2025-04-04')
        end_date (str): ISO format end date (e.g. '2025-04-06')

    Returns:
        int: Minimum number of POIs required to proceed
    """
    try:
        start = datetime.fromisoformat(start_date).date()
        end = datetime.fromisoformat(end_date).date()
        total_days = (end - start).days + 1
        if total_days <= 0:
            raise ValueError("Invalid date range")
    except Exception:
        total_days = 1  # 🛟 fallback: default to 1 day if parsing fails

    intensity = intensity.lower().strip()

    if intensity == "chill":
        return total_days * 1  # ~1 POI/day
    elif intensity == "intense":
        return total_days * 3  # ~3 POIs/day
    else:
        return total_days * 2  # default: ~2 POIs/day (normal)
