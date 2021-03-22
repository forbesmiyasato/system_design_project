import boto3
import json
import uuid

import database_model
import message_queue

from flask import Flask, request
from .utilities import split_s3_path

app = Flask(__name__)
model = database_model.get_model()
s3 = boto3.client("s3")


@app.route("/transform", methods=["POST"])
def transform():
    """
    Endpoint to make a conversion request

    Adds the conversion request to the queue

    Returns
    -------
    Request ID if conversion request is accepted; Error message if the 
    conversion request fails
    """
    from_format = request.args.get("from_format")
    to_format = request.args.get("to_format")
    file_path = request.args.get("filename")

    bucket, key = split_s3_path(file_path)
    request_id = str(uuid.uuid1())
    message = {
        "from_format": from_format,
        "to_format": to_format,
        "key": key,
        "bucket": bucket,
        "request_id": request_id,
    }
    try:
        queue = message_queue.get_model()
        queue.send_message(message)

        request_id_inserted = model.post_request(
            request_id, "Created conversion request", 1
        )  # returns false if couldn't insert request id into DB

        return f'Received transform request for {file_path} from {from_format} \
            to {to_format}. Your request ID is \
            {request_id if request_id_inserted else "undefined"}'
    except Exception as e:
        return f"Failed to create conversion request - {e}"


@app.route("/status", methods=["GET"])
def get_status():
    """
    Endpoint to check the conversion progress

    Returns
    -------
    The conversion progress of the task or error message if fetching the 
    conversion progress failed
    """
    request_id = request.args.get("request_id")
    error, status = model.get_request(request_id)
    if not error:
        status["code"] = int(status["code"])  # serialize the Decimal object
    return json.dumps(status) if not error else status


@app.route("/update", methods=["POST"])
def update_status():
    """
    Endpoint to update the conversion progress

    Returns
    -------
    Message to indicate update status
    """
    request_id = request.form["request_id"]
    status = request.form["status"]
    code = request.form["code"]
    # TODO if update failed
    model.update_request(request_id, status, code)
    return "Updated"


@app.route("/file", methods=["GET"])
def get_file():
    """
    Endpoint to fetch the content of a file using the filename

    Returns
    -------
    Returns the content of the file if fetched successfully. Otherwise,
    error message returned.

    Raises
    ------
    Exception : if error occurs when retrieving file from s3
    """    
    
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
