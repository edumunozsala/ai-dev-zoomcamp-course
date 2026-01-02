#!/usr/bin/env python
"""
Example script showing how to use the MCP tools directly.
This demonstrates the functionality of the count_word_in_url tool.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from server import get_jina_content
import re

def count_word_in_url(url: str, word: str) -> dict:
    """
    Count occurrences of a word on a web page using r.jina.ai.
    
    Args:
        url: The URL of the web page to search.
        word: The word to count (case-insensitive).
    
    Returns:
        A dictionary with the count and statistics.
    """
    content = get_jina_content(url)
    if content.startswith("Error"):
        return {"error": content, "count": 0}
    
    # Count with word boundaries (case-insensitive)
    pattern = r'\b' + re.escape(word) + r'\b'
    word_boundary_count = len(re.findall(pattern, content, re.IGNORECASE))
    
    # Count simple substring (case-insensitive)
    substring_count = content.lower().count(word.lower())
    
    return {
        "url": url,
        "word": word,
        "total_characters": len(content),
        "count_word_boundaries": word_boundary_count,
        "count_substring": substring_count,
    }

if __name__ == "__main__":
    # Example: Count "data" on datatalks.club
    result = count_word_in_url("https://datatalks.club/", "data")
    
    print("=" * 60)
    print("WORD COUNT ANALYSIS")
    print("=" * 60)
    print(f"URL: {result['url']}")
    print(f"Word: {result['word']}")
    print(f"Total characters: {result['total_characters']:,}")
    print(f"Word boundary matches: {result['count_word_boundaries']}")
    print(f"Substring matches: {result['count_substring']}")
    print("=" * 60)
