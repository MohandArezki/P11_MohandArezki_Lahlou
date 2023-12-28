from locust import HttpUser, task, constant
from locust.exception import StopUser


CLUB_NAME = "Simply Lift"
CLUB_EMAIL = "john@simplylift.co"
COMPETITION_NAME = "Fall Classic Edition 2024"

class PerfServerTest(HttpUser):
    wait_time = constant(1)
    @task
    def on_start(self):
        self.client.get("/")
        self.client.post("/showSummary", data={"email": CLUB_EMAIL})

    @task
    def displayPoints(self):
        self.client.get("/displayPoints")

    @task()
    def purchasePlaces(self): 
        self.client.post("/purchasePlaces", data={
            "club": CLUB_NAME,
            "competition": COMPETITION_NAME,
            "places": "1"})

    @task
    def book(self):
    
        self.client.get(f"/book/{COMPETITION_NAME}/{CLUB_NAME}")
    
    @task
    def logout(self):
        self.client.get("/logout")
