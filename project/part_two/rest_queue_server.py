import json
from flask import Flask, request
from collections import deque

app = Flask(__name__)

messages = deque()


@app.route("/add_message", method=["POST"])
def add_message():
    message = request.form["message"]
    return_string = "Message is successfully added to queue."
    message = json.load(message)
    if type(message) is not dict:
        return_string = "Invalid type for message, expecting type 'dict'"
    elif {
        "from_format",
        "to_format",
        "key",
        "bucket, request_id",
    } != message.keys():
        return_string = "Invalid keys for message."
    messages.append(message)
    print(messages)
    return return_string


@app.route("/get_message", method=["GET"])
def get_message():
    message = None
    try:
        message = messages.popleft()
    except IndexError:
        return "No messages in queue"
    return json.dump(message)


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)
