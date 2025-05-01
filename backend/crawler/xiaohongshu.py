"""
xiaohongshu.py · Mock Crawler (XHS Simulator)

This module simulates fetching travel-related content from Xiaohongshu (RED) based on
a Point of Interest (POI)'s name and city. It is a mock version used for early-stage
highlight generation and testing, before implementing a real scraper or API integration.

Returned content mimics real user posts from XHS, providing short review texts
and optional note links.

Main Use Case:
--------------
Used by the fusion engine to generate highlight summaries and tags for POIs
when building Tinder-style recommendation cards.

Key Features:
-------------
✅ Keyword-based mock review generator  
✅ Conditional branching for test POIs (e.g. "Pizza", "MoMA")  
✅ Chinese-language simulated reviews to match realistic input  
✅ Lightweight and fast for local development and LLM testing

Output Schema:
--------------
Dict with:
    - "raw_texts": List[str] → simulated user comments
    - "links": List[str] → optional post links

Author: Tripllery AI Backend
"""

from typing import List, Dict

def fetch_reviews_for_poi(name: str, city: str) -> Dict:
    """
    Simulates fetching Xiaohongshu (RED) review content for a given POI.

    This mock function returns Chinese-language post snippets depending on the POI name,
    which are used by the highlight extractor to generate descriptions and tags.

    Args:
        name (str): Name of the Point of Interest (e.g. "Joe's Pizza")
        city (str): Name of the city where the POI is located (e.g. "New York")

    Returns:
        Dict: A dictionary with:
            - "raw_texts": A list of simulated post texts (List[str])
            - "links": A list of optional reference URLs (List[str])
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
