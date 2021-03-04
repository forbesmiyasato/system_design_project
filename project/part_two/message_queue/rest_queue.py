import requests
import json
from .base_queue import MessageQueue


class RestQueue(MessageQueue):
    def __init__(self):
        self.host = "localhost:5000/"

    def send_message(self, message):
        super(RestQueue, self).send_message(message)
        url = self.host + "add_message"
        requests.post(url, data={json.dump(message)})

    def receive_message(self):
        url = self.host + "get_message"
        response = requests.get(url)
        print(response.json())
        response_json = response.json()
        return response.json()
