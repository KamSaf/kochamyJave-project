from locust import HttpUser, TaskSet, task


class WebsiteTasks(TaskSet):

    @task(5)
    def home_page(self):
        self.client.get("/")

    @task(4)
    def about_page(self):
        self.client.get("/about")

    @task(3)
    def login_page(self):
        self.client.get("/login_page")

    @task(2)
    def new_post_page(self):
        self.client.get("/new_post")

    @task(1)
    def new_comment_page(self):
        self.client.get("/new_comment/1")


class WebsiteUser(HttpUser):
    # task_set = WebsiteTasks
    tasks = [WebsiteTasks]
    host = "https://kochamyjave.pythonanywhere.com"
    min_wait = 2 * 1000
    max_wait = 6 * 1000