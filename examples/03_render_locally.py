#!/usr/bin/env python3
"""
Render diagrams locally — no data leaves the machine.

This script demonstrates the two local rendering backends:
  1. Mermaid — client-side HTML via mermaid.js CDN
  2. D2 — local binary via d2-python-wrapper

Run:
    python examples/03_render_locally.py

Output:
    examples/output_mermaid.html
    examples/output_d2.svg  (requires `uv add "canvas-parser[local]"`)
"""

from canvas_parser import parse_canvas, render_mermaid_html, to_d2, to_mermaid

# ── 1. Parse ───────────────────────────────────────────────────────────────
canvas = parse_canvas("examples/webapp_architecture.canvas")

# ── 2. Mermaid — client-side HTML ────────────────────────────────────────
mermaid_str = to_mermaid(canvas, direction="LR")
html_str = render_mermaid_html(mermaid_str)

output_path = "examples/output_mermaid.html"
with open(output_path, "w") as f:
    f.write(html_str)
print(f"Mermaid HTML saved to {output_path}")

# ── 3. D2 — local binary ────────────────────────────────────────────────
d2_str = to_d2(canvas, direction="down")

print("\nGenerated D2 syntax:")
print(d2_str)

try:
    from canvas_parser import render_d2_local

    svg_bytes = render_d2_local(d2_str, output_format="svg")

    output_path = "examples/output_d2.svg"
    with open(output_path, "wb") as f:
        f.write(svg_bytes)
    print(f"\nD2 SVG saved to {output_path} ({len(svg_bytes):,} bytes)")

except ImportError:
    print("\nSkipping D2 local render (d2-python-wrapper not installed).")
    print("  Install with: uv add 'canvas-parser[local]'")
