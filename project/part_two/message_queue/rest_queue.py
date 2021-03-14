import requests
import json
from .base_queue import MessageQueue


class RestQueue(MessageQueue):
    def __init__(self):
        self.host = "http://127.0.0.1:5000/"

    def send_message(self, message):
        super(RestQueue, self).send_message(message)
        url = self.host + "add_message"
        requests.post(url, data={"message": json.dumps(message)})

    def receive_message(self):
        url = self.host + "get_message"
        response = requests.get(url)
        if response is None or "empty" in response.json():
            return None
        return response.json()

    def delete_message(self, receipt_handle):
        pass