import boto3
import json
import csv
import io
import requests
import time
from multiprocessing import Process

import message_queue

queue = message_queue.get_model()

s3 = boto3.client("s3")

url_host = "http://34.208.159.15:80/"


def convert_from_csv_to_json(content):
    # Converts the csv string into json string
    csv_reader = csv.DictReader(io.StringIO(content))
    json_data = json.dumps(list(csv_reader))
    return str(json.dumps(json_data))


def convert_from_json_to_csv(content):
    # Converts the json string into csv string
    # first load reformats the json data into proper string format
    json_data = json.loads(content)
    json_data = json.loads(json_data)
    in_memory_file = io.StringIO()
    csv_writer = csv.writer(in_memory_file)
    header = True
    for row in json_data:
        if header:
            header = row.keys()
            csv_writer.writerow(header)
            header = False
        csv_writer.writerow(row.values())
    return in_memory_file.getvalue()


def handle_task(message):
    time.sleep(10)  # pretend like it takes longer to receive a message
    request_id = message["request_id"]
    print(f"received request {request_id}")
    update_url = url_host + "update"
    requests.post(
        update_url,
        data={
            "request_id": request_id,
            "status": "Processing request",
            "code": "2",
        },
    )
    from_format = message["from_format"]
    to_format = message["to_format"]
    object_name = message["key"]
    bucket_name = message["bucket"]
    object_key = object_name + "." + from_format
    csv_to_json = from_format == "csv" and to_format == "json"
    json_to_csv = from_format == "json" and to_format == "csv"

    if not csv_to_json and not json_to_csv:
        # invalid message
        print("invalid message format")
        message.delete()
    try:
        file_obj = s3.get_object(Bucket=bucket_name, Key=object_key)
    except Exception:
        # TODO handle exception from getting file
        pass

    file_body = file_obj["Body"]
    content = file_body.read().decode("utf-8-sig")
    body = None

    if csv_to_json:
        body = convert_from_csv_to_json(content)
    elif json_to_csv:
        body = convert_from_json_to_csv(content)

    time.sleep(10)  # pretend like it takes longer for task to process
    new_object_key = object_name + "." + to_format
    try:
        s3.put_object(Body=body, Bucket=bucket_name, Key=new_object_key)
    except Exception:
        # TODO handle exception from uploading file
        pass
    s3.delete_object(Bucket=bucket_name, Key=object_key)
    message.delete()
    requests.post(
        update_url,
        data={
            "request_id": request_id,
            "status": "Conversion completed",
            "code": "3",
        },
    )
    print(f"finished request {request_id}")


if __name__ == "__main__":
    print("Worker running")
    """Receives messages from the queue and processes the conversions.

    Polls task messages from the queue in an infinite loop.

    If there is a task message in the queue, check if the task is already 
    being processed. If it is, discard the message. If it isn't, spawn a new 
    process to handle the task and continue polling for messages.
    """
    while True:
        message = queue.receive_message()
        print(message)
        if message:
            get_url = url_host + "status"
            res = requests.get(
                get_url, params={"request_id": message["request_id"]}
            )
            print(res)
            print(res.json())
            if res == 1:  # 1 for not being processed yet
                p = Process(target=handle_task, args=(message,))
                p.start()
        time.sleep(1)
