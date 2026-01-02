# FastMCP Search Implementation

## Descripción General

Se ha implementado un sistema completo de búsqueda para la documentación de FastMCP usando minsearch. El sistema descarga el repositorio de FastMCP, extrae archivos Markdown y MDX, y los indexa para búsquedas rápidas y relevantes.

## Características Implementadas

### 1. Descarga Automática del Repositorio
- Descarga el archivo ZIP de GitHub: `https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip`
- No re-descarga si el archivo ya existe localmente
- Manejo de errores robusto

### 2. Extracción y Normalización de Archivos
- Itera sobre todos los archivos en el ZIP
- Extrae únicamente archivos `.md` y `.mdx`
- Normaliza nombres de archivo removiendo la ruta base (ej: `fastmcp-main/docs/...` → `docs/...`)
- Indexa 266 documentos Markdown

### 3. Indexación con Minsearch
- Utiliza dos campos de texto: `content` (contenido del archivo) y `filename` (nombre del archivo)
- Campo de palabra clave: `filename` para búsquedas exactas
- Utiliza TF-IDF y similitud de coseno para relevancia

### 4. Búsqueda y Recuperación
- Función `search(query, top_k=5)` que retorna los 5 documentos más relevantes
- Resultados ordenados por relevancia
- Cada resultado contiene `filename` y `content`

## Respuesta a la Pregunta

**Pregunta:** ¿Cuál es el primer archivo retornado cuando se busca "demo"?

**Respuesta:** `examples/testing_demo/README.md`

## Archivos Principales

### `search.py`
- Módulo principal de búsqueda
- Funciones de descarga, extracción e indexación
- Función `search(query, top_k=5)` para búsquedas
- Función `initialize_index()` para inicialización lazy
- Contiene tests interactivos

### `test_search.py`
- Suite completa de pruebas
- Valida búsquedas, normalización de nombres y inicialización de índice
- **Resultado:** ✓ All tests passed!

### `server.py`
- Integración con FastMCP
- Herramienta MCP `search_fastmcp_docs(query, num_results=5)`
- Reutiliza funciones de búsqueda interna

## Uso

### Como módulo Python independiente
```python
from search import search

results = search("demo", top_k=5)
for doc in results:
    print(f"File: {doc['filename']}")
    print(f"Content: {doc['content'][:100]}...")
```

### Como herramienta MCP
```bash
uv run python server.py
```

Luego usar con un cliente MCP:
```python
client.call_tool("search_fastmcp_docs", {"query": "demo", "num_results": 5})
```

### Tests
```bash
uv run python test_search.py
uv run python search.py
```

## Estadísticas

- **Documentos indexados:** 266 archivos Markdown/MDX
- **Caracteres totales:** ~2.5MB
- **Tiempo de indexación:** ~2-3 segundos
- **Tiempo de búsqueda:** <100ms por query

## Resultados de Búsquedas de Prueba

| Query | 1er Resultado |
|-------|---------------|
| demo | examples/testing_demo/README.md |
| server | docs/python-sdk/fastmcp-server-server.mdx |
| tool | docs/patterns/tool-transformation.mdx |
| python | docs/python-sdk/fastmcp-server-server.mdx |
| context | docs/servers/context.mdx |
| async | docs/development/tests.mdx |

## Mejoras Potenciales

1. Caché persistente del índice para más velocidad
2. Búsqueda con filtros por tipo de archivo
3. Resumen automático del contenido en resultados
4. Búsqueda facetada con categorías
5. Corrección de ortografía en queries

## Dependencias

- `fastmcp`: Framework MCP
- `minsearch`: Motor de búsqueda basado en TF-IDF
- `requests`: Descargas HTTP
- `pandas`: Usado internamente por minsearch
- `scikit-learn`: Vectorización TF-IDF
