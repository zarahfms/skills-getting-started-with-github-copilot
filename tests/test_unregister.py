"""
Tests for DELETE /activities/{activity_name}/unregister endpoint.

These tests follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test preconditions
- Act: Execute the endpoint being tested
- Assert: Verify the results
"""
import pytest


def test_unregister_registered_student(client):
    """
    Test successful unregister for a registered student.
    
    Arrange: Sign up student first, get baseline participant count
    Act: DELETE unregister request
    Assert: Status 200, email removed from participants, success message returned
    """
    # Arrange
    activity_name = "Drama Club"
    email = "diana@mergington.edu"
    
    # First sign up the student
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    assert signup_response.status_code == 200
    
    # Get activities to verify student was added
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    initial_participant_count = len(activities_data[activity_name]["participants"])
    
    # Act: Unregister the student
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered" in data["message"]
    assert email in data["message"]
    
    # Verify email was actually removed
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    final_participant_count = len(activities_data[activity_name]["participants"])
    assert final_participant_count == initial_participant_count - 1
    assert email not in activities_data[activity_name]["participants"]


def test_unregister_not_registered_fails(client):
    """
    Test that unregister for non-registered email returns 400 error.
    
    Arrange: Client ready, email not registered for activity
    Act: DELETE unregister request for non-registered email
    Assert: Status 400, error indicates email not registered
    """
    # Arrange
    activity_name = "Art Workshop"
    email = "ella@mergington.edu"
    
    # Act: Try to unregister email that was never registered
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    error_data = response.json()
    assert "detail" in error_data
    assert "not registered" in error_data["detail"]


def test_unregister_nonexistent_activity(client):
    """
    Test that unregister for non-existent activity returns 404 error.
    
    Arrange: Client ready, invalid activity name
    Act: DELETE unregister request for non-existent activity
    Assert: Status 404, error indicates activity not found
    """
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "frank@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    error_data = response.json()
    assert "detail" in error_data
    assert "not found" in error_data["detail"].lower()
