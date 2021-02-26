from message_queue import MessageQueue


class RestQueue(MessageQueue):
    def __init__(self):
        pass

    def send_message(self, message):
        super(RestQueue, self).send_message(message)
        pass

    def receive_message(self, message):
        pass
