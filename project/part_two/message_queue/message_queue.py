class MessageQueue:
    def send_message(self, message):
        print("parent")
        """
        Delivers a message to the specified queue.
        Message format: {
            "from_format": ,
            "to_format": ,
            "key": ,
            "bucket": ,
        }
        """
        if type(message) is not dict:
            raise ValueError("Invalid type for message, expecting type 'dict'")
        elif {"from_format", "to_format", "key", "bucket"} != message.keys():
            raise ValueError("Invalid keys for message.")
        pass

    def receive_message(self):
        """
        fetch a message from the specified queue.
        """
        pass
