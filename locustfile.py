from locust import HttpUser, TaskSet, task


class WebsiteTasks(TaskSet):

    @task(3)
    def home_page(self):
        self.client.get("/")

    @task(2)
    def about_page(self):
        self.client.get("/about")

    @task(1)
    def login_page(self):
        self.client.get("/login_page")


class WebsiteUser(HttpUser):
    # task_set = WebsiteTasks
    tasks = [WebsiteTasks]
    host = "https://kochamyjave.pythonanywhere.com"

    min_wait = 2 * 1000
    max_wait = 6 * 1000