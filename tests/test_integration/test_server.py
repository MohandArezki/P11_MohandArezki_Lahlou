import pytest
from http import HTTPStatus
from server import clubs, competitions
from utils import (
    MAX_BOOKING,
    MSG_EMAIL_NOT_FOUND,
    MSG_BOOK_MORE_THAN_AUTORIZED,
    MSG_BOOK_MORE_AVAILABLE_PLACES,
    MSG_BOOK_MORE_AVAILABLE_POINTS,
    MSG_COMPETITION_PASSED
)


class TestIntergration:
    """
    Integration tests for the server.
    """

    @pytest.mark.parametrize(
        "email, expected_status, expected_msg",
        [
            ("invalid_email@test.data", HTTPStatus.BAD_REQUEST, MSG_EMAIL_NOT_FOUND),
            ("john@simplylift.co", HTTPStatus.OK, "Welcome, john@simplylift.co"),
        ],
    )
    def test_show_summary_route(self, client, email, expected_status, expected_msg):
        """
        Test the /show_summary route.

        Args:
        - client: Flask test client.
        - email (str): Email for testing.
        - expected_status (HTTPStatus): Expected HTTP status.
        - expected_msg (str): Expected message in response.

        Returns:
        None
        """
        response = client.post("/show_summary", data={"email": email})
        assert response.status_code == expected_status
        assert expected_msg in response.data.decode()

    @pytest.mark.parametrize(
        "club, competition, RequiredPlaces, HTTP_expected_result, expected_msg",
        [
            # Test purchas_places when trying to book more than 12 places
            (clubs[0]["name"], competitions[2]["name"], 13, HTTPStatus.BAD_REQUEST,
             MSG_BOOK_MORE_THAN_AUTORIZED.format(13, MAX_BOOKING)),
            # Test purchas_places when trying to book using valid data
            (clubs[0]["name"], competitions[2]["name"], 10, HTTPStatus.OK, "Great-booking complete!"),
            # Test purchas_places when trying to book on a passed competition
            (clubs[0]["name"], competitions[0]["name"], 4, HTTPStatus.BAD_REQUEST,
             MSG_COMPETITION_PASSED.format(competitions[0]["name"])),
            # Test purchas_places when trying to book more than available places
            (clubs[0]["name"], competitions[2]["name"], 11, HTTPStatus.BAD_REQUEST,
             MSG_BOOK_MORE_AVAILABLE_PLACES.format(11, 10)),
            # Test purchas_places when trying to book more than available points
            (clubs[0]["name"], competitions[2]["name"], 9,
             HTTPStatus.BAD_REQUEST, MSG_BOOK_MORE_AVAILABLE_POINTS.format(9, 3)),
        ],
    )
    def test_purchas_places(
        self, client, club, competition, RequiredPlaces, HTTP_expected_result, expected_msg
    ):
        """
        Test the /purchas_places route.

        Args:
        - client: Flask test client.
        - club (str): Club name for testing.
        - competition (str): Competition name for testing.
        - RequiredPlaces (int): Number of places required for booking.
        - HTTP_expected_result (HTTPStatus): Expected HTTP status.
        - expected_msg (str): Expected message in response.

        Returns:
        None
        """
        response = client.post(
            "/purchas_places",
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
            ("invalid_club", "invalid_competition", HTTPStatus.BAD_REQUEST, "Something went wrong-please try again"),
            (clubs[0]["name"], "invalid_competition", HTTPStatus.BAD_REQUEST, "Something went wrong-please try again"),
            (clubs[0]["name"], competitions[2]["name"], HTTPStatus.OK, "How many places?"),
        ],
    )
    def test_book(self, client, club, competition, http_expected_result, expected_msg):
        """
        Test the /book route.

        Args:
        - client: Flask test client.
        - club (str): Club name for testing.
        - competition (str): Competition name for testing.
        - http_expected_result (HTTPStatus): Expected HTTP status.
        - expected_msg (str): Expected message in response.

        Returns:
        None
        """
        response = client.get(f"/book/{competition}/{club}")
        assert expected_msg in response.data.decode()
        assert response.status_code == http_expected_result

    def test_display_points(self, client):
        """
        Test the /display_points route.

        Args:
        - client: Flask test client.

        Returns:
        None
        """
        response = client.get("/display_points")
        assert response.status_code == HTTPStatus.OK
        assert "Available points" in response.data.decode()

    def test_logout(self, client):
        """
        Test the /logout route.

        Args:
        - client: Flask test client.

        Returns:
        None
        """
        response = client.get('/logout')
        assert response.status_code == HTTPStatus.FOUND
