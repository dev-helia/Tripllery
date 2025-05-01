"""
query_generator.py · Tripllery V3 Query Builder

This module generates search queries based on user travel preferences and city routes.

It constructs search phrases like:
    "New York museums", "Boston nightlife", etc.
for each stop along the trip — including the main destination and optional stopover cities.

The queries are used by downstream crawler components (e.g. Google Maps or Xiaohongshu)
to retrieve POIs relevant to the user's interests.

Main Use Case:
--------------
This function is called during the early recommendation pipeline to transform AI-tagged
interests into city-specific search prompts for external data sources.

Key Features:
-------------
✅ Accepts structured interests (e.g. ["nature", "coffee shops", "art galleries"])  
✅ Supports multi-city trips (via stopovers)  
✅ Normalized query format for crawler input  
✅ Fully deterministic, no randomness

Input:
------
- destination: str → The final destination city  
- stopovers: List[str] → Any cities visited along the way  
- interest_keywords: List[str] → Tags representing user interest or LLM-extracted topics

Output:
-------
Dict[str, List[str]] → Mapping from city to list of search queries

Example Output:
---------------
{
    "Boston": ["Boston museums", "Boston brunch"],
    "Providence": ["Providence museums", "Providence brunch"]
}

Author: Tripllery AI Backend
"""

from typing import List, Dict

def generate_queries(destination: str, stopovers: List[str], interest_keywords: List[str]) -> Dict[str, List[str]]:
    """
    Generates a dictionary mapping each city to a list of search queries based on keywords.

    This function combines user interests with destination and stopover cities
    to form location-specific search prompts for POI discovery.

    Args:
        destination (str): Final destination city (e.g. "New York")
        stopovers (List[str]): List of stopover cities (e.g. ["New Haven"])
        interest_keywords (List[str]): List of keyword strings (e.g. ["museums", "romantic dinner"])

    Returns:
        Dict[str, List[str]]: City → list of queries to use with crawler/maps

    Example:
        {
            "New York": ["New York museums", "New York romantic dinner"],
            "New Haven": ["New Haven museums", "New Haven romantic dinner"]
        }
    """
    cities = [destination] + stopovers
    result = {}

    for city in cities:
        result[city] = [f"{city} {kw}" for kw in interest_keywords if kw.strip()]

    return result
