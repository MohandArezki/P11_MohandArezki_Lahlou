
from datetime import datetime

MSG_EMAIL_NOT_FOUND = "Email not found. Please verify the entered email address and try again."
MSG_COMPETITION_PASSED ="The competition ({}) is no longer available."

class EmailError(Exception):
    def __init__(self, message=MSG_EMAIL_NOT_FOUND):
        self.message = message
        super().__init__(self.message)

class BookingError(Exception):
    def __init__(self, message="Booking error"):
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


def check_competition_validity(competition):
    """Check if the competition is valid.

    Args:
        competition: A dictionary representing the competition.

    Returns:
        True if the competition is valid, raises BookingError otherwise.
    """
    # Prevent booking on passed competition
    if datetime.fromisoformat(competition["date"]) < datetime.now():
        raise BookingError(
            MSG_COMPETITION_PASSED.format(competition['name'])
        )

    return True
