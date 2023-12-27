from locust import HttpUser, task, constant

CLUB_NAME = "Simply Lift"
CLUB_EMAIL = "john@simplylift.co"
COMPETITION_NAME = "Fall Classic Edition 2024"


class PerfServerTest(HttpUser):
    """
    Performance testing using Locust for the server.
    """

    wait_time = constant(1)

    @task
    def index(self):
        """
        Task to simulate a user accessing the / endpoint.

        Returns:
        None
        """
        self.client.get("/")

    @task
    def display_points(self):
        """
        Task to simulate a user accessing the /display_points endpoint.

        Returns:
        None
        """
        self.client.get("/display_points")

    @task
    def show_summary(self):
        """
        Task to simulate a user posting data to the /show_summary endpoint.

        Returns:
        None
        """
        self.client.post("/show_summary", data={"email": CLUB_EMAIL})

    @task
    def purchas_places(self):
        """
        Task to simulate a user posting data to the /purchas_places endpoint.

        Returns:
        None
        """
        print(CLUB_NAME)
        print(COMPETITION_NAME)
        self.client.post("/purchas_places", data={
            "club": CLUB_NAME,
            "competition": COMPETITION_NAME,
            "places": "1"})

    @task
    def book(self):
        """
        Task to simulate a user accessing the /book endpoint.

        Returns:
        None
        """
        self.client.get(f"/book/{COMPETITION_NAME}/{CLUB_NAME}")

    @task
    def logout(self):
        """
        Task to simulate a user accessing the /logout endpoint.

        Returns:
        None
        """
        self.client.get("/logout")
