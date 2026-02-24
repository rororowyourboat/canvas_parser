#!/usr/bin/env python3
"""
Batch conversion — process all .canvas files in a directory.

This script demonstrates automation-friendly batch processing:
  1. Scan a directory for .canvas files
  2. Parse and convert each one to both Mermaid and D2
  3. Write the output syntax files next to each canvas

This pattern is ideal for CI/CD pipelines, documentation generators,
or static site builds.

Run:
    python examples/04_batch_processing.py <directory>

Example:
    python examples/04_batch_processing.py examples/
"""

import sys
from pathlib import Path

from canvas_parser import parse_canvas, to_d2, to_mermaid


def process_directory(directory: str) -> None:
    """Find all .canvas files in a directory and convert them."""
    canvas_dir = Path(directory)
    canvas_files = sorted(canvas_dir.glob("**/*.canvas"))

    if not canvas_files:
        print(f"No .canvas files found in {directory}")
        return

    print(f"Found {len(canvas_files)} canvas file(s) in {directory}\n")

    for canvas_path in canvas_files:
        print(f"  Processing: {canvas_path}")

        canvas = parse_canvas(str(canvas_path))

        # Write Mermaid output
        mermaid_path = canvas_path.with_suffix(".mermaid.md")
        mermaid_str = to_mermaid(canvas, direction="LR")
        mermaid_path.write_text(f"```mermaid\n{mermaid_str}\n```\n")
        print(f"    → {mermaid_path.name}  ({len(canvas.nodes)} nodes, {len(canvas.edges)} edges)")

        # Write D2 output
        d2_path = canvas_path.with_suffix(".d2")
        d2_str = to_d2(canvas, direction="down")
        d2_path.write_text(d2_str + "\n")
        print(f"    → {d2_path.name}")

    print(f"\n✓ Done! Converted {len(canvas_files)} file(s).")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "examples/"
    process_directory(target)
