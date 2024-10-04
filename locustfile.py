from locust import HttpUser, TaskSet, task, between
import random

class UserBehaviour(TaskSet):
    @task
    def like_post(self):
        post_id = random.randint(1,4)
        self.client.get(f"/like/{post_id}") 
        
        
class WebsiteUser(HttpUser):
    tasks = [UserBehaviour]
    wait_time = between(1,2)