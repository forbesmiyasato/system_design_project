import boto3
import json
import csv
import io
import pandas as pd

bucket_name = "aws-system-design"
sqs = boto3.resource('sqs')
s3 = boto3.client('s3')

queue = sqs.get_queue_by_name(QueueName='tasks.fifo')

def handleTask():
    while True:
        messages = queue.receive_messages()
        if messages:
            message = messages[0]
            request_id = message.message_id
            print(f"received request {request_id}")
            data = json.loads(message.body)
            from_format = data['from_format']
            to_format = data['to_format']
            filename = data['filename']
            object_key = filename + '.' + from_format
            file_obj = s3.get_object(Bucket=bucket_name, Key=object_key)
            file_body = file_obj['Body']
            content = file_body.read().decode('utf-8-sig')
            print(content)
            print(type(content))
            csv_reader = csv.DictReader(io.StringIO(content))
            json_data = json.dumps(list(csv_reader))
            print(json_data)
            object_key = filename + '.' + to_format
            #s3.put_object(Body=str(json.dumps(json_data)), Bucket=bucket_name, Key=object_key)
            #message.delete()

if __name__ == '__main__':
    handleTask()
