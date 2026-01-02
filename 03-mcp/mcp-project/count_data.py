#!/usr/bin/env python
"""Script to count occurrences of 'data' on https://datatalks.club/ using the MCP tool"""

import requests
import re

def get_jina_content(url: str) -> str:
    """Fetch content using r.jina.ai"""
    jina_url = f"https://r.jina.ai/{url}"
    try:
        response = requests.get(jina_url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching content: {str(e)}")
        return ""

def count_word(text: str, word: str) -> int:
    """Count occurrences of a word in text (case-insensitive)"""
    # Use regex to find word boundaries
    pattern = r'\b' + re.escape(word) + r'\b'
    matches = re.findall(pattern, text, re.IGNORECASE)
    return len(matches)

if __name__ == "__main__":
    url = "https://datatalks.club/"
    print(f"Fetching content from {url}...")
    
    content = get_jina_content(url)
    
    if content:
        # Count occurrences of "data"
        count = count_word(content, "data")
        print(f"\nTotal characters: {len(content)}")
        print(f"Occurrences of 'data': {count}")
    else:
        print("Failed to fetch content")
