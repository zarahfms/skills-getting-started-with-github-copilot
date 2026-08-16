"""
Tests for POST /activities/{activity_name}/signup endpoint.

These tests follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test preconditions
- Act: Execute the endpoint being tested
- Assert: Verify the results
"""
import pytest


def test_signup_new_student(client):
    """
    Test successful signup for a new student.
    
    Arrange: Client ready, prepare test email
    Act: POST signup request
    Assert: Status 200, email added to participants, success message returned
    """
    # Arrange
    activity_name = "Basketball Team"
    email = "alice@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_signup_duplicate_fails(client):
    """
    Test that duplicate signup for same email returns 400 error.
    
    Arrange: Sign up student once
    Act: Try to sign up same email again
    Assert: Status 400, error indicates already registered
    """
    # Arrange
    activity_name = "Soccer Club"
    email = "bob@mergington.edu"
    
    # First signup should succeed
    response1 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Act: Try duplicate signup
    response2 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response2.status_code == 400
    error_data = response2.json()
    assert "detail" in error_data
    assert "already registered" in error_data["detail"]


def test_signup_nonexistent_activity(client):
    """
    Test that signup for non-existent activity returns 404 error.
    
    Arrange: Client ready, invalid activity name
    Act: POST signup request for non-existent activity
    Assert: Status 404, error indicates activity not found
    """
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "charlie@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    error_data = response.json()
    assert "detail" in error_data
    assert "not found" in error_data["detail"].lower()
