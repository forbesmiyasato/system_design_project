import boto3
import json
import csv
import io
import requests
import time

sqs = boto3.resource('sqs')
s3 = boto3.client('s3')

queue = sqs.get_queue_by_name(QueueName='tasks.fifo')

def get_json(content):
    csv_reader = csv.DictReader(io.StringIO(content))
    json_data = json.dumps(list(csv_reader))
    return str(json.dumps(json_data))


def get_csv(content):
    json_data = json.loads(content) # first load reformats the json data into proper string format
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


def handle_task():
    while True:
        messages = queue.receive_messages(MaxNumberOfMessages=1)
        if messages:
            time.sleep(10) # pretend like it takes longer to receive a message
            message = messages[0]
            request_id = message.message_id
            print(f"received request {request_id}")
            url = 'http://52.27.158.127:80/update'
            requests.post(url, data={'request_id': request_id, 'status': 'Processing request', 'code': '2'})
            data = json.loads(message.body)
            from_format = data['from_format']
            to_format = data['to_format']
            object_name = data['key']
            bucket_name = data['bucket']
            object_key = object_name + '.' + from_format
            csv_to_json = from_format == 'csv' and to_format == 'json'
            json_to_csv = from_format == 'json' and to_format == 'csv'

            if not csv_to_json and not json_to_csv:
                # invalid message
                print("invalid message format")
                message.delete()
                continue

            try:
                file_obj = s3.get_object(Bucket=bucket_name, Key=object_key)
            except:
                # handle exception from getting file
                continue

            file_body = file_obj['Body']
            content = file_body.read().decode('utf-8-sig')
            body = None

            if csv_to_json:
                body = get_json(content)
            elif json_to_csv:
                body = get_csv(content)

            time.sleep(10) # pretend like it takes longer for task to process
            new_object_key = object_name + '.' + to_format
            try:
                s3.put_object(Body=body, Bucket=bucket_name, Key=new_object_key)
            except:
                # handle exception from uploading file
                continue
            s3.delete_object(Bucket=bucket_name, Key=object_key)
            message.delete()
            requests.post(url, data={'request_id': request_id, 'status': 'Conversion completed', 'code': '3'})
            print(f'finished request {request_id}')

if __name__ == '__main__':
    print("Worker running")
    handle_task()
