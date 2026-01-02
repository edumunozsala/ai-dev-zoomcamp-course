#!/usr/bin/env python
"""
Search functionality for indexed FastMCP documentation.
Retrieves 5 most relevant documents from the index.
"""

import os
import zipfile
from pathlib import Path
from minsearch import Index
import requests

# Global index variable
_index = None
_documents = None

def download_fastmcp_zip():
    """Download the fastmcp repository zip file if not already present."""
    zip_path = "fastmcp-main.zip"
    
    if os.path.exists(zip_path):
        print(f"✓ {zip_path} already exists")
        return zip_path
    
    url = "https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip"
    print(f"Downloading {url}...")
    
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(zip_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print(f"✓ Downloaded to {zip_path}")
    return zip_path

def extract_and_index_files(zip_path):
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

def build_index(documents):
    """Create a minsearch index from the documents."""
    # Initialize the index
    index = Index(
        text_fields=['content', 'filename'],
        keyword_fields=['filename']
    )
    
    # Fit the index with all documents
    index.fit(documents)
    
    return index

def initialize_index():
    """Initialize the global index."""
    global _index, _documents
    
    if _index is not None:
        return _index, _documents
    
    print("Initializing index...")
    
    # Download the zip file
    zip_path = download_fastmcp_zip()
    
    # Extract and index files
    print("Extracting and indexing md/mdx files...")
    _documents = extract_and_index_files(zip_path)
    
    print(f"✓ Indexed {len(_documents)} markdown files")
    
    # Create the index
    _index = build_index(_documents)
    
    return _index, _documents

def search(query: str, top_k: int = 5):
    """
    Search the index for documents matching the query.
    
    Args:
        query: The search query string
        top_k: Number of results to return (default: 5)
    
    Returns:
        List of dictionaries with 'filename' and 'content' fields
    """
    index, documents = initialize_index()
    
    # Search the index
    results = index.search(query, num_results=top_k)
    
    return results

def test_search():
    """Test the search functionality with various queries."""
    print("=" * 60)
    print("FastMCP Documentation Search - Test")
    print("=" * 60)
    
    # Test query: "demo"
    test_query = "demo"
    print(f"\nSearching for: '{test_query}'")
    print("-" * 60)
    
    results = search(test_query, top_k=5)
    
    if results:
        print(f"\nFound {len(results)} result(s):\n")
        for i, doc in enumerate(results, 1):
            print(f"{i}. {doc['filename']}")
            print(f"   Content preview: {doc['content'][:100]}...")
            print()
    else:
        print("No results found.")
    
    # Additional test queries
    test_queries = ["server", "tool", "python"]
    
    print("-" * 60)
    print("\nAdditional searches:")
    print("-" * 60)
    
    for query in test_queries:
        results = search(query, top_k=1)
        if results:
            print(f"'{query}' -> {results[0]['filename']}")
        else:
            print(f"'{query}' -> No results")

if __name__ == "__main__":
    test_search()
