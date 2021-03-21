class MessageQueue:
    """
    A class used as an abstraction of queue operations

    Methods
    -------
    send_message(message)
        Sends a message to the queue

    receive_message()
        Get a message from the queue

    delete_message(receipt_handle, message_id)
        Delete the message from the queue with its receipt handle
    """

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
        Fetch a message from the specified queue.

        Returns
        -------
        A message as a dictionary with attributes: from_format, to_format
        key, bucket, request_id, receipt_handle, message_id
        """
        pass

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
        pass