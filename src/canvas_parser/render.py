"""
Local diagram rendering backends.

This module provides rendering backends that keep all diagram data on the
local machine — nothing is sent to an external server.

Privacy guarantee
-----------------
Both backends process diagram source entirely on your machine:

- :func:`render_mermaid_html` embeds the diagram source in a self-contained
  HTML file.  The only network request the resulting page makes is fetching
  the mermaid.js script from a CDN — the diagram content itself is never
  transmitted.
- :func:`render_d2_local` invokes the ``d2`` binary in a temporary directory
  on disk.  No network access is required or attempted.

No telemetry, analytics, or outbound API calls are made by this module.

Backends
--------
- :func:`render_mermaid_html` — client-side Mermaid via mermaid.js CDN.
- :func:`render_d2_local` — local D2 binary via ``d2-python-wrapper``.
"""

from typing import Literal


def render_mermaid_html(diagram_str: str) -> str:
    """Return a self-contained HTML string that renders a Mermaid diagram
    client-side via mermaid.js CDN.

    The diagram source is embedded directly in the HTML — only the CDN
    script URL hits the network, so **no diagram data leaves the machine**.

    The returned HTML can be used with ``mo.iframe()`` in a marimo notebook
    or written to a standalone ``.html`` file.

    Args:
        diagram_str: Raw Mermaid diagram source code.

    Returns:
        A complete HTML document string that renders the diagram in a browser.
    """
    import html as _html

    escaped = _html.escape(diagram_str)
    return f"""\
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<style>body {{ margin: 0; display: flex; justify-content: center; }}</style>
</head>
<body>
<pre class="mermaid">
{escaped}
</pre>
<script>mermaid.initialize({{ startOnLoad: true }});</script>
</body>
</html>"""


def render_d2_local(
    diagram_str: str,
    output_format: Literal["svg", "png", "pdf"] = "svg",
) -> bytes:
    """Render a D2 diagram locally using the ``d2`` binary via
    ``d2-python-wrapper``.

    This function requires the optional ``d2-python-wrapper`` package::

        uv add "canvas-parser[local]"

    Args:
        diagram_str:   Raw D2 diagram source code.
        output_format: Desired output format — ``"svg"``, ``"png"``, or
                       ``"pdf"``.  Defaults to ``"svg"``.

    Returns:
        The rendered image data as bytes.

    Raises:
        ImportError: If ``d2-python-wrapper`` is not installed.
        RuntimeError: If the ``d2`` binary fails to render the diagram.
    """
    try:
        import d2_python  # noqa: F811
    except ImportError:
        raise ImportError(
            "d2-python-wrapper is required for local D2 rendering. "
            "Install it with: uv add 'd2-python-wrapper' "
            "or install canvas-parser with: uv add 'canvas-parser[local]'"
        )

    import os
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.d2")
        output_path = os.path.join(tmpdir, f"output.{output_format}")

        with open(input_path, "w", encoding="utf-8") as f:
            f.write(diagram_str)

        try:
            d2_python.compile(input_path, output_path)
        except Exception as e:
            raise RuntimeError(f"D2 rendering failed: {e}")

        with open(output_path, "rb") as f:
            return f.read()
