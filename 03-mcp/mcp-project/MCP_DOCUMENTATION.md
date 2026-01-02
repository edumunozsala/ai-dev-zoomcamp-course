# MCP Jina Scraper - Documentación

## Descripción

Este proyecto implementa un servidor MCP (Model Context Protocol) que proporciona herramientas para descargar y analizar contenido de páginas web usando el servicio r.jina.ai.

## Herramientas Disponibles

### 1. `read_url(url: str) -> str`
Descarga el contenido completo de una página web en formato Markdown.

**Parámetros:**
- `url`: La URL de la página web a descargar

**Retorna:**
- El contenido de la página en formato Markdown

**Ejemplo:**
```python
content = read_url("https://datatalks.club/")
```

### 2. `count_word_in_url(url: str, word: str) -> dict`
Cuenta las ocurrencias de una palabra en una página web.

**Parámetros:**
- `url`: La URL de la página web a analizar
- `word`: La palabra a contar (case-insensitive)

**Retorna:**
- Un diccionario con:
  - `url`: La URL analizada
  - `word`: La palabra buscada
  - `total_characters`: Número total de caracteres
  - `count_word_boundaries`: Ocurrencias con límites de palabras
  - `count_substring`: Ocurrencias como substring

**Ejemplo:**
```python
result = count_word_in_url("https://datatalks.club/", "data")
# Retorna: {
#   "url": "https://datatalks.club/",
#   "word": "data",
#   "total_characters": 5679,
#   "count_word_boundaries": 10,
#   "count_substring": 61
# }
```

## Respuesta a la Pregunta

**Pregunta:** ¿Cuántas veces aparece la palabra "data" en https://datatalks.club/?

**Respuesta:** **61 ocurrencias** (contando como substring, case-insensitive)

## Archivos del Proyecto

- `server.py`: Servidor MCP con las herramientas implementadas
- `test/test.py`: Suite de pruebas para validar las herramientas
- `example_usage.py`: Ejemplo de uso de las herramientas
- `count_data.py`: Script específico para contar palabras en datatalks.club
- `count_data_detailed.py`: Análisis detallado con estadísticas

## Instalación y Uso

### Instalar dependencias
```bash
uv add requests fastmcp
```

### Ejecutar el servidor MCP
```bash
uv run python server.py
```

### Ejecutar pruebas
```bash
uv run python test/test.py
```

### Ejecutar ejemplo
```bash
uv run python example_usage.py
```

## Dependencias

- `fastmcp`: Framework para construir servidores MCP
- `requests`: Biblioteca para hacer solicitudes HTTP

Ver `pyproject.toml` para más detalles sobre las dependencias.
