from locust import HttpUser, TaskSet, task


class WebsiteTasks(TaskSet):
    @task(3)
    def index(self):
        self.client.get("/")

    @task(1)
    def about_page(self):
        self.client.get("/about")


class WebsiteUser(HttpUser):
    # task_set = WebsiteTasks
    tasks = [WebsiteTasks]
    host = "https://kochamyjave.pythonanywhere.com"

    min_wait = 2 * 1000
    max_wait = 6 * 1000