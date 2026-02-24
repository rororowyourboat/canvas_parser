"""
Diagram rendering — Kroki API client plus local rendering helpers.

This module provides multiple rendering backends:

- :func:`render_diagram` — send diagrams to a `Kroki <https://kroki.io/>`_
  instance (public or self-hosted) and return rendered image bytes.
- :func:`render_mermaid_html` — return a self-contained HTML string that
  renders a Mermaid diagram client-side via mermaid.js CDN.  No diagram
  data leaves the machine.
- :func:`render_d2_local` — render a D2 diagram locally using the ``d2``
  binary (via ``d2-python-wrapper``).  No network access required.
- :func:`encode_kroki_diagram` — low-level helper to compress + base64-encode
  a diagram string into the URL-safe token that Kroki expects.

The Kroki client uses only the Python standard library (``urllib``, ``zlib``,
``base64``) — no ``requests`` or ``httpx`` needed.

Example::

    from canvas_parser import to_d2, render_diagram, parse_canvas

    canvas = parse_canvas("my_diagram.canvas")
    d2_str = to_d2(canvas)

    svg_bytes = render_diagram(d2_str, diagram_type="d2", output_format="svg")
    with open("output.svg", "wb") as f:
        f.write(svg_bytes)
"""

import base64
import json
import urllib.error
import urllib.parse
import urllib.request
import zlib
from typing import Literal


def encode_kroki_diagram(diagram_str: str) -> str:
    """Compress and encode a diagram string for use in a Kroki URL.

    Uses **zlib deflate** (level 9) followed by **base64 URL-safe encoding**
    with padding stripped, as specified in the
    `Kroki docs <https://docs.kroki.io/kroki/setup/encode-diagram/>`_.

    Args:
        diagram_str: The raw diagram source code (Mermaid, D2, etc.).

    Returns:
        A URL-safe encoded string suitable for appending to the Kroki URL.
    """
    compressed = zlib.compress(diagram_str.encode("utf-8"), 9)
    encoded = base64.urlsafe_b64encode(compressed).decode("utf-8").rstrip("=")
    return encoded


def render_diagram(
    diagram_str: str,
    diagram_type: Literal["mermaid", "d2"],
    output_format: Literal["svg", "png", "pdf"] = "svg",
    base_url: str = "https://kroki.io",
) -> bytes:
    """Send a diagram to a Kroki API instance and return rendered image bytes.

    This is a convenience wrapper around :func:`encode_kroki_diagram` that
    builds the full Kroki URL, makes the HTTP request, and returns the
    response body.

    Args:
        diagram_str:   The raw diagram source code (Mermaid, D2, etc.).
        diagram_type:  The rendering engine to use — ``"mermaid"`` or ``"d2"``.
        output_format: The desired output image type — ``"svg"``, ``"png"``,
                       or ``"pdf"``.  Defaults to ``"svg"``.
        base_url:      The base URL of the Kroki instance.  Defaults to the
                       public ``https://kroki.io``.  Set this to a self-hosted
                       instance (e.g. ``http://localhost:8000``) when working
                       with private or sensitive diagrams.

    Returns:
        The binary image data from the Kroki API response.

    Raises:
        RuntimeError: If the HTTP request to the Kroki API fails.
    """
    url = f"{base_url.rstrip('/')}/{diagram_type}/{output_format}"

    payload = json.dumps({"diagram_source": diagram_str}).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "User-Agent": "canvas-parser-kroki-client/1.0",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as response:
            return response.read()
    except urllib.error.URLError as e:
        raise RuntimeError(f"Failed to render diagram via Kroki: {e}")


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
