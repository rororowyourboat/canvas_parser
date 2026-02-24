"""
D2 converter — transforms a Canvas into D2 declarative diagram syntax.

`D2 <https://d2lang.com/>`_ is a modern, readable diagramming language that
supports nested containers, shapes, and connections natively.

This module produces a D2 script with:

- **Nested containers** for each :class:`~canvas_parser.models.GroupNode`.
- **Shaped declarations** depending on type (``rectangle`` for text,
  ``package`` for files, ``parallelogram`` for links).
- **Connections** with directional arrows and optional labels.

Valid directions: ``down``, ``up``, ``right``, ``left``.

Example::

    from canvas_parser import parse_canvas, to_d2

    canvas = parse_canvas("my_diagram.canvas")
    print(to_d2(canvas, direction="right"))
"""

from ._spatial import group_children
from .models import Canvas, FileNode, GroupNode, LinkNode, Node, TextNode

_VALID_DIRECTIONS = {"down", "right", "left", "up"}


def _escape_d2_string(s: str) -> str:
    """Escape a string for safe use inside D2 quoted labels.

    Handles double-quotes (backslash-escaped) and truncates to 100
    characters for readability.  D2 natively supports newlines inside
    quoted strings, so those are left as-is.
    """
    if not s:
        return ""
    s = s.replace('"', '\\"')

    # Max length truncation for readability
    if len(s) > 100:
        s = s[:97] + "..."

    return s


def to_d2(canvas: Canvas, direction: str = "down") -> str:
    """Convert a :class:`~canvas_parser.models.Canvas` to a D2 script string.

    The output is a complete D2 document ready to be rendered by the D2
    CLI or via the Kroki API.

    Args:
        canvas:    The parsed Canvas object.
        direction: Graph layout direction — one of ``down``, ``up``,
                   ``right``, ``left``.

    Returns:
        A multi-line string containing valid D2 syntax.

    Raises:
        ValueError: If *direction* is not one of the valid values.

    Example::

        d2_str = to_d2(canvas, "right")
        # direction: right
        #
        # group1: "My Group" {
        #   node1: "Hello" {
        #     shape: rectangle
        #   }
        # }
        # node1 -> node2
    """
    if direction not in _VALID_DIRECTIONS:
        raise ValueError(
            f"Invalid D2 direction '{direction}'. Must be one of {sorted(_VALID_DIRECTIONS)}"
        )

    lines = [f"direction: {direction}", ""]

    # Separate groups from other nodes
    group_nodes: list[GroupNode] = [n for n in canvas.nodes if isinstance(n, GroupNode)]
    other_nodes: list[Node] = [n for n in canvas.nodes if not isinstance(n, GroupNode)]

    # Compute containment once via shared spatial utility
    children_map: dict[str, list[Node]] = group_children(group_nodes, other_nodes)
    grouped_node_ids: set[str] = set()

    # 1. Handle Group Nodes (Nested objects in D2)
    for group in group_nodes:
        children = children_map[group.id]
        for child in children:
            grouped_node_ids.add(child.id)

        label = _escape_d2_string(group.label or f"Group {group.id[:8]}")
        lines.append(f'{group.id}: "{label}" {{ ')

        for child in children:
            lines.append(f"  {_node_to_d2(child)}")

        lines.append("}")
        lines.append("")

    # 2. Handle remaining top-level Nodes
    for node in other_nodes:
        if node.id not in grouped_node_ids:
            lines.append(_node_to_d2(node))

    lines.append("")

    # 3. Handle Edges
    for edge in canvas.edges:
        from_id = edge.fromNode
        to_id = edge.toNode

        # Determine endpoint arrows
        link_str = "->"
        if edge.toEnd == "none" and edge.fromEnd == "none":
            link_str = "--"
        elif edge.fromEnd == "arrow" and edge.toEnd == "none":
            link_str = "<-"
        elif edge.fromEnd == "arrow" and edge.toEnd == "arrow":
            link_str = "<->"

        edge_line = f"{from_id} {link_str} {to_id}"
        if edge.label:
            edge_label = _escape_d2_string(edge.label)
            edge_line += f': "{edge_label}"'

        lines.append(edge_line)

    return "\n".join(lines)


def _node_to_d2(node: Node) -> str:
    """Format a single Canvas :class:`~canvas_parser.models.Node` to D2 syntax.

    Shape mapping:

    - :class:`TextNode`  → ``shape: rectangle``
    - :class:`FileNode`  → ``shape: package``
    - :class:`LinkNode`  → ``shape: parallelogram``
    - other              → plain labeled node (no shape override)
    """
    n_id = node.id
    base_line = f"{n_id}"

    if isinstance(node, TextNode):
        label = _escape_d2_string(node.text)
        base_line += f': "{label}"'
        return f"{base_line} {{\n  shape: rectangle\n}}"
    elif isinstance(node, FileNode):
        label_parts = [node.file]
        if node.subpath:
            label_parts.append(node.subpath)
        label = _escape_d2_string(" > ".join(label_parts))
        base_line += f': "{label}"'
        return f"{base_line} {{\n  shape: package\n}}"
    elif isinstance(node, LinkNode):
        label = _escape_d2_string(node.url)
        base_line += f': "{label}"'
        return f"{base_line} {{\n  shape: parallelogram\n}}"
    else:
        # Generic node
        label = _escape_d2_string(f"Node: {n_id[:8]}")
        return f'{base_line}: "{label}"'
