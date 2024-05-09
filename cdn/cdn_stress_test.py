from locust import HttpUser, task, between
import random

file_paths = [
    "test/oral-b-toothbrush.jpg",
    "test/colgate-toothpaste.jpg",
    "test/dabur-red-toothpaste.jpg",
    "test/maggi.jpg",
]

class MyUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def access_homepage(self):
        self.client.get("/")

    @task
    def upload_file(self):
        file_path = random.choice(file_paths)
        files = {'file': open(file_path, 'rb')}
        self.client.post("/upload", files=files)

    @task
    def download_file(self):
        self.client.get(random.choice(file_paths))