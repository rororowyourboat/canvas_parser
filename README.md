# Canvas Parser

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/v3.10.0/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/rororowyourboat/canvas_parser/actions/workflows/ci.yml/badge.svg)](https://github.com/rororowyourboat/canvas_parser/actions/workflows/ci.yml)

A Python utility that bridges the gap between **Obsidian JSON Canvas** (`.canvas`) and powerful declarative diagramming languages like **Mermaid.js** and **D2**, with fully local rendering that keeps your data private.

## Goals & Architectural Approach

While incredible tools like `Canvas2Document` exist for parsing Canvas data, they are built natively into Obsidian's TypeScript plugin ecosystem. Our goal was to build a **standalone, automation-first Python library**.

### Why build this?

The `jsoncanvas` specification defines the spatial layout of an infinite canvas (x, y, width, height) but lacks native export to structured diagram syntax. This library reads a `.canvas` file, computes the bounding boxes of grouping nodes, and safely translates strings, edges, and nested relationships into valid declarative syntax.

By keeping this utility in Python and dependency-free, it becomes highly **complementary**:

1. **Automation & CI/CD**: You can run this parser across thousands of `.canvas` files in a batch process, or trigger it in GitHub Actions to automatically update team documentation.
2. **Static Site Integration**: Easily embed this parser into documentation generators like Sphinx, MkDocs, or Jekyll.
3. **Privacy First**: All rendering happens locally — no diagram data ever leaves your machine.

## Privacy & Data Handling

canvas\_parser is designed so that **your diagram data never leaves your machine**. Every step of the pipeline — parsing, syntax conversion, and rendering — runs locally.

- **Parsing & conversion** are pure Python with zero dependencies. Your `.canvas` files are read from disk, transformed in memory, and never transmitted anywhere.
- **Mermaid rendering** produces a self-contained HTML file. The diagram source is embedded directly in the HTML. The only network request is loading the mermaid.js library from a CDN — your diagram content is never sent over the wire.
- **D2 rendering** invokes the `d2` binary on your machine via `d2-python-wrapper`. The entire render happens in a local temp directory with no network access.
- **No telemetry, no analytics, no external API calls.** The library makes no outbound connections with your data, ever.

This makes canvas\_parser safe for proprietary diagrams, internal architecture docs, and any environment where data exfiltration is a concern.

## Features

- **Parse JSON Canvas**: Extracts `TextNode`, `FileNode`, `LinkNode`, `GroupNode`, and standard `Edge` representations.
- **Export to Mermaid**: Converts elements to Mermaid flowcharts with subgraphs.
- **Export to D2**: Converts elements into modern D2 (`x -> y`) declarative syntax with implicit formatting.
- **Render locally**: Mermaid diagrams render client-side via mermaid.js (zero dependencies), D2 diagrams render locally via `d2-python-wrapper`. No diagram data leaves the machine.

## Installation

Requires `python 3.10+`. Currently, you can install the package using `uv`:

```bash
uv pip install -e .
```

## Quick Start

```python
from canvas_parser import parse_canvas, to_mermaid, to_d2, render_mermaid_html

# 1. Parse your .canvas file
canvas = parse_canvas("sample.canvas")

# 2. Convert to targeted syntax
mermaid_str = to_mermaid(canvas, "LR")
d2_str = to_d2(canvas, "down")

# 3. Render Mermaid client-side (no data leaves the machine)
html = render_mermaid_html(mermaid_str)
with open("diagram.html", "w") as f:
    f.write(html)
```

## Rendering Options

canvas\_parser supports two local rendering backends. No diagram data ever leaves your machine.

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

## Setup Best Practices & Open Source Acknowledgements

This project is open-source and benefits from the community!

### Best Practices for Contribution

If you plan to fork or contribute:

1. **Tests**: Verify your changes against `pytest`. We maintain 100% test coverage for syntax generation.
2. **Environment**: We use `uv` for lightning-fast dependency resolution (`uv run pytest`).
3. **Data Models**: Use Python `dataclasses` (with `kw_only=True`) inside `models.py` when expanding canvas nodes.

### Credits

- **Spatial Traversal Logic**: The bounding-box collision logic for subgroups (`GroupNode`) was heavily inspired by the incredible Obsidian plugin **[Canvas2Document](https://github.com/slnsys/canvas2document)** by `@slnsys`.
