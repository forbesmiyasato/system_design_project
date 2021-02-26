import boto3
import json
from flask import Flask, request
from model import Model

app = Flask(__name__)
sqs = boto3.resource("sqs")
queue = sqs.get_queue_by_name(QueueName="tasks.fifo")
model = Model()  # is this a good practice?
s3 = boto3.client("s3")


def split_s3_path(s3_path):
    # Copied from stackoverflow
    # retrieve bucket name and object key from s3_path
    path_parts = s3_path.replace("s3://", "").split("/")
    bucket = path_parts.pop(0)
    key = "/".join(path_parts)
    return bucket, key


@app.route("/transform", methods=["POST"])
def transform():
    # Route for the user to make a conversion request
    # Adds the conversion request to the queue and returns the
    # user a request id
    from_format = request.args.get("from_format")
    to_format = request.args.get("to_format")
    file_path = request.args.get("filename")

    bucket, key = split_s3_path(file_path)
    print(queue.url)
    message = {
        "from_format": from_format,
        "to_format": to_format,
        "key": key,
        "bucket": bucket,
    }
    print(message)
    try:
        response = queue.send_message(
            MessageBody=json.dumps(message), MessageGroupId="tasks"
        )
        response_id = response.get("MessageId")
        request_id_inserted = model.post_request
        (response_id, "Created conversion request", 1)
        return f'Received transform request for {file_path} from {from_format} \
            to {to_format}. Your request ID is \
            {response_id if request_id_inserted else "undefined"}'
    except Exception as e:
        return f"Failed to create conversion request - {e}"


@app.route("/status", methods=["GET"])
def get_status():
    # Route for the user to check the conversion progress
    request_id = request.args.get("request_id")
    error, status = model.get_request(request_id)

    return status["request_status"] if not error else status


@app.route("/update", methods=["POST"])
def update_status():
    # Route for the worker to update the conversion progress
    request_id = request.form["request_id"]
    status = request.form["status"]
    code = request.form["code"]
    model.update_request(request_id, status, code)
    return "Updated"


@app.route("/file", methods=["GET"])
def get_file():
    # Route for the user to check the file's content
    path = request.args.get("filename")

    bucket_name, object_key = split_s3_path(path)

    try:
        file_obj = s3.get_object(Bucket=bucket_name, Key=object_key)
    except Exception:
        # handle exception from getting file
        return "Error occured when retrieving file from s3"

    file_body = file_obj["Body"]
    content = file_body.read().decode("utf-8-sig")
    return content


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8000)
