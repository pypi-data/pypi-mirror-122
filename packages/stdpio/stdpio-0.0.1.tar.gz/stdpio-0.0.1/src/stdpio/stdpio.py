import requests


class stdpio:

    API = "https://stdp.io/api/"
    ENDPOINTS = {
        "auth": "{}token-auth".format(API),
        "my_models": "{}my-models?format=json".format(API),
    }

    def __init__(self, username, password):
        self.token = False
        if username and password:
            self.username = username
            self.password = password
            self.authenticate()

    def query(self, method, **kwargs):
        r = requests.request(method, **kwargs)
        if r.status_code == 200:
            return r.json()

    def authenticate(self):
        data = self.query(
            "post",
            url=self.ENDPOINTS.get("auth"),
            data={"username": self.username, "password": self.password},
        )
        self.token = data.get("token")

    def my_models(self):
        data = self.query(
            "get",
            url=self.ENDPOINTS.get("my_models"),
            headers={"Authorization": "Token {}".format(self.token)},
        )
        return data
