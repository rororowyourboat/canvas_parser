"""
Parsing layer — reads JSON Canvas data from files or strings.

This module is the primary entry point for loading ``.canvas`` files.  It
supports two modes:

- :func:`parse_canvas` — reads directly from a file path.
- :func:`loads` — parses from a JSON string already in memory.

Both functions delegate to :func:`_build_canvas`, which maps the raw JSON
dictionaries to typed :mod:`canvas_parser.models` dataclasses.  Unknown
fields in the source JSON are silently ignored via :func:`_safe_construct`,
making the parser forward-compatible with future spec additions.

Example::

    from canvas_parser import parse_canvas, loads

    # From file
    canvas = parse_canvas("vault/my_diagram.canvas")

    # From string (e.g. from an API response)
    canvas = loads(json_string)
"""

import dataclasses
import json
from typing import Any, Type, TypeVar

from .models import Canvas, Edge, FileNode, GroupNode, LinkNode, Node, TextNode

T = TypeVar("T")

_NODE_FACTORIES: dict[str, type[Node]] = {
    "text": TextNode,
    "file": FileNode,
    "link": LinkNode,
    "group": GroupNode,
}


def _safe_construct(cls: Type[T], data: dict[str, Any]) -> T:
    """Construct a dataclass instance, silently ignoring unexpected fields.

    This ensures that unknown keys in the source JSON (e.g. future spec
    additions or user-defined metadata) do not crash the parser.

    Args:
        cls:  The target dataclass type.
        data: Raw dictionary from ``json.load`` / ``json.loads``.

    Returns:
        An instance of *cls* populated only with known fields.
    """
    if not dataclasses.is_dataclass(cls):
        raise TypeError(f"{cls} must be a dataclass")
    known = {f.name for f in dataclasses.fields(cls)}
    return cls(**{k: v for k, v in data.items() if k in known})


def _build_canvas(data: dict[str, Any]) -> Canvas:
    """Shared logic to turn a raw canvas dict into a Canvas object.

    Unknown node types fall back to the base :class:`Node` class.
    """
    nodes: list[Node] = []
    for node_data in data.get("nodes", []):
        node_type = node_data.get("type", "")
        # Use an explicit fallback to satisfy strict type checkers
        factory = _NODE_FACTORIES.get(node_type)
        if factory is None:
            factory = Node
        nodes.append(_safe_construct(factory, node_data))

    edges = [_safe_construct(Edge, e) for e in data.get("edges", [])]
    return Canvas(nodes=nodes, edges=edges)


def parse_canvas(file_path: str) -> Canvas:
    """Parse a ``.canvas`` file from disk.

    Args:
        file_path: Path to the ``.canvas`` JSON file.

    Returns:
        A :class:`~canvas_parser.models.Canvas` containing typed nodes and edges.

    Raises:
        FileNotFoundError: If *file_path* does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return _build_canvas(json.load(f))


def loads(json_string: str) -> Canvas:
    """Parse a JSON Canvas string.

    This is the in-memory equivalent of :func:`parse_canvas` — useful when the
    canvas data comes from an API, database, or clipboard.

    Args:
        json_string: A JSON string conforming to the JSON Canvas spec.

    Returns:
        A :class:`~canvas_parser.models.Canvas` containing typed nodes and edges.

    Raises:
        json.JSONDecodeError: If the string is not valid JSON.
    """
    return _build_canvas(json.loads(json_string))
