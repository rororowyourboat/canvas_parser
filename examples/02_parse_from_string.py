#!/usr/bin/env python3
"""
Working with JSON strings — Parse canvas data from memory.

This script demonstrates using `loads()` to parse a JSON Canvas string
directly, without needing a file on disk. Useful for:
  - API integrations
  - Database-stored canvases
  - Programmatically constructed canvases

Run:
    python examples/02_parse_from_string.py
"""

import json

from canvas_parser import loads, to_mermaid

# ── Build a canvas programmatically as a dict ──────────────────────────────
canvas_data = {
    "nodes": [
        {
            "id": "start",
            "type": "text",
            "x": 0,
            "y": 0,
            "width": 150,
            "height": 60,
            "text": "User signs up",
        },
        {
            "id": "validate",
            "type": "text",
            "x": 200,
            "y": 0,
            "width": 150,
            "height": 60,
            "text": "Validate email",
        },
        {
            "id": "welcome",
            "type": "text",
            "x": 400,
            "y": 0,
            "width": 150,
            "height": 60,
            "text": "Send welcome email",
        },
        {
            "id": "db",
            "type": "file",
            "file": "migrations/001_users.sql",
            "x": 200,
            "y": 100,
            "width": 150,
            "height": 60,
        },
    ],
    "edges": [
        {"id": "e1", "fromNode": "start", "toNode": "validate"},
        {"id": "e2", "fromNode": "validate", "toNode": "welcome"},
        {"id": "e3", "fromNode": "validate", "toNode": "db", "label": "persist"},
    ],
}

# ── Parse from JSON string ────────────────────────────────────────────────
json_string = json.dumps(canvas_data)
canvas = loads(json_string)

print(f"Parsed {len(canvas.nodes)} nodes and {len(canvas.edges)} edges from string.\n")

# ── Convert and display ───────────────────────────────────────────────────
print(to_mermaid(canvas, direction="LR"))
