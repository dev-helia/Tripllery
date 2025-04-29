# /services/preview/flexible_time.py

from datetime import datetime, timedelta

def smart_insert_flexible_blocks(day_schedule: list, target_total_flexible_minutes: int = 60) -> list:
    """
    Analyze a day's schedule and smartly insert flexible time blocks.
    
    Args:
        day_schedule (list): List of existing blocks for the day.
        target_total_flexible_minutes (int): Total flexible minutes we want to insert.

    Returns:
        list: Updated day_schedule with inserted flexible blocks.
    """
    # 先找到所有可能插入自由时间的"空隙"（比如POI与POI之间，或者活动块后）
    candidate_gaps = []

    for i in range(len(day_schedule) - 1):
        end_time_curr = parse_time(day_schedule[i]["end_time"])
        start_time_next = parse_time(day_schedule[i+1]["start_time"])

        gap_minutes = (start_time_next - end_time_curr).total_seconds() / 60

        if gap_minutes >= 20:  # 至少20分钟以上的空隙才值得插
            candidate_gaps.append({
                "index": i,
                "gap_minutes": gap_minutes,
                "start_time": end_time_curr,
                "end_time": start_time_next
            })

    # 如果一天非常紧凑，没空隙，直接返回
    if not candidate_gaps:
        return day_schedule

    # 分配Flexible时间：均匀往空隙里塞
    remaining_flexible_minutes = target_total_flexible_minutes
    updated_schedule = []
    offset = 0  # 用来动态调整插入位置

    for idx, block in enumerate(day_schedule):
        updated_schedule.append(block)

        # 检查当前块后是否有空隙可插
        matching_gap = next((gap for gap in candidate_gaps if gap["index"] == idx), None)

        if matching_gap and remaining_flexible_minutes > 0:
            # 本空隙可以插入的自由时间：不能超过gap本身的一半
            insert_minutes = min(remaining_flexible_minutes, matching_gap["gap_minutes"] * 0.5)
            insert_minutes = max(20, insert_minutes)  # 至少20分钟一块

            if insert_minutes < remaining_flexible_minutes:
                # 插入Flexible Block
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
    Parse a time string like '09:00' into a datetime object (date part dummy).

    Args:
        time_str (str): Time string in format "HH:MM".

    Returns:
        datetime: Dummy datetime object.
    """
    return datetime.strptime(time_str, "%H:%M")
