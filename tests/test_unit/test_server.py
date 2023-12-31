import pytest
from http import HTTPStatus
from tests.conftest import CLUB_10_POINTS, CLUB_20_POINTS, COMP_20_PLACES, COMP_5_PLACES, COMP_PASSED
from utils import (
    MAX_BOOKING,
    MSG_EMAIL_NOT_FOUND, 
    MSG_BOOK_MORE_THAN_AUTORIZED,
    MSG_BOOK_MORE_AVAILABLE_PLACES,
    MSG_BOOK_MORE_AVAILABLE_POINTS,
    MSG_COMPETITION_PASSED
    )

UNKNOWN_CLUB = {"name": "Unknown Club", "email": "admin@unknown.com", "points": "18"}
UNKNOWN_COMPETITION = {"name": "Unknown Competition", "date": "2024-05-10 15:30:00", "numberOfPlaces": "20"}
MSG_WELCOME = "Welcome to the GUDLFT Registration Portal!"


class TestUnit:
      
    def test_index(self, client):
        response = client.get('/')
        assert response.status_code == HTTPStatus.OK
        assert MSG_WELCOME in response.data.decode()

    def test_displayPoints(self, client,mock_data):

        response = client.get("/displayPoints")

        assert response.status_code == HTTPStatus.OK
        assert "Available points" in response.data.decode()

    @pytest.mark.parametrize(
        "email, expected_status, expected_msg",
        [
            ("invalid_email@test.data", HTTPStatus.BAD_REQUEST, MSG_EMAIL_NOT_FOUND),
            ("admin@clubone.com", HTTPStatus.OK, "Welcome, admin@clubone.com"),
        ],
    )
    def test_showSummary(self, client, mock_data, email, expected_status, expected_msg):

        response = client.post("/showSummary", data={"email": email})

        assert response.status_code == expected_status
        assert expected_msg in response.data.decode()

    @pytest.mark.parametrize(
        "club, competition, RequiredPlaces, http_expected_result, expected_msg",
        [
            # Test purchasePlaces when try to book more than 12 places
            (CLUB_20_POINTS, COMP_20_PLACES, 13, HTTPStatus.BAD_REQUEST,
             MSG_BOOK_MORE_THAN_AUTORIZED.format(13, MAX_BOOKING)),
            # Test purchasePlaces when try to book on passed competition
            (CLUB_10_POINTS, COMP_PASSED, 4, HTTPStatus.BAD_REQUEST, MSG_COMPETITION_PASSED.format(COMP_PASSED)),
            # Test purchasePlaces when try to book more than available places
            (CLUB_20_POINTS, COMP_5_PLACES, 8, HTTPStatus.BAD_REQUEST, MSG_BOOK_MORE_AVAILABLE_PLACES.format(8, 5)),
            # Test purchasePlaces when try to book more than available points
            (CLUB_10_POINTS, COMP_20_PLACES, 11, HTTPStatus.BAD_REQUEST, MSG_BOOK_MORE_AVAILABLE_POINTS.format(11, 10)),
            # Test purchasePlaces when try to book using valid data
            (CLUB_10_POINTS, COMP_5_PLACES, 4, HTTPStatus.OK, "Great-booking complete!"),
        ],
    )
    def test_purchasePlaces(
        self, client, mock_data, club, competition, RequiredPlaces, http_expected_result, expected_msg
    ):

        response = client.post(
            "/purchasePlaces",
            data={
                "club": club,
                "competition": competition,
                "places": RequiredPlaces
            }
        )
        
        assert response.status_code == http_expected_result
        assert expected_msg in response.data.decode()

    @pytest.mark.parametrize(
        "club,competition, http_expected_result,expected_msg",
        [
            ("invalid_club","invalid_competition",HTTPStatus.BAD_REQUEST, "Something went wrong-please try again"),
            (CLUB_10_POINTS,"invalid_competition",HTTPStatus.BAD_REQUEST, "Something went wrong-please try again"),
            (CLUB_10_POINTS,COMP_20_PLACES,HTTPStatus.OK, "How many places?"),        
        ],

    )
    def test_book(self, client, mock_data, club,competition, http_expected_result, expected_msg):

        response = client.get(f"/book/{competition}/{club}")
        assert expected_msg in response.data.decode()
        assert response.status_code == http_expected_result


    def test_logout(self, client):
        response = client.get('/logout')
        assert response.status_code == HTTPStatus.FOUND
