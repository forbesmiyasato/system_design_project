import json
from flask import Flask, request
from collections import deque

app = Flask(__name__)

messages = deque()


@app.route("/add_message", methods=["POST"])
def add_message():
    print("test")
    message = request.form["message"]
    print(message)
    return_string = "Message is successfully added to queue."
    message = json.loads(message)
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


@app.route("/get_message", methods=["GET"])
def get_message():
    message = None
    try:
        message = messages.popleft()
    except IndexError:
        return "No messages in queue"
    return json.dumps(message)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
