import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # Use a test activity
    activity = "Chess Club"
    test_email = "pytestuser@mergington.edu"

    # Sign up
    signup_resp = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert signup_resp.status_code == 200 or signup_resp.status_code == 400
    # If already signed up, 400 is valid

    # Unregister
    unregister_resp = client.post(f"/activities/{activity}/unregister", json={"email": test_email})
    assert unregister_resp.status_code == 200 or unregister_resp.status_code == 400
    # If not registered, 400 is valid

    # Confirm removal
    activities = client.get("/activities").json()
    assert test_email not in activities[activity]["participants"]
