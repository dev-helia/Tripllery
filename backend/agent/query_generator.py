"""
Query Generator · Tripllery V3

Generates search queries based on:
- Destination city + stopovers
- Structured keywords (from LLM or user-selected)

Now accepts: interest_keywords: List[str]
"""

from typing import List, Dict

def generate_queries(destination: str, stopovers: List[str], interest_keywords: List[str]) -> Dict[str, List[str]]:
    """
    Generates a dictionary of {city: [query1, query2, ...]} based on structured keywords.

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
