#!/usr/bin/env python3
"""
Render to SVG via Kroki — end-to-end pipeline.

This script demonstrates the full pipeline from .canvas to rendered SVG:
  1. Parse a .canvas file
  2. Convert to D2 syntax
  3. Render to SVG via the public Kroki API
  4. Save the output to disk

Run:
    python examples/03_render_with_kroki.py

Output:
    examples/output.svg
"""

from canvas_parser import parse_canvas, render_diagram, to_d2

# ── 1. Parse ───────────────────────────────────────────────────────────────
canvas = parse_canvas("examples/webapp_architecture.canvas")

# ── 2. Convert to D2 ──────────────────────────────────────────────────────
d2_str = to_d2(canvas, direction="down")

print("Generated D2 syntax:")
print(d2_str)
print()

# ── 3. Render via Kroki ───────────────────────────────────────────────────
print("Sending to Kroki API...")
try:
    svg_bytes = render_diagram(d2_str, diagram_type="d2", output_format="svg")

    # ── 4. Save to disk ───────────────────────────────────────────────────
    output_path = "examples/output.svg"
    with open(output_path, "wb") as f:
        f.write(svg_bytes)

    print(f"✓ Rendered SVG saved to {output_path} ({len(svg_bytes):,} bytes)")

except RuntimeError as e:
    print(f"✗ Kroki rendering failed: {e}")
    print("  (This is expected if you're offline or behind a firewall.)")
