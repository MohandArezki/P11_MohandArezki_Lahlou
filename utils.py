from datetime import datetime

MSG_EMAIL_NOT_FOUND = "Email not found. Please verify the entered email address and try again."
MSG_COMPETITION_PASSED = "The competition ({}) is no longer available."
MSG_BOOK_MORE_THAN_AUTORIZED = "Trying to book ({}) places. Booking more than ({}) places is not allowed."
MSG_BOOK_MORE_AVAILABLE_PLACES = "Trying to book ({}) places. Available, only ({}) places."
MSG_BOOK_MORE_AVAILABLE_POINTS = "Trying to book ({}) places. Not enough available points, only ({})."

MAX_BOOKING = 12


class EmailError(Exception):
    def __init__(self, message=MSG_EMAIL_NOT_FOUND):
        """
        Initialize an EmailError.

        Args:
        - message (str): The error message.
        """
        self.message = message
        super().__init__(self.message)


class BookingError(Exception):
    def __init__(self, message="Booking error"):
        """
        Initialize a BookingError.

        Args:
        - message (str): The error message.
        """
        self.message = message
        super().__init__(self.message)


def search_club_by_email(email, clubs):
    """
    Get the club with the specified email.

    Parameters:
    - email (str): The email to search for.
    - clubs (list): List of dictionaries representing clubs.

    Returns:
    - dict: Club with the specified email.

    Raises:
    - EmailError: If the email is not found in any club.
    """
    for club in clubs:
        if club.get('email') == email:
            return club
    raise EmailError()


def check_booking_validity(competition, places_required, club):
    """
    Check if the competition is valid.

    Args:
        competition (dict): A dictionary representing the competition.
        places_required (int): The number of places required for booking.

    Returns:
        bool: True if the competition is valid.

    Raises:
        BookingError: If the competition has passed or the booking exceeds the authorized limit.
    """
    # Prevent booking on passed competition
    if datetime.fromisoformat(competition["date"]) < datetime.now():
        raise BookingError(
            MSG_COMPETITION_PASSED.format(competition['name'])
        )

    # Prevent booking more than 12 places
    if places_required > MAX_BOOKING:
        raise BookingError(
            MSG_BOOK_MORE_THAN_AUTORIZED.format(places_required, MAX_BOOKING)
        )

    # Prevent booking more than available places
    if places_required > int(competition['numberOfPlaces']):
        raise BookingError(
            MSG_BOOK_MORE_AVAILABLE_PLACES.format(places_required, competition['numberOfPlaces'])
        )

    # Prevent booking more places than available points
    if places_required > int(club['points']):
        raise BookingError(
            MSG_BOOK_MORE_AVAILABLE_POINTS.format(places_required, club['points'])
        )

    return True
