#!/usr/bin/env python
"""Script to count occurrences of 'data' on https://datatalks.club/ - detailed analysis"""

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

if __name__ == "__main__":
    url = "https://datatalks.club/"
    print(f"Fetching content from {url}...")
    
    content = get_jina_content(url)
    
    if content:
        print(f"\nTotal characters: {len(content)}\n")
        
        # Count with word boundaries (case-insensitive)
        pattern = r'\bdata\b'
        matches = re.findall(pattern, content, re.IGNORECASE)
        print(f"Occurrences of 'data' (word boundaries, case-insensitive): {len(matches)}")
        
        # Count simple substring (case-insensitive)
        count = content.lower().count("data")
        print(f"Occurrences of 'data' (substring, case-insensitive): {count}")
        
        # Show first 2000 characters
        print(f"\nFirst 2000 characters of content:\n")
        print(content[:2000])
    else:
        print("Failed to fetch content")
