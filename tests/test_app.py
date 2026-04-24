import pytest
import copy
from fastapi.testclient import TestClient
from src.app import app

# Original activities data for reset
ORIGINAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Team practices and intramural games",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["liam@mergington.edu", "ava@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Swim training and aquatic fitness",
        "schedule": "Tuesdays and Thursdays, 3:45 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["nathan@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore painting, sculpture, and mixed media",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["chloe@mergington.edu", "jack@mergington.edu"]
    },
    "Drama Club": {
        "description": "Produce plays and practice acting techniques",
        "schedule": "Tuesdays and Fridays, 4:15 PM - 5:45 PM",
        "max_participants": 20,
        "participants": ["sophia@mergington.edu", "isabella@mergington.edu"]
    },
    "Debate Team": {
        "description": "Research and compete in debate tournaments",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["alex@mergington.edu", "zara@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Prepare for science competitions across disciplines",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["ethan@mergington.edu", "maya@mergington.edu"]
    }
}

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities data before each test."""
    import src.app
    src.app.activities = copy.deepcopy(ORIGINAL_ACTIVITIES)

client = TestClient(app)

# Tests for GET /activities
def test_get_activities():
    # Arrange
    # (data reset by fixture)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 9
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]
    assert "schedule" in data["Chess Club"]
    assert "max_participants" in data["Chess Club"]
    assert "participants" in data["Chess Club"]
    assert isinstance(data["Chess Club"]["participants"], list)

# Tests for POST /activities/{activity_name}/signup
def test_signup_success():
    # Arrange
    email = "new@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}
    # Verify data change
    import src.app
    assert email in src.app.activities[activity]["participants"]

def test_signup_duplicate():
    # Arrange
    email = "michael@mergington.edu"  # already in Chess Club
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_invalid_activity():
    # Arrange
    email = "test@mergington.edu"
    activity = "Nonexistent"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

# Tests for DELETE /activities/{activity_name}/participants/{email}
def test_remove_participant_success():
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.delete(f"/activities/{activity}/participants/{email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity}"}
    # Verify data change
    import src.app
    assert email not in src.app.activities[activity]["participants"]

def test_remove_participant_not_found():
    # Arrange
    email = "not@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.delete(f"/activities/{activity}/participants/{email}")

    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]

def test_remove_invalid_activity():
    # Arrange
    email = "test@mergington.edu"
    activity = "Nonexistent"

    # Act
    response = client.delete(f"/activities/{activity}/participants/{email}")

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

# Test for GET / (redirect)
def test_root_redirect():
    # Arrange
    # (no special setup)

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 307  # redirect
    assert response.headers["location"] == "/static/index.html"