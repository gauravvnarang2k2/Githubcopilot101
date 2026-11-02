def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_seeded_data(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert expected_activity in payload
    assert "participants" in payload[expected_activity]


def test_signup_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new-student@mergington.edu"

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]

    # Assert
    assert signup_response.status_code == 200
    assert participants.count(email) == 1


def test_unregister_removes_participant(client):
    # Arrange
    activity_name = "Programming Class"
    email = "temporary-student@mergington.edu"
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Act
    unregister_response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]

    # Assert
    assert unregister_response.status_code == 200
    assert email not in participants
