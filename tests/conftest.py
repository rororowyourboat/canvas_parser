import os

import pytest

from canvas_parser import parse_canvas

_FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


@pytest.fixture
def sample_canvas_path():
    """Path to the official JSON Canvas sample file."""
    return os.path.join(_FIXTURES_DIR, "sample.canvas")


@pytest.fixture
def stress_canvas_path():
    """Path to the stress-test canvas file."""
    return os.path.join(_FIXTURES_DIR, "stress.canvas")


@pytest.fixture
def sample_canvas(sample_canvas_path):
    """Pre-parsed Canvas from the sample file."""
    return parse_canvas(sample_canvas_path)


@pytest.fixture
def stress_canvas(stress_canvas_path):
    """Pre-parsed Canvas from the stress file."""
    return parse_canvas(stress_canvas_path)
