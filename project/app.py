import boto3
import json
from flask import Flask, request
from model import Model

app = Flask(__name__)
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='tasks.fifo')

@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/transform', methods=['POST'])
def transform():
    model = Model()
    from_format = request.args.get('from_format')
    to_format = request.args.get('to_format')
    filename = request.args.get('filename')
    print(queue.url)
    message = {
	"from_format": from_format,
	"to_format": to_format,
	"filename": filename
	}

    try:
        response = queue.send_message(MessageBody=json.dumps(message), MessageGroupId="tasks")
        response_id = response.get('MessageId')
        request_id_inserted = model.post_request(response_id, "Created conversion request")
        return f'Received transform request for {filename} from {from_format} to {to_format}. Your request ID is {response_id if request_id_inserted else "ERROR"}'
    except:
        return "Failed to create conversion request"


@app.route('/status', methods=['GET'])
def get_status():
    model = Model()
    request_id = request.args.get('request_id')
    error, status = model.get_request(request_id)
    print(status)
    return status if not error else status 


@app.route('/update', methods=['POST'])
def update_status():
    model = Model()
    request_id = request.args.get('request_id')
    status = request.args.get('status')
    model.update_request(request_id, status)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)
