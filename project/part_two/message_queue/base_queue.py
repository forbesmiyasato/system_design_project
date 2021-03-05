class MessageQueue:
    def send_message(self, message):
        """
        Delivers a message to the specified queue.
        Message format: {
            "from_format": ,
            "to_format": ,
            "key": ,
            "bucket": ,
        }
        """
        expected_keys = [
            "from_format",
            "to_format",
            "key",
            "bucket", 
            "request_id",
        ]

        if type(message) is not dict:
            raise ValueError("Invalid type for message, expecting type 'dict'")
        elif all(key in message.keys() for key in expected_keys) is False:
            raise ValueError("Invalid keys for message.")

    def receive_message(self):
        """
        fetch a message from the specified queue.
        """
        pass
