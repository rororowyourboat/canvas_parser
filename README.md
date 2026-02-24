# Canvas Parser

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/v3.10.0/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/rororowyourboat/canvas_parser/actions/workflows/ci.yml/badge.svg)](https://github.com/rororowyourboat/canvas_parser/actions/workflows/ci.yml)

A Python utility that bridges the gap between **Obsidian JSON Canvas** (`.canvas`) and powerful declarative diagramming languages like **Mermaid.js** and **D2**, seamlessly rendered via **Kroki.io**.

## Goals & Architectural Approach

While incredible tools like `Canvas2Document` exist for parsing Canvas data, they are built natively into Obsidian's TypeScript plugin ecosystem. Our goal was to build a **standalone, automation-first Python library**.

### Why build this?

The `jsoncanvas` specification defines the spatial layout of an infinite canvas (x, y, width, height) but lacks native export to structured diagram syntax. This library reads a `.canvas` file, computes the bounding boxes of grouping nodes, and safely translates strings, edges, and nested relationships into valid declarative syntax.

By keeping this utility in Python and dependency-free, it becomes highly **complementary**:

1. **Automation & CI/CD**: You can run this parser across thousands of `.canvas` files in a batch process, or trigger it in GitHub Actions to automatically update team documentation.
2. **Static Site Integration**: Easily embed this parser into documentation generators like Sphinx, MkDocs, or Jekyll.
3. **The Kroki Bridge**: We aren't reinventing the drawing engine; we are feeding it! Our parser bridges the gap between Obsidian's raw JSON and the declarative formats (Mermaid, D2) that powerful rendering engines like [Kroki.io](https://kroki.io/) expect.

## Features

- **Parse JSON Canvas**: Extracts `TextNode`, `FileNode`, `LinkNode`, `GroupNode`, and standard `Edge` representations.
- **Export to Mermaid**: Converts elements to Mermaid flowcharts with subgraphs.
- **Export to D2**: Converts elements into modern D2 (`x -> y`) declarative syntax with implicit formatting.
- **Render locally or via Kroki**: Mermaid diagrams render client-side via mermaid.js (zero dependencies), D2 diagrams render locally via `d2-python-wrapper`, and [Kroki](https://kroki.io/) is available as an optional server-side fallback for both formats.

## Installation

Requires `python 3.10+`. Currently, you can install the package using `uv`:

```bash
uv pip install -e .
```

## Quick Start

```python
from canvas_parser import parse_canvas, to_mermaid, to_d2, render_diagram

# 1. Parse your .canvas file
canvas = parse_canvas("sample.canvas")

# 2. Convert to targeted syntax
mermaid_str = to_mermaid(canvas, "LR")
d2_str = to_d2(canvas, "down")

# 3. Retrieve rendered image instantly via Kroki
svg_bytes = render_diagram(d2_str, diagram_type="d2", output_format="svg")
with open("my_diagram.svg", "wb") as f:
    f.write(svg_bytes)
```

## Rendering Options

canvas\_parser supports three rendering backends. Choose the one that fits your privacy and dependency needs:

### 1. Mermaid — Client-Side (Recommended)

Renders Mermaid diagrams in the browser via mermaid.js CDN. **No diagram data leaves the machine** — only the CDN script URL hits the network. Zero Python dependencies.

```python
from canvas_parser import to_mermaid, render_mermaid_html, parse_canvas

canvas = parse_canvas("sample.canvas")
html_str = render_mermaid_html(to_mermaid(canvas, "LR"))

# Write to a file and open in a browser
with open("diagram.html", "w") as f:
    f.write(html_str)

# Or use in a marimo notebook
import marimo as mo
mo.iframe(html_str)
```

### 2. D2 — Local Binary

Renders D2 diagrams locally using the `d2` binary (bundled via `d2-python-wrapper`). No network access required.

```bash
uv add "canvas-parser[local]"
```

```python
from canvas_parser import to_d2, render_d2_local, parse_canvas

canvas = parse_canvas("sample.canvas")
svg_bytes = render_d2_local(to_d2(canvas), output_format="svg")

with open("diagram.svg", "wb") as f:
    f.write(svg_bytes)
```

### 3. Kroki — Server-Side Fallback

Sends diagram source to a [Kroki](https://kroki.io/) instance (public or self-hosted) for rendering. Supports both Mermaid and D2.

```python
from canvas_parser import to_d2, render_diagram, parse_canvas

canvas = parse_canvas("sample.canvas")
svg_bytes = render_diagram(to_d2(canvas), diagram_type="d2", output_format="svg")
```

For private diagrams, self-host Kroki instead of using the public instance:

```bash
docker run -d -p 8000:8000 yuzutech/kroki
```

```python
svg_bytes = render_diagram(
    d2_str,
    diagram_type="d2",
    output_format="svg",
    base_url="http://localhost:8000",
)
```

## Setup Best Practices & Open Source Acknowledgements

This project is open-source and benefits from the community!

### Best Practices for Contribution

If you plan to fork or contribute:

1. **Tests**: Verify your changes against `pytest`. We maintain 100% test coverage for syntax generation.
2. **Environment**: We use `uv` for lightning-fast dependency resolution (`uv run pytest`).
3. **Data Models**: Use Python `dataclasses` (with `kw_only=True`) inside `models.py` when expanding canvas nodes.

### Credits

- **Spatial Traversal Logic**: The bounding-box collision logic for subgroups (`GroupNode`) was heavily inspired by the incredible Obsidian plugin **[Canvas2Document](https://github.com/slnsys/canvas2document)** by `@slnsys`.

- **Rendering Engine**: Image generation is securely and rapidly generated via **[Kroki](https://kroki.io/)**.
