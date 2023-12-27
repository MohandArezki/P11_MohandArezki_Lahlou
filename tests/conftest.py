from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytest
import server


DATE_NEXT_YEAR = datetime.now() + relativedelta(years=1)
DATE_LAST_YEAR = datetime.now() - relativedelta(years=1)

mock_clubs = [
    {"name": "Club One", "email": "admin@clubone.com", "points": "10"},
    {"name": "Club Two", "email": "clubtwo@clubtwo.com", "points": "20"},
]

mock_competitions = [
    {
        "name": f"Competition Classic One - Edition {DATE_NEXT_YEAR.year}",
        "date": DATE_NEXT_YEAR.strftime("%Y-%m-%d %H:%M:%S"),
        "numberOfPlaces": "20",
    },
    {
        "name": f"Competition Classic Two - Edition {DATE_NEXT_YEAR.year}",
        "date": DATE_NEXT_YEAR.strftime("%Y-%m-%d %H:%M:%S"),
        "numberOfPlaces": "5",
    },
    {
        "name": f"Competition Classic Four - Edition {DATE_LAST_YEAR.year}",
        "date": DATE_LAST_YEAR.strftime("%Y-%m-%d %H:%M:%S"),
        "numberOfPlaces": "10",
    },
]
COMP_20_PLACES, COMP_5_PLACES, COMP_PASSED = [competition["name"] for competition in mock_competitions]
CLUB_10_POINTS, CLUB_20_POINTS = [club["name"] for club in mock_clubs]


@pytest.fixture
def client():
    """
    Fixture for creating a test client.
    """
    server.app.config["TESTING"] = True
    with server.app.test_client() as client:
        yield client


@pytest.fixture
def mock_data(mocker):
    """
    Fixture for providing mock data.
    """
    mocker.patch.object(server, "clubs", mock_clubs)
    mocker.patch.object(server, "competitions", mock_competitions)
