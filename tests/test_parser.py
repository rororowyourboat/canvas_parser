from canvas_parser import Canvas, FileNode, GroupNode, TextNode


def test_parse_sample_canvas(sample_canvas):
    canvas = sample_canvas

    # Verify canvas instance
    assert isinstance(canvas, Canvas)

    # We know sample.canvas has 5 nodes and 1 edge
    assert len(canvas.nodes) == 5
    assert len(canvas.edges) == 1

    # Specific type verification
    group_nodes = [n for n in canvas.nodes if isinstance(n, GroupNode)]
    file_nodes = [n for n in canvas.nodes if isinstance(n, FileNode)]
    text_nodes = [n for n in canvas.nodes if isinstance(n, TextNode)]

    assert len(group_nodes) == 1
    assert len(file_nodes) == 3
    assert len(text_nodes) == 1

    # Verify group node properties
    gn = group_nodes[0]
    assert gn.id == "754a8ef995f366bc"
    assert gn.label == "JSON Canvas"
    assert gn.width == 610

    # Verify text node properties
    tn = text_nodes[0]
    assert "Learn more:" in tn.text

    # Verify edge properties
    edge = canvas.edges[0]
    assert edge.fromNode == "7efdbbe0c4742315"
    assert edge.toNode == "59e896bc8da20699"
    assert edge.fromSide == "right"
    assert edge.toSide == "left"
