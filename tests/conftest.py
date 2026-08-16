"""
Shared pytest fixtures and configuration for FastAPI app tests.
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Fixture providing a TestClient connected to the FastAPI app.
    This allows tests to make HTTP requests to the app without running a server.
    """
    return TestClient(app)
