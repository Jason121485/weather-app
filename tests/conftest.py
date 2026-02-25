"""
Pytest configuration and fixtures for the weather dashboard app.
"""
import pytest
from app import app


@pytest.fixture
def client():
    """Flask test client with testing config."""
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c
