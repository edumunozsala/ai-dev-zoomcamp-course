#!/usr/bin/env python
"""
Comprehensive tests for the FastMCP search functionality.
"""

import sys
from search import search, initialize_index

def test_search_demo():
    """Test searching for 'demo' query."""
    print("Test 1: Search for 'demo'")
    print("-" * 60)
    
    results = search("demo", top_k=5)
    
    assert len(results) > 0, "Search should return at least one result"
    
    # Check that the first result is the expected file
    first_result = results[0]['filename']
    assert first_result == "examples/testing_demo/README.md", f"Expected examples/testing_demo/README.md but got {first_result}"
    
    print(f"✓ Found {len(results)} results")
    print(f"✓ First result: {first_result}")
    print()

def test_search_server():
    """Test searching for 'server' query."""
    print("Test 2: Search for 'server'")
    print("-" * 60)
    
    results = search("server", top_k=3)
    
    assert len(results) > 0, "Search should return at least one result"
    
    print(f"✓ Found {len(results)} results:")
    for i, doc in enumerate(results, 1):
        print(f"  {i}. {doc['filename']}")
    print()

def test_search_multiple_queries():
    """Test searching with multiple queries."""
    print("Test 3: Multiple search queries")
    print("-" * 60)
    
    queries = ["python", "tool", "context", "async"]
    
    for query in queries:
        results = search(query, top_k=1)
        if results:
            print(f"✓ '{query}' -> {results[0]['filename']}")
        else:
            print(f"✗ '{query}' -> No results")
    print()

def test_index_initialization():
    """Test that index is properly initialized."""
    print("Test 4: Index initialization")
    print("-" * 60)
    
    index, documents = initialize_index()
    
    assert index is not None, "Index should be initialized"
    assert documents is not None, "Documents should be loaded"
    assert len(documents) > 0, "Should have indexed documents"
    
    print(f"✓ Index initialized with {len(documents)} documents")
    print()

def test_filename_normalization():
    """Test that filenames are normalized correctly."""
    print("Test 5: Filename normalization")
    print("-" * 60)
    
    index, documents = initialize_index()
    
    # Check that no filenames contain "fastmcp-main/"
    for doc in documents:
        filename = doc['filename']
        assert not filename.startswith("fastmcp-main/"), f"Filename should not contain base directory: {filename}"
    
    print(f"✓ All {len(documents)} filenames are properly normalized")
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("FastMCP Search - Comprehensive Tests")
    print("=" * 60)
    print()
    
    try:
        test_search_demo()
        test_search_server()
        test_search_multiple_queries()
        test_index_initialization()
        test_filename_normalization()
        
        print("=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
