"""
Integration tests for multi-step scenarios.

These tests follow the AAA (Arrange-Act-Assert) pattern and combine
multiple endpoints to verify the system works end-to-end.
"""
import pytest


def test_signup_verify_unregister_flow(client):
    """
    Test the complete flow: signup -> verify in list -> unregister -> verify removed.
    
    Arrange: Client ready
    Act: Signup, get activities, unregister
    Assert: Student appears after signup, disappears after unregister
    """
    # Arrange
    activity_name = "Debate Club"
    email = "grace@mergington.edu"
    
    # Act 1: Sign up student
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    assert signup_response.status_code == 200
    
    # Assert 1: Verify student is in participants list
    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]
    initial_count = len(activities[activity_name]["participants"])
    
    # Act 2: Unregister student
    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    assert unregister_response.status_code == 200
    
    # Assert 2: Verify student is no longer in participants list
    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]
    final_count = len(activities[activity_name]["participants"])
    assert final_count == initial_count - 1


def test_multiple_students_signup_and_unregister(client):
    """
    Test that multiple students can sign up and unregister independently.
    
    Arrange: Client ready
    Act: Multiple signups and unregisters
    Assert: Each operation succeeds and state is correct
    """
    # Arrange
    activity_name = "Science Club"
    students = [
        "henry@mergington.edu",
        "iris@mergington.edu",
        "jack@mergington.edu"
    ]
    
    # Act 1: All students sign up
    for email in students:
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Assert 1: All students are in participants list
    activities = client.get("/activities").json()
    for email in students:
        assert email in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == len(students)
    
    # Act 2: Unregister first student
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": students[0]}
    )
    assert response.status_code == 200
    
    # Assert 2: First student removed, others still there
    activities = client.get("/activities").json()
    assert students[0] not in activities[activity_name]["participants"]
    assert students[1] in activities[activity_name]["participants"]
    assert students[2] in activities[activity_name]["participants"]
    
    # Act 3: Unregister second student
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": students[1]}
    )
    assert response.status_code == 200
    
    # Assert 3: Only last student remains
    activities = client.get("/activities").json()
    assert students[0] not in activities[activity_name]["participants"]
    assert students[1] not in activities[activity_name]["participants"]
    assert students[2] in activities[activity_name]["participants"]
