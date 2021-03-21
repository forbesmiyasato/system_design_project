import requests
import json
from .base_queue import MessageQueue


class RestQueue(MessageQueue):
    def __init__(self):
        self.host = "http://127.0.0.1:5000/"

    def send_message(self, message):
        """
        Sends a message to the queue

        Parameters
        ----------
        message : dict
            The message being sent to the queue

        Raises
        ------
        ValueError : if the message isn't a dict or missing keys
        """
        super(RestQueue, self).send_message(message)
        url = self.host + "add_message"
        requests.post(url, data={"message": json.dumps(message)})

    def receive_message(self):
        """
        Fetch a message from the specified queue.

        Returns
        -------
        A message as a dictionary with attributes: from_format, to_format
        key, bucket, request_id, receipt_handle, message_id
        """
        url = self.host + "get_message"
        response = requests.get(url)
        if response is None or "empty" in response.json():
            return None
        
        res_json = response.json()
        message = json.loads(res_json)
        return message

    def delete_message(self, receipt_handle, message_id):
        """
        Delete a message from the queue using its receipt_handle

        REST based queue doesn't have a message retention period, all
        messages are deleted upon receive. Hence, this method is empty

        Parameters
        ----------
        receipt_handle : string
            The receipt handle for the message to be deleted

        message_id : string
            An identifier for this particular receipt handle
        """
        pass