from canvas_parser import to_d2, to_mermaid


def test_stress_canvas_parsing(stress_canvas):
    # Verify counts
    assert len(stress_canvas.nodes) == 6
    assert len(stress_canvas.edges) == 3


def test_stress_mermaid_output(stress_canvas):
    mermaid_str = to_mermaid(stress_canvas, "LR")

    # Verify Subgraphs (g1 encompasses g2, n1, n2, n3 based on coordinates)
    assert 'subgraph g1["Infrastructure"]' in mermaid_str
    assert 'subgraph g2["VPC"]' in mermaid_str


def test_stress_d2_output(stress_canvas):
    d2_str = to_d2(stress_canvas, "down")

    # Verify escaped multi-line text mapping
    assert "n4" in d2_str

    # Verify edge types
    assert "n1 -- n2" in d2_str  # toEnd none, fromEnd none
    assert "n2 <-> n3" in d2_str  # toEnd arrow, fromEnd arrow
