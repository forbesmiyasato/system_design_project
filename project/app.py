import boto3
import json
from flask import Flask, request
from model import Model

app = Flask(__name__)
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='tasks.fifo')

def split_s3_path(s3_path):
    # this method is from stackoverflow
    path_parts=s3_path.replace("s3://","").split("/")
    bucket=path_parts.pop(0)
    key="/".join(path_parts)
    return bucket, key


@app.route('/transform', methods=['POST'])
def transform():
    model = Model()
    from_format = request.args.get('from_format')
    to_format = request.args.get('to_format')
    file_path = request.args.get('filename')

    bucket, key = split_s3_path(file_path)
    print(queue.url)
    message = {
	"from_format": from_format,
	"to_format": to_format,
	"key": key,
        "bucket": bucket
	}
    print(message)
    try:
        response = queue.send_message(MessageBody=json.dumps(message), MessageGroupId="tasks")
        response_id = response.get('MessageId')
        request_id_inserted = model.post_request(response_id, "Created conversion request", 1)
        return f'Received transform request for {filename} from {from_format} to {to_format}. Your request ID is {response_id if request_id_inserted else "ERROR"}'
    except:
        return "Failed to create conversion request"


@app.route('/status', methods=['GET'])
def get_status():
    model = Model()
    request_id = request.args.get('request_id')
    error, status = model.get_request(request_id)

    return status['request_status'] if not error else status 


@app.route('/update', methods=['POST'])
def update_status():
    model = Model()
    request_id = request.form['request_id']
    status = request.form['status']
    code = request.form['code']
    model.update_request(request_id, status, code)
    return "Updated"


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)
