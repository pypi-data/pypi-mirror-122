import os
import requests


class stdpio:

    API = "https://stdp.io/api/"
    ENDPOINTS = {
        "auth": "{}token-auth".format(API),
        "my_models": "{}my-models?format=json".format(API),
    }

    def __init__(self, **kwargs):
        self.token = False
        if kwargs.get("username") and kwargs.get("password"):
            self.username = kwargs.get("username")
            self.password = kwargs.get("password")
            self.authenticate()
            self.model_dir = kwargs.get("model_dir", "/tmp/")

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

    def fetch_model_file(self, model):
        url = model.get("download_path")
        unique_id = model.get("unique_id")
        if url and unique_id:
            filename = "{}.fbz".format(unique_id)
            local_storage_path = os.path.join(self.model_dir, filename)
            with requests.get(
                url,
                stream=True,
                headers={"Authorization": "Token {}".format(self.token)},
            ) as r:
                r.raise_for_status()
                with open(local_storage_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

    def fetch_known(self, model):
        labels = model.get("labels")
        learned = model.get("learned")
        if labels or learned:
            known = {
                "labels": labels,
                "learned": learned,
            }
            return known

    def my_models(self):
        data = self.query(
            "get",
            url=self.ENDPOINTS.get("my_models"),
            headers={"Authorization": "Token {}".format(self.token)},
        )
        return data
