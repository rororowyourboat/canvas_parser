"""
canvas_parser — Lightweight bridge between Obsidian JSON Canvas and declarative diagrams.

This package reads ``.canvas`` files (the open `JSON Canvas <https://jsoncanvas.org/>`_
specification) and converts them into declarative diagram syntax that rendering
engines like `Kroki <https://kroki.io/>`_ understand.

Quick start::

    from canvas_parser import (
        parse_canvas, to_mermaid, to_d2,
        render_diagram, render_mermaid_html, render_d2_local,
    )

    canvas = parse_canvas("my_notes.canvas")

    # Convert to Mermaid or D2
    mermaid_str = to_mermaid(canvas, direction="LR")
    d2_str      = to_d2(canvas, direction="right")

    # Render to SVG via Kroki
    svg_bytes = render_diagram(d2_str, diagram_type="d2", output_format="svg")

Supported output formats:

- **Mermaid.js** — flowchart with subgraphs, via :func:`to_mermaid`
- **D2** — declarative diagrams with nested containers, via :func:`to_d2`

The library is **zero-dependency** (stdlib only) and designed to be embedded in
CI pipelines, static-site generators, or any Python automation.
"""

from .d2 import to_d2
from .kroki import encode_kroki_diagram, render_d2_local, render_diagram, render_mermaid_html
from .mermaid import to_mermaid
from .models import Canvas, Edge, FileNode, GroupNode, LinkNode, Node, TextNode
from .parser import loads, parse_canvas

__all__ = [
    "Canvas",
    "Node",
    "TextNode",
    "FileNode",
    "LinkNode",
    "GroupNode",
    "Edge",
    "parse_canvas",
    "loads",
    "to_mermaid",
    "to_d2",
    "render_diagram",
    "render_mermaid_html",
    "render_d2_local",
    "encode_kroki_diagram",
]
