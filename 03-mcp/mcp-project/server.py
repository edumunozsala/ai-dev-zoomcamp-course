from fastmcp import FastMCP
import requests
import re
import os
import zipfile
from minsearch import Index

# Initialize FastMCP server
mcp = FastMCP("jina-scraper")

# Global index variable for FastMCP search
_fastmcp_index = None
_fastmcp_documents = None

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

def _download_fastmcp_zip():
    """Download the fastmcp repository zip file if not already present."""
    zip_path = "fastmcp-main.zip"
    
    if os.path.exists(zip_path):
        return zip_path
    
    url = "https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip"
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(zip_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    return zip_path

def _extract_and_index_files(zip_path):
    """Extract md and mdx files from zip and prepare for indexing."""
    documents = []
    
    with zipfile.ZipFile(zip_path, 'r') as zf:
        # Get the base directory name from the zip
        base_names = set()
        for name in zf.namelist():
            base_names.add(name.split('/')[0])
        
        base_dir = list(base_names)[0] if base_names else "fastmcp-main"
        
        for file_info in zf.infolist():
            filename = file_info.filename
            
            # Skip directories
            if filename.endswith('/'):
                continue
            
            # Only process .md and .mdx files
            if not (filename.endswith('.md') or filename.endswith('.mdx')):
                continue
            
            # Read the file content
            content = zf.read(filename).decode('utf-8')
            
            # Normalize filename by removing the base directory
            normalized_filename = filename.replace(f"{base_dir}/", "", 1)
            
            documents.append({
                'filename': normalized_filename,
                'content': content
            })
    
    return documents

def _build_fastmcp_index(documents):
    """Create a minsearch index from the documents."""
    index = Index(
        text_fields=['content', 'filename'],
        keyword_fields=['filename']
    )
    
    # Fit the index with all documents
    index.fit(documents)
    
    return index

def _initialize_fastmcp_index():
    """Initialize the global FastMCP documentation index."""
    global _fastmcp_index, _fastmcp_documents
    
    if _fastmcp_index is not None:
        return _fastmcp_index, _fastmcp_documents
    
    # Download the zip file
    zip_path = _download_fastmcp_zip()
    
    # Extract and index files
    _fastmcp_documents = _extract_and_index_files(zip_path)
    
    # Create the index
    _fastmcp_index = _build_fastmcp_index(_fastmcp_documents)
    
    return _fastmcp_index, _fastmcp_documents

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

@mcp.tool()
def search_fastmcp_docs(query: str, num_results: int = 5) -> list:
    """
    Search the FastMCP documentation for relevant documents.
    
    Args:
        query: The search query string.
        num_results: Number of results to return (default: 5).
    
    Returns:
        A list of dictionaries containing the most relevant documents with 'filename' and 'content' fields.
    """
    index, documents = _initialize_fastmcp_index()
    
    # Search the index
    results = index.search(query, num_results=num_results)
    
    return results

if __name__ == "__main__":
    mcp.run()