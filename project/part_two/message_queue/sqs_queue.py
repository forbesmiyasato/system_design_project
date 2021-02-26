import boto3
import json
from .base_queue import MessageQueue


class SQS(MessageQueue):
    def __init__(self):
        self.resource = boto3.resource("sqs")
        self.queue = self.resource.get_queue_by_name(QueueName="tasks.fifo")

    def send_message(self, message):
        super(SQS, self).send_message(message)
        self.queue.send_message(
            MessageBody=json.dumps(message), MessageGroupId="tasks"
        )

    def receive_message(self):
        messages = self.queue.receive_messages(
            MaxNumberOfMessages=1, WaitTimeSeconds=20
        )
        message = messages[0]
        data = json.loads(message.body)

        return data
