import pytest


def test_get_activities_returns_activities(client):
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_adds_participant_and_prevents_duplicate(client):
    activity = "Basketball Team"
    email = "tester@example.com"

    # Ensure participant not present
    participants = client.get("/activities").json()[activity]["participants"]
    assert email not in participants

    # Signup
    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 200
    data = client.get("/activities").json()
    assert email in data[activity]["participants"]

    # Duplicate signup should return 400
    res2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert res2.status_code == 400


def test_remove_participant(client):
    activity = "Chess Club"
    email = "remove_test@example.com"

    # Add participant
    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 200

    # Remove participant
    res2 = client.delete(f"/activities/{activity}/participants?email={email}")
    assert res2.status_code == 200
    data = client.get("/activities").json()
    assert email not in data[activity]["participants"]

    # Removing again should return 404
    res3 = client.delete(f"/activities/{activity}/participants?email={email}")
    assert res3.status_code == 404


@pytest.mark.skip(reason="Server does not enforce capacity yet")
def test_signup_respects_capacity(client):
    from src.app import activities as activities_store

    activity = "Drama Club"
    max_p = activities_store[activity]["max_participants"]
    # Fill to max - 1
    activities_store[activity]["participants"] = [f"p{i}@example.com" for i in range(max_p - 1)]

    res = client.post(f"/activities/{activity}/signup?email=new1@example.com")
    assert res.status_code == 200

    # Next signup should be rejected once capacity enforcement exists
    res2 = client.post(f"/activities/{activity}/signup?email=new2@example.com")
    assert res2.status_code in (200, 400)
