"""
Kroki rendering client — encodes diagrams and fetches rendered images.

`Kroki <https://kroki.io/>`_ is a free API that renders diagrams from
textual descriptions.  This module provides two functions:

- :func:`encode_kroki_diagram` — compress + base64-encode a diagram string
  into the URL-safe token that Kroki expects.
- :func:`render_diagram` — one-shot helper that encodes the string, calls
  the Kroki API, and returns the raw image bytes.

The client uses only the Python standard library (``urllib``, ``zlib``,
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
) -> bytes:
    """Send a diagram to the public Kroki API and return rendered image bytes.

    This is a convenience wrapper around :func:`encode_kroki_diagram` that
    builds the full Kroki URL, makes the HTTP request, and returns the
    response body.

    Args:
        diagram_str:   The raw diagram source code (Mermaid, D2, etc.).
        diagram_type:  The rendering engine to use — ``"mermaid"`` or ``"d2"``.
        output_format: The desired output image type — ``"svg"``, ``"png"``,
                       or ``"pdf"``.  Defaults to ``"svg"``.

    Returns:
        The binary image data from the Kroki API response.

    Raises:
        RuntimeError: If the HTTP request to the Kroki API fails.

    Note:
        This function calls the **public** Kroki instance at
        ``https://kroki.io``.  For production workloads, consider
        self-hosting Kroki and modifying the URL.
    """
    url = f"https://kroki.io/{diagram_type}/{output_format}"

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
