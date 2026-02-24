from canvas_parser import to_mermaid


def test_mermaid_generation(sample_canvas):
    # Generate the string
    mermaid_str = to_mermaid(sample_canvas, "LR")

    # Basic verifications
    assert mermaid_str.startswith("graph LR")

    # Verify subgraph was created for the group
    assert 'subgraph 754a8ef995f366bc["JSON Canvas"]' in mermaid_str

    # Verify nodes have the right formatting based on type

    # Text Node
    assert '59e896bc8da20699("Learn more:' in mermaid_str

    # File Nodes
    assert '8132d4d894c80022[["readme.md"]]' in mermaid_str
    assert '7efdbbe0c4742315[["_site/logo.svg"]]' in mermaid_str
    assert '0ba565e7f30e0652[["spec/1.0.md"]]' in mermaid_str

    # Verify the edge
    # sample.canvas has edge from 7efdbbe0c4742315 to 59e896bc8da20699.
    # Both end shapes are default (toEnd=arrow, fromEnd=none) -> -->
    assert "7efdbbe0c4742315 --> 59e896bc8da20699" in mermaid_str
