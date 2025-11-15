from locust import HttpUser, task, between
import random

FIXED_MENU_ITEMS = [1, 2, 3, 4, 5, 6]
class Customer(HttpUser):
    wait_time = between(1, 15)   
    def generate_customer_info(self):
        names = ["Chan Tai Man", "Chan Siu Ming", "Chan Ka Lok", "Chan Mei Ling", "Hugo Cheung", "Joe Chan"]
        return {
            "customer_name": random.choice(names),
            "customer_phone": f"{random.randint(5000, 9999)} {random.randint(1000, 9999)}",
            "customer_address": f"{random.randint(1, 999)} Floor {random.randint(1, 50)}, Building {random.randint(1, 99)}, Random District"
        }   
    @task(5)
    def purchasing_product_by_customer(self):
        self.client.get("/menu")
        num_items = random.randint(1, 6)
        purchasing_items = random.sample(FIXED_MENU_ITEMS, num_items)
        for item in purchasing_items:
            qty = random.randint(1, 6)
            self.client.post(f"/add_to_cart/{item}", data={"qty": qty})
        data_of_customer = self.generate_customer_info()
        self.client.post("/checkout", data=data_of_customer)

class Admin(HttpUser):
    wait_time = between(5, 20)
    @task(3)
    def view_admin(self):
        self.client.get("/admin")
    @task(1)
    def view_orders(self):
        self.client.get("/my_orders")