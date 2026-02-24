"""
Mermaid.js converter — transforms a Canvas into a Mermaid flowchart.

`Mermaid <https://mermaid.js.org/>`_ is a popular text-based diagramming
language supported natively in GitHub markdown, GitLab, Notion, and many
other platforms.

This module produces a ``graph`` definition with:

- **Subgraphs** for each :class:`~canvas_parser.models.GroupNode`.
- **Shaped nodes** depending on type (rounded rect for text, subroutine
  for files, parallelogram for links).
- **Edges** with directional arrows and optional labels.

Valid directions: ``TB`` (top → bottom), ``BT``, ``LR`` (left → right),
``RL``, ``TD``.

Example::

    from canvas_parser import parse_canvas, to_mermaid

    canvas = parse_canvas("my_diagram.canvas")
    print(to_mermaid(canvas, direction="LR"))
"""

from ._spatial import group_children
from .models import Canvas, FileNode, GroupNode, LinkNode, Node, TextNode

_VALID_DIRECTIONS = {"TB", "BT", "LR", "RL", "TD"}


def _escape_mermaid_string(s: str) -> str:
    """Escape a string for safe use inside Mermaid node labels.

    Handles double-quotes (replaced with ``&quot;``), newlines (replaced
    with ``<br>``), square/round/curly brackets (HTML entities to prevent
    Mermaid interpreting them as node shapes), and truncates to 100
    characters for readability.
    """
    if not s:
        return ""
    # Strip Obsidian-flavoured markdown that has no meaning in diagrams
    s = s.replace("**", "")
    s = s.replace("[[", "")
    s = s.replace("]]", "")
    # Replace pipe used in Obsidian wikilinks (display text separator)
    s = s.replace("|", " - ")
    # Replace quotes that would break mermaid syntax
    s = s.replace('"', "&quot;")
    # Replace brackets that Mermaid interprets as node-shape delimiters
    s = s.replace("[", "&lsqb;")
    s = s.replace("]", "&rsqb;")
    s = s.replace("{", "&lbrace;")
    s = s.replace("}", "&rbrace;")
    # Replace newlines with <br> for mermaid
    s = s.replace("\n", "<br>")
    # Max length truncation for readability
    if len(s) > 100:
        s = s[:97] + "..."
    return s


def to_mermaid(canvas: Canvas, direction: str = "TB") -> str:
    """Convert a :class:`~canvas_parser.models.Canvas` to a Mermaid flowchart string.

    The output is a complete ``graph`` definition ready to be embedded in a
    markdown code-fence or passed to a Mermaid renderer.

    Args:
        canvas:    The parsed Canvas object.
        direction: Graph layout direction — one of ``TB``, ``BT``, ``LR``,
                   ``RL``, ``TD``.

    Returns:
        A multi-line string containing valid Mermaid syntax.

    Raises:
        ValueError: If *direction* is not one of the valid values.

    Example::

        mermaid_str = to_mermaid(canvas, "LR")
        # graph LR
        #     subgraph group1["My Group"]
        #         node1("Hello")
        #     end
        #     node1 --> node2
    """
    if direction not in _VALID_DIRECTIONS:
        raise ValueError(
            f"Invalid Mermaid direction '{direction}'. Must be one of {sorted(_VALID_DIRECTIONS)}"
        )

    lines = [f"graph {direction}"]

    # Separate groups from other nodes
    group_nodes: list[GroupNode] = [n for n in canvas.nodes if isinstance(n, GroupNode)]
    other_nodes: list[Node] = [n for n in canvas.nodes if not isinstance(n, GroupNode)]

    # Compute containment once via shared spatial utility
    children_map: dict[str, list[Node]] = group_children(group_nodes, other_nodes)
    grouped_node_ids: set[str] = set()

    # 1. Handle Group Nodes (Mermaid Subgraphs)
    for group in group_nodes:
        children = children_map[group.id]
        for child in children:
            grouped_node_ids.add(child.id)

        label = _escape_mermaid_string(group.label or f"Group {group.id[:8]}")
        lines.append(f'    subgraph {group.id}["{label}"]')

        for child in children:
            lines.append(f"        {_node_to_mermaid(child)}")

        lines.append("    end")

    # 2. Handle remaining top-level Nodes
    for node in other_nodes:
        if node.id not in grouped_node_ids:
            lines.append(f"    {_node_to_mermaid(node)}")

    # 3. Handle Edges
    for edge in canvas.edges:
        from_id = edge.fromNode
        to_id = edge.toNode

        # Determine endpoint arrows
        link_str = "-->"
        if edge.toEnd == "none" and edge.fromEnd == "none":
            link_str = "---"
        elif edge.fromEnd == "arrow" and edge.toEnd == "none":
            link_str = "<--"
        elif edge.fromEnd == "arrow" and edge.toEnd == "arrow":
            link_str = "<-->"

        if edge.label:
            edge_label = _escape_mermaid_string(edge.label)
            link_str = f'{link_str}|"{edge_label}"|'

        lines.append(f"    {from_id} {link_str} {to_id}")

    return "\n".join(lines)


def _node_to_mermaid(node: Node) -> str:
    """Format a single Canvas :class:`~canvas_parser.models.Node` to Mermaid syntax.

    Shape mapping:

    - :class:`TextNode`  → rounded rectangle  ``id("label")``
    - :class:`FileNode`  → subroutine shape   ``id[["label"]]``
    - :class:`LinkNode`  → parallelogram      ``id[/"label"/]``
    - other              → standard rectangle  ``id["label"]``
    """
    n_id = node.id

    if isinstance(node, TextNode):
        label = _escape_mermaid_string(node.text) or " "
        return f'{n_id}("{label}")'  # Rounded rect
    elif isinstance(node, FileNode):
        label_parts = [node.file]
        if node.subpath:
            label_parts.append(node.subpath)
        label = _escape_mermaid_string(" > ".join(label_parts))
        return f'{n_id}[["{label}"]]'  # Subroutine shape for files
    elif isinstance(node, LinkNode):
        label = _escape_mermaid_string(node.url)
        return f'{n_id}[/"{label}"/]'  # Parallelogram for URLs
    else:
        # Generic node
        label = _escape_mermaid_string(f"Node: {n_id[:8]}")
        return f'{n_id}["{label}"]'  # Standard rect
