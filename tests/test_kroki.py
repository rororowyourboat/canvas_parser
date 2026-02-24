from canvas_parser import encode_kroki_diagram


def test_kroki_encoder():
    # Example provided by Kroki documentation: a simple GraphViz hello world
    # graphviz diagram string: "digraph G {Hello->World}"
    test_str = "digraph G {Hello->World}"

    # Kroki document output equivalent encoded for URL should be:
    # "eNpLyUwvSizIUHBXqPZIzcnJ17ULzy_KSakFAGxACMY"
    output = encode_kroki_diagram(test_str)

    assert output == "eNpLyUwvSizIUHBXqPZIzcnJ17ULzy_KSakFAGxACMY"
