import json

import pytest

from canvas_parser import Canvas, Edge, Node, TextNode, loads, to_d2, to_mermaid


def test_loads_basic():
    """Verify the string-based entry point works."""
    data = {
        "nodes": [
            {"id": "a", "type": "text", "x": 0, "y": 0, "width": 100, "height": 50, "text": "hi"}
        ],
        "edges": [],
    }
    canvas = loads(json.dumps(data))
    assert isinstance(canvas, Canvas)
    assert len(canvas.nodes) == 1
    assert isinstance(canvas.nodes[0], TextNode)
    assert canvas.nodes[0].text == "hi"


def test_empty_canvas():
    """An empty but valid canvas should parse without error."""
    canvas = loads('{"nodes":[],"edges":[]}')
    assert canvas.nodes == []
    assert canvas.edges == []


def test_missing_nodes_and_edges_keys():
    """A canvas with no nodes/edges keys at all should still parse."""
    canvas = loads("{}")
    assert canvas.nodes == []
    assert canvas.edges == []


def test_unknown_node_type_falls_back():
    """Unknown node types should produce a generic Node."""
    data = {
        "nodes": [{"id": "u1", "type": "custom_widget", "x": 0, "y": 0, "width": 10, "height": 10}],
        "edges": [],
    }
    canvas = loads(json.dumps(data))
    assert len(canvas.nodes) == 1
    assert type(canvas.nodes[0]) is Node


def test_unknown_fields_ignored():
    """Extra / future fields in the JSON should not crash the parser."""
    data = {
        "nodes": [
            {
                "id": "a",
                "type": "text",
                "x": 0,
                "y": 0,
                "width": 10,
                "height": 10,
                "text": "ok",
                "futureField": True,
                "anotherNew": 42,
            }
        ],
        "edges": [
            {
                "id": "e1",
                "fromNode": "a",
                "toNode": "a",
                "unknownProp": "should be ignored",
            }
        ],
    }
    canvas = loads(json.dumps(data))
    assert isinstance(canvas.nodes[0], TextNode)
    assert isinstance(canvas.edges[0], Edge)


def test_malformed_json_raises():
    """Invalid JSON should raise a clear error."""
    with pytest.raises(json.JSONDecodeError):
        loads("this is not json")


def test_invalid_mermaid_direction():
    """Invalid direction should raise ValueError."""
    canvas = Canvas()
    with pytest.raises(ValueError, match="Invalid Mermaid direction"):
        to_mermaid(canvas, "DIAGONAL")


def test_invalid_d2_direction():
    """Invalid direction should raise ValueError."""
    canvas = Canvas()
    with pytest.raises(ValueError, match="Invalid D2 direction"):
        to_d2(canvas, "sideways")
