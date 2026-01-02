#!/usr/bin/env python
"""
Demostración completa del sistema de búsqueda FastMCP.
Ejecuta todas las pruebas y muestra los resultados.
"""

import sys
from search import search, initialize_index

def main():
    print("=" * 70)
    print("DEMOSTRACIÓN DEL SISTEMA DE BÚSQUEDA FASTMCP")
    print("=" * 70)
    print()
    
    # Inicializar el índice
    print("1. Inicializando índice...")
    index, documents = initialize_index()
    print(f"   ✓ {len(documents)} documentos indexados")
    print()
    
    # Búsqueda por "demo"
    print("2. Búsqueda: 'demo'")
    print("   " + "-" * 60)
    results = search("demo", top_k=3)
    for i, doc in enumerate(results, 1):
        preview = doc['content'][:80].replace('\n', ' ')
        print(f"   {i}. {doc['filename']}")
        print(f"      {preview}...")
    print()
    
    # Respuesta a Question 5
    print("3. RESPUESTA A QUESTION 5")
    print("   " + "-" * 60)
    first_result = results[0]['filename']
    print(f"   Primer archivo para 'demo': {first_result}")
    print()
    
    # Validar opciones
    options = [
        "README.md",
        "docs/servers/context.mdx",
        "examples/testing_demo/README.md",
        "docs/python-sdk/fastmcp-settings.mdx"
    ]
    
    print("   Opciones disponibles:")
    for i, opt in enumerate(options, 1):
        marker = " ✓" if first_result == opt else ""
        print(f"   {i}. {opt}{marker}")
    print()
    
    # Búsquedas adicionales
    print("4. Búsquedas adicionales")
    print("   " + "-" * 60)
    additional_queries = ["server", "python", "testing"]
    for query in additional_queries:
        results = search(query, top_k=1)
        if results:
            print(f"   '{query}' → {results[0]['filename']}")
    print()
    
    print("=" * 70)
    print("DEMOSTRACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
