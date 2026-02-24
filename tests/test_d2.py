from canvas_parser import to_d2


def test_d2_generation(sample_canvas):
    # Generate the string
    d2_str = to_d2(sample_canvas, "right")

    # Basic verifications
    assert d2_str.startswith("direction: right")

    # Verify nesting was created for the group
    assert '754a8ef995f366bc: "JSON Canvas" { ' in d2_str

    # Verify nodes have the right formatting based on type

    # Text Node and explicit styling tests
    assert '59e896bc8da20699: "Learn more:' in d2_str
    assert "shape: rectangle" in d2_str

    # File Node
    assert '8132d4d894c80022: "readme.md"' in d2_str
    assert "shape: package" in d2_str

    # Verify the edge connection and syntax escapes
    assert "7efdbbe0c4742315 -> 59e896bc8da20699" in d2_str
