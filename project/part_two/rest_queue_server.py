import json
import uuid
from flask import Flask, request
from collections import deque

app = Flask(__name__)

messages = deque()


@app.route("/add_message", methods=["POST"])
def add_message():
    message = request.form["message"]
    return_string = "Message is successfully added to queue."
    message = json.loads(message)
    expected_keys = [
        "from_format",
        "to_format",
        "key",
        "bucket",
        "request_id",
    ]
    if type(message) is not dict:
        return_string = "Invalid type for message, expecting type 'dict'"
    elif all(key in message.keys() for key in expected_keys) is False:
        return_string = "Invalid keys for message."
    else:
        return_string = "Successfully added message to queue."
        # add attributes to be consistent with SQS.Message
        # Could be used to add keep message until requested to delete feature
        message['receipt_handle'] = str(uuid.uuid1())
        message['message_id'] = str(uuid.uuid1())
        messages.append(message)
    return return_string


@app.route("/get_message", methods=["GET"])
def get_message():
    message = None
    try:
        message = messages.popleft()
    except IndexError:
        return json.dumps({"empty": True})
    return json.dumps(message)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
