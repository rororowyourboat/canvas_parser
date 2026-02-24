# Examples

Runnable scripts demonstrating the core capabilities of `canvas_parser`.

## Setup

```bash
# From the project root
uv pip install -e .
```

## Scripts

| Script | Description |
|---|---|
| [`01_basic_conversion.py`](01_basic_conversion.py) | Parse a `.canvas` file and convert to both Mermaid and D2 syntax. Shows how to inspect the parsed data model. |
| [`02_parse_from_string.py`](02_parse_from_string.py) | Build a canvas programmatically as a Python dict, serialize to JSON, and parse with `loads()`. |
| [`03_render_with_kroki.py`](03_render_with_kroki.py) | Full pipeline: `.canvas` → D2 → SVG via the public Kroki API. Saves the output to `output.svg`. |
| [`04_batch_processing.py`](04_batch_processing.py) | Scan a directory for `.canvas` files and batch-convert each to Mermaid markdown + D2 files. Ideal for CI/CD. |

## Sample Data

| File | Description |
|---|---|
| [`webapp_architecture.canvas`](webapp_architecture.canvas) | A realistic web app architecture with frontend/backend groups, database, Redis cache, and docs link. |

## Running

```bash
# Basic conversion (parse + inspect + convert)
python examples/01_basic_conversion.py

# Parse from in-memory JSON string
python examples/02_parse_from_string.py

# Render SVG via Kroki (requires internet)
python examples/03_render_with_kroki.py

# Batch convert all .canvas files in a directory
python examples/04_batch_processing.py examples/
```
