import pytest
from http import HTTPStatus
from server import clubs,competitions

from utils import (
    MAX_BOOKING,
    MSG_EMAIL_NOT_FOUND, 
    MSG_BOOK_MORE_THAN_AUTORIZED,
    MSG_BOOK_MORE_AVAILABLE_PLACES,
    MSG_BOOK_MORE_AVAILABLE_POINTS,
    MSG_COMPETITION_PASSED
    )

class TestIntergration:
    
    @pytest.mark.parametrize(
        "email, expected_status, expected_msg",
        [
            ("invalid_email@test.data", HTTPStatus.BAD_REQUEST, MSG_EMAIL_NOT_FOUND),
            ("john@simplylift.co", HTTPStatus.OK, "Welcome, john@simplylift.co"),
        ],
    )
    def test_show_summary_route(self, client, email, expected_status, expected_msg):
       
        response = client.post("/showSummary", data={"email": email})
        assert response.status_code == expected_status
        assert expected_msg in response.data.decode()
    
    @pytest.mark.parametrize(
        "club, competition, RequiredPlaces, HTTP_expected_result, expected_msg",
        [
        # Test purchasePlaces when try to book more than 12 places
        (clubs[0]["name"], competitions[2]["name"], 13, HTTPStatus.BAD_REQUEST, MSG_BOOK_MORE_THAN_AUTORIZED.format(13, MAX_BOOKING)),
        # Test purchasePlaces when try to book using valid data
        (clubs[0]["name"], competitions[2]["name"], 10, HTTPStatus.OK, "Great-booking complete!"),
        
        # Test purchasePlaces when try to book on passed competition
        (clubs[0]["name"], competitions[0]["name"], 4, HTTPStatus.BAD_REQUEST, MSG_COMPETITION_PASSED.format(competitions[0]["name"])),
        # Test purchasePlaces when try to book more than available places
        (clubs[0]["name"], competitions[2]["name"], 11, HTTPStatus.BAD_REQUEST, MSG_BOOK_MORE_AVAILABLE_PLACES.format(11, 10)),
        # Test purchasePlaces when try to book more than available points
        (clubs[0]["name"], competitions[2]["name"], 9, HTTPStatus.BAD_REQUEST, MSG_BOOK_MORE_AVAILABLE_POINTS.format(9, 3)),
        ],
    )
    def test_purchasePlaces(
        self, client, club, competition, RequiredPlaces, HTTP_expected_result, expected_msg
    ):
        
        response = client.post(
            "/purchasePlaces",
            data={
            "club": club,
            "competition": competition,
            "places": RequiredPlaces
            }
        )
        assert response.status_code == HTTP_expected_result
        assert expected_msg in response.data.decode()

    @pytest.mark.parametrize(
        "club,competition, http_expected_result,expected_msg",
        [
            ("invalid_club","invalid_competition",HTTPStatus.BAD_REQUEST, "Something went wrong-please try again"),
            (clubs[0]["name"],"invalid_competition",HTTPStatus.BAD_REQUEST, "Something went wrong-please try again"),
            (clubs[0]["name"], competitions[2]["name"],HTTPStatus.OK, "How many places?"),        
        ],

    )
    def test_book(self, client, club,competition, http_expected_result, expected_msg):

        response = client.get(f"/book/{competition}/{club}")
        assert expected_msg in response.data.decode()
        assert response.status_code == http_expected_result

    def test_displayPoints(self, client):

        response = client.get("/displayPoints")

        assert response.status_code == HTTPStatus.OK
        assert "Available points" in response.data.decode()

    def test_logout(self, client):
        response = client.get('/logout')
        assert response.status_code == HTTPStatus.FOUND
    