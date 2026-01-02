#!/usr/bin/env python
"""
Download fastmcp repository and index md/mdx files with minsearch.
"""

import os
import zipfile
import requests
from pathlib import Path
import shutil

def download_fastmcp_zip():
    """Download the fastmcp repository zip file if not already present."""
    zip_path = "fastmcp-main.zip"
    
    if os.path.exists(zip_path):
        print(f"✓ {zip_path} already exists, skipping download")
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
            
            print(f"  - Indexed: {normalized_filename}")
    
    return documents

def create_index(documents):
    """Create a minsearch index from the documents."""
    from minsearch import Index
    
    # Initialize the index
    index = Index(
        text_fields=['content', 'filename'],
        keyword_fields=['filename']
    )
    
    # Add all documents
    for i, doc in enumerate(documents):
        index.index(doc)
    
    return index

if __name__ == "__main__":
    print("=" * 60)
    print("FastMCP Repository Indexing")
    print("=" * 60)
    
    # Download the zip file
    zip_path = download_fastmcp_zip()
    
    # Extract and index files
    print(f"\nExtracting md/mdx files from {zip_path}...")
    documents = extract_and_index_files(zip_path)
    
    print(f"\n✓ Found and indexed {len(documents)} markdown files")
    
    # Create the index
    print("\nCreating minsearch index...")
    index = create_index(documents)
    
    print("✓ Index created successfully")
    print("=" * 60)
