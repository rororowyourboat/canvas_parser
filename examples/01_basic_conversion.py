#!/usr/bin/env python3
"""
Basic Usage — Parse a .canvas file and convert to Mermaid + D2.

This script demonstrates the core workflow:
  1. Parse a .canvas file into typed Python objects
  2. Inspect the parsed data
  3. Convert to Mermaid.js syntax
  4. Convert to D2 syntax

Run:
    python examples/01_basic_conversion.py
"""

from canvas_parser import Canvas, Node, parse_canvas, to_d2, to_mermaid

# ── 1. Parse ───────────────────────────────────────────────────────────────
canvas: Canvas = parse_canvas("examples/webapp_architecture.canvas")

print("=" * 60)
print("PARSED CANVAS")
print("=" * 60)
print(f"  Nodes: {len(canvas.nodes)}")
print(f"  Edges: {len(canvas.edges)}")
print()

node: Node
for node in canvas.nodes:
    label = (
        getattr(node, "text", None)
        or getattr(node, "label", None)
        or getattr(node, "file", None)
        or getattr(node, "url", None)
        or "(no label)"
    )
    print(f"  [{node.type:5s}] {node.id}  →  {label}")

print()
for edge in canvas.edges:
    label = f'  "{edge.label}"' if edge.label else ""
    print(f"  {edge.fromNode} → {edge.toNode}{label}")


# ── 2. Convert to Mermaid ─────────────────────────────────────────────────
mermaid_str = to_mermaid(canvas, direction="TB")

print()
print("=" * 60)
print("MERMAID OUTPUT")
print("=" * 60)
print(mermaid_str)


# ── 3. Convert to D2 ──────────────────────────────────────────────────────
d2_str = to_d2(canvas, direction="down")

print()
print("=" * 60)
print("D2 OUTPUT")
print("=" * 60)
print(d2_str)
