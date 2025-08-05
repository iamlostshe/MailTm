import time
from threading import Thread

from .consts import BASE_URL


class Listen:
    def __init__(self) -> None:
        self.listen = False
        self.message_ids = []

    def message_list(self) -> list:
        url = f"{BASE_URL}messages"
        headers = {"Authorization": "Bearer " + self.token}
        response = self.session.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        return [
            msg
            for i, msg in enumerate(data["hydra:member"])
            if data["hydra:member"][i]["id"] not in self.message_ids
        ]

    def message(self, idx: str) -> dict | list:
        url = f"{BASE_URL}messages/{idx}"
        headers = {"Authorization": "Bearer " + self.token}
        response = self.session.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def run(self) -> None:
        while self.listen:
            for message in self.message_list():
                self.message_ids.append(message["id"])
                self.listener(self.message(message["id"]))

            time.sleep(self.interval)

    def start(self, listener, interval: int = 3):
        if self.listen:
            self.stop()

        self.listener = listener
        self.interval = interval
        self.listen = True

        # Start listening thread
        self.thread = Thread(target=self.run)
        self.thread.start()

    def stop(self) -> None:
        self.listen = False
        self.thread.join()
