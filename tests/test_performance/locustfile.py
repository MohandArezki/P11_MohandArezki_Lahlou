from locust import HttpUser, task, constant

CLUB_NAME = "Simply Lift"
CLUB_EMAIL = "john@simplylift.co"
COMPETITION_NAME = "Fall Classic Edition 2024"

class PerfServerTest(HttpUser):
    wait_time = constant(1)

    @task
    def index(self):
        self.client.get("/")

    @task
    def displayPoints(self):
        self.client.get("/displayPoints")

    @task
    def showSummary(self):
        
        self.client.post("/showSummary", data={"email": CLUB_EMAIL})

    @task
    def purchasePlaces(self):
        print(CLUB_NAME)
        print(COMPETITION_NAME)
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