class MessageQueue:
    """
    A class used as an abstraction of queue operations

    Methods
    -------
    send_message(message)
        Sends a message to the queue

    receive_message()
        Get a message from the queue
    """

    def send_message(self, message):
        """Sends a message to the queue

        Parameters
        ----------
        message : int
            The id of the request record we want to retrive from the DB

        Returns
        ------
        True (has error) and error message if can't retrieve the
        request from DB, and False (has no error) and request json if retrieved
        request from DB
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
