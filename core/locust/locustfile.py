from locust import HttpUser, task


class HelloWorldUser(HttpUser):

    # def on_start(self):
        # response = self.client.post("/account/api/v1/token/jwt/create/",
        #                             data={"email": "admin@admin.com",
        #                                   "password": "Mn00137400"
        #                                   }
        #                             ).json()

    @task
    def test_posts(self):
        response = self.client.get("/blog/api/v1/post/", )

        print(response.status_code)
        print(response.text)
