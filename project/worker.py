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

            try:
                file_obj = s3.get_object(Bucket=bucket_name, Key=object_key)
            except:
                #handle exception from getting file
                pass

            file_body = file_obj['Body']
            content = file_body.read().decode('utf-8-sig')
            body = None
            valid_message = True

            if from_format == 'csv' and to_format == 'json':
                csv_reader = csv.DictReader(io.StringIO(content))
                json_data = json.dumps(list(csv_reader))
                body = str(json.dumps(json_data))
            elif from_format == 'json' and to_format == 'csv':
                json_data = json.loads(content) #first load reformats the json data into proper string format
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
                body = in_memory_file.getvalue()
            else:
                valid_message = False

            if valid_message:
                new_object_key = filename + '.' + to_format
                try:
                    s3.put_object(Body=body, Bucket=bucket_name, Key=new_object_key)
                except:
                    continue
                s3.delete_object(Bucket=bucket_name, Key=object_key)

            message.delete() #delete message if valid or invalid?

if __name__ == '__main__':
    handleTask()
