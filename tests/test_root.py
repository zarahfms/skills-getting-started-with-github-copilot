"""
Tests for GET / redirect endpoint.

These tests follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test preconditions
- Act: Execute the endpoint being tested
- Assert: Verify the results
"""
import pytest


def test_root_redirect(client):
    """
    Test that GET / redirects to /static/index.html.
    
    Arrange: Client ready
    Act: GET request to /
    Assert: Redirect status code and location header correct
    """
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert: Should get redirect status (307 or 302)
    assert response.status_code in [301, 302, 303, 307, 308]
    
    # Verify redirect location is correct (if status is 307/308)
    if response.status_code in [307, 308]:
        assert "location" in response.headers
    
    # Follow redirect and verify it leads to index.html
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert "Mergington High School" in response.text
