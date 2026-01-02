import sys
import os
import re

# Add parent directory to path to import server
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import get_jina_content

def test_jina_scraper():
    """Test fetching content from GitHub URL"""
    test_url = "https://github.com/alexeygrigorev/minsearch"
    print(f"Testing jina scraper with URL: {test_url}")
    
    content = get_jina_content(test_url)
    
    if content and "minsearch" in content:
        print("✓ SUCCESS: Content fetched successfully and contains expected text.")
        print("-" * 50)
        print("Snippet of content:")
        print(content[:200])
        print("-" * 50)
        print(f"Content length: {len(content)} characters")
    else:
        print("✗ FAILURE: Could not fetch content or content did not match expectation.")
        print(f"Content received: {content[:100]}...")

def test_count_word():
    """Test counting words on a webpage"""
    test_url = "https://datatalks.club/"
    test_word = "data"
    
    print(f"\n\nTesting word counting on: {test_url}")
    print(f"Searching for word: '{test_word}'")
    
    content = get_jina_content(test_url)
    
    if content and not content.startswith("Error"):
        # Count with word boundaries (case-insensitive)
        pattern = r'\b' + re.escape(test_word) + r'\b'
        word_boundary_count = len(re.findall(pattern, content, re.IGNORECASE))
        
        # Count simple substring (case-insensitive)
        substring_count = content.lower().count(test_word.lower())
        
        print("-" * 50)
        print(f"Total characters: {len(content)}")
        print(f"Occurrences of '{test_word}' (word boundaries): {word_boundary_count}")
        print(f"Occurrences of '{test_word}' (substring): {substring_count}")
        print("-" * 50)
        print(f"✓ Content successfully analyzed")
    else:
        print(f"✗ Failed to fetch content: {content}")

if __name__ == "__main__":
    test_jina_scraper()
    test_count_word()