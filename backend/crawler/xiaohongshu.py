"""
Xiaohongshu Crawler · Mock Version

Simulates travel content search for a query, returns sample text posts.
Used for highlight generation before real crawler is implemented.
"""

from typing import List, Dict

def fetch_reviews_for_poi(name: str, city: str) -> Dict:
    """
    Simulate fetching Xiaohongshu content for a POI.

    Args:
        name (str): POI name, e.g. "Joe's Pizza"
        city (str): City name, e.g. "New York"

    Returns:
        Dict: {
            "raw_texts": [ ... ],
            "links": [...]
        }
    """
    if "Pizza" in name:
        return {
            "raw_texts": [
                "芝士拉丝太疯狂了！！我们深夜来吃，真的好香，排队也值得！",
                "适合深夜来和朋友聊天，披萨分量大，味道正宗。"
            ],
            "links": ["https://www.xiaohongshu.com/note/xyz"]
        }
    elif "MoMA" in name:
        return {
            "raw_texts": [
                "MoMA真的太美了，展品超级现代，有点酷有点怪，超适合拍照！",
                "推荐提前买票，不然人超多～我在大厅坐着发呆一个小时，好安静。"
            ],
            "links": ["https://www.xiaohongshu.com/note/abc"]
        }
    else:
        return {
            "raw_texts": [
                f"{name} 在 {city} 是个打卡点，很多人说适合情侣或者拍照。",
                "环境不错，适合轻松放松，不赶时间。"
            ],
            "links": []
        }
