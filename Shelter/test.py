import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 2.5)
    pets=[4,5,6]

    @task
    def pets(self):
        self.client.get("pets/1/")

    @task
    def news(self):
        self.client.get("news")

