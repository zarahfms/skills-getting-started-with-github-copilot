"""
Tests for GET /activities endpoint.

These tests follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test preconditions
- Act: Execute the endpoint being tested
- Assert: Verify the results
"""
import pytest


def test_get_all_activities(client):
    """
    Test that GET /activities returns all activities.
    
    Arrange: Client is ready (from fixture)
    Act: Make GET request to /activities
    Assert: Status 200, all 9 activities present with correct structure
    """
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    
    # Verify we have 9 activities
    assert len(activities) == 9
    
    # Verify all expected activities are present
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Soccer Club",
        "Drama Club",
        "Art Workshop",
        "Debate Club",
        "Science Club"
    ]
    for activity in expected_activities:
        assert activity in activities
    
    # Verify activity structure for first activity
    chess_club = activities["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)
