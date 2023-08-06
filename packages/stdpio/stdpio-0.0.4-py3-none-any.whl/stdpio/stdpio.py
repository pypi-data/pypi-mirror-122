import os
import time
import requests
import threading
from datetime import datetime


class stdpio:

    API = "https://stdp.io/api/"
    ENDPOINTS = {
        "auth": "{}token-auth".format(API),
        "my_models": "{}my-models".format(API),
        "download_model": "{}download-model".format(API),
    }

    def __init__(self, **kwargs):
        # init values
        self.models_to_sync = []
        self.token = False

        # set credentials
        if kwargs.get("username") and kwargs.get("password"):
            self.username = kwargs.get("username")
            self.password = kwargs.get("password")
            self.authenticate()
        elif kwargs.get("token"):
            self.token = kwargs.get("token")

        # set the interval and sync directory
        self.interval = kwargs.get("interval", 5)
        self.model_dir = kwargs.get("model_dir", "/tmp/")

        # start the sync
        self.model_sync = threading.Thread(target=self.fetch_and_sync_models)
        self.model_sync.start()

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
        if data:
            self.token = data.get("token")

    def get_token(self):
        return self.token

    def fetch_model_file(self, model):
        unique_id = model.get("unique_id")
        if unique_id:
            filename = "{}.fbz".format(unique_id)
            local_storage_path = os.path.join(self.model_dir, filename)
            with requests.get(
                self.ENDPOINTS.get("download_model"),
                stream=True,
                headers={"Authorization": "Token {}".format(self.token)},
                params={"unique_id": unique_id},
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

    def my_models(self, **kwargs):
        data = self.query(
            "get",
            url=self.ENDPOINTS.get("my_models"),
            headers={"Authorization": "Token {}".format(self.token)},
            params=dict(kwargs, format="json"),
        )
        return data

    def get_model(self, unique_id):
        data = self.query(
            "get",
            url="{}/{}".format(self.ENDPOINTS.get("my_models"), unique_id),
            headers={"Authorization": "Token {}".format(self.token)},
            params={"format": "json"},
        )
        return data

    def sync_model(self, unique_id):
        if not unique_id in self.models_to_sync:
            self.models_to_sync.append(unique_id)

    def unsync_model(self, unique_id):
        if unique_id in self.models_to_sync:
            self.models_to_sync.remove(unique_id)

    def fetch_and_sync_models(self):
        last_sync = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        while True:
            try:
                m = ",".join(self.models_to_sync)
                q = {
                    "unique_id__in": m,
                    "updated_at__gte": last_sync,
                }

                models = self.my_models(**q)
                if models and len(models) > 0:
                    for model in models:
                        self.fetch_model_file(model)
                    last_sync = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

            except Exception as e:
                pass
                # handle bad model sync

            time.sleep(self.interval)
