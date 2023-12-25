MSG_EMAIL_NOT_FOUND = "Email not found. Please verify the entered email address and try again."

class EmailError(Exception):
    def __init__(self, message="email error"):
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
    raise EmailError(MSG_EMAIL_NOT_FOUND)
