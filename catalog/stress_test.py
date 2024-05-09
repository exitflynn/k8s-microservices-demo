from locust import HttpUser, task, between, constant
import json
import random

class FastAPIUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_products(self):
        self.client.get("products")

    @task
    def get_product(self):
        product_id = random.randint(1, 100)  # Assuming product IDs are in the range of 1 to 100
        self.client.get(f"products/{product_id}")

    @task
    def add_product(self):
        product = {
            "id": random.randint(101, 200),  # Assuming new product ID starts from 101
            "name": "New Product",
            "description": "New Product Description",
            "price": 10.99
        }
        headers = {'Content-Type': 'application/json'}
        self.client.post("products", data=json.dumps(product), headers=headers)

    @task
    def update_product(self):
        product_id = random.randint(1, 100)  # Assuming product IDs are in the range of 1 to 100
        product = {
            "name": "Updated Product",
            "description": "Updated Product Description",
            "price": 19.99
        }
        headers = {'Content-Type': 'application/json'}
        self.client.put(f"products/{product_id}", data=json.dumps(product), headers=headers)

    @task
    def delete_product(self):
        product_id = random.randint(1, 100)  # Assuming product IDs are in the range of 1 to 100
        self.client.delete(f"products/{product_id}")

