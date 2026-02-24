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
- **Render with Kroki**: Generates ready-to-use PNG/SVG bytes directly utilizing the public [Kroki API](https://kroki.io/) without any local binaries.

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
