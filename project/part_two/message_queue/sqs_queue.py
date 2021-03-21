import boto3
import json
from .base_queue import MessageQueue


class SQS(MessageQueue):
    def __init__(self):
        self.resource = boto3.resource("sqs")
        self.queue = self.resource.get_queue_by_name(QueueName="tasks.fifo")

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
        super(SQS, self).send_message(message)
        self.queue.send_message(
            MessageBody=json.dumps(message), MessageGroupId="tasks"
        )

    def receive_message(self):
        """
        Fetch a message from the specified queue.

        Returns
        -------
        A message as a dictionary with attributes: from_format, to_format
        key, bucket, request_id, receipt_handle, message_id
        """
        messages = self.queue.receive_messages(
            MaxNumberOfMessages=1, WaitTimeSeconds=20
        )
        data = None

        if messages:
            message = messages[0]
            data = json.loads(message.body)
            data['receipt_handle'] = message.receipt_handle
            data['message_id'] = message.message_id
        return data

    def delete_message(self, receipt_handle, message_id):
        """
        Delete a message from the queue using its receipt_handle

        Parameters
        ----------
        receipt_handle : string
            The receipt handle for the message to be deleted

        message_id : string
            An identifier for this particular receipt handle
        """
        print(receipt_handle)
        self.queue.delete_messages(
            Entries=[
                {
                    'Id': message_id,
                    'ReceiptHandle': receipt_handle
                },
            ]
        )
        pass