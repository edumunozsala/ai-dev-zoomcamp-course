from fastmcp import FastMCP
import requests
import re

# Initialize FastMCP server
mcp = FastMCP("jina-scraper")

def get_jina_content(url: str) -> str:
    """
    Helper function to fetch content using r.jina.ai.
    This is separated to be easily importable for testing if needed,
    though testing the tool endpoint is also valid.
    """
    jina_url = f"https://r.jina.ai/{url}"
    try:
        response = requests.get(jina_url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return f"Error fetching content: {str(e)}"

@mcp.tool()
def read_url(url: str) -> str:
    """
    Download the content of a web page using r.jina.ai.
    
    Args:
        url: The URL of the web page to download.
    """
    return get_jina_content(url)

@mcp.tool()
def count_word_in_url(url: str, word: str) -> dict:
    """
    Count occurrences of a word on a web page using r.jina.ai.
    
    Args:
        url: The URL of the web page to search.
        word: The word to count (case-insensitive).
    
    Returns:
        A dictionary with the count, character count, and some context.
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
        "recommendation": f"Use substring count ({substring_count}) for general searches"
    }

if __name__ == "__main__":
    mcp.run()