"""
flexible_time.py · Free Time Block Inserter

This module scans the existing day schedule and smartly inserts
"Flexible" time blocks (e.g. rest, explore, shopping) into valid time gaps
between activities, without violating meal or POI structure.

Main Use Case:
--------------
Called at the end of each `build_day_schedule()` step to enrich the timeline
with human-friendly breathing space.

Key Features:
-------------
✅ Identifies 20min+ gaps between activities  
✅ Evenly distributes flexible time  
✅ Targets a total user-defined duration (e.g. 60min/day)  
✅ Skips tight schedules gracefully  
✅ Maintains existing time order

Author: Tripllery AI Backend
"""

from datetime import datetime, timedelta


def smart_insert_flexible_blocks(day_schedule: list, target_total_flexible_minutes: int = 60) -> list:
    """
    Analyze a day's schedule and smartly insert flexible time blocks.

    Args:
        day_schedule (list): List of existing blocks (with start_time/end_time)
        target_total_flexible_minutes (int): Total desired "Free Time" minutes

    Returns:
        list: Updated schedule including inserted "Flexible" blocks
    """
    candidate_gaps = []

    # Step 1️⃣: Scan for gaps ≥ 20min between activities
    for i in range(len(day_schedule) - 1):
        end_time_curr = parse_time(day_schedule[i]["end_time"])
        start_time_next = parse_time(day_schedule[i + 1]["start_time"])

        gap_minutes = (start_time_next - end_time_curr).total_seconds() / 60

        if gap_minutes >= 20:
            candidate_gaps.append({
                "index": i,
                "gap_minutes": gap_minutes,
                "start_time": end_time_curr,
                "end_time": start_time_next
            })

    # Step 2️⃣: If no valid gaps, skip inserting
    if not candidate_gaps:
        return day_schedule

    # Step 3️⃣: Evenly insert Flexible blocks into gaps
    remaining_flexible_minutes = target_total_flexible_minutes
    updated_schedule = []

    for idx, block in enumerate(day_schedule):
        updated_schedule.append(block)

        # Match this block to any gap after it
        matching_gap = next((gap for gap in candidate_gaps if gap["index"] == idx), None)

        if matching_gap and remaining_flexible_minutes > 0:
            # Limit insert time: half the gap or remaining
            insert_minutes = min(remaining_flexible_minutes, matching_gap["gap_minutes"] * 0.5)
            insert_minutes = max(20, insert_minutes)  # Minimum chunk

            if insert_minutes < remaining_flexible_minutes:
                flexible_start = matching_gap["start_time"]
                flexible_end = flexible_start + timedelta(minutes=insert_minutes)

                flex_block = {
                    "day": block.get("day"),
                    "date": block.get("date"),
                    "start_time": flexible_start.strftime("%H:%M"),
                    "end_time": flexible_end.strftime("%H:%M"),
                    "type": "Flexible",
                    "activity": "Free Time / Explore",
                    "location": None
                }

                updated_schedule.append(flex_block)
                remaining_flexible_minutes -= insert_minutes

    return updated_schedule


def parse_time(time_str: str) -> datetime:
    """
    Parse a "HH:MM" string into datetime (dummy date).

    Args:
        time_str (str): Time in "09:00" format

    Returns:
        datetime: Dummy datetime object
    """
    return datetime.strptime(time_str, "%H:%M")
