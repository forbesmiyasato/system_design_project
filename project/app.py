import boto3
import json
from flask import Flask, request

app = Flask(__name__)
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='tasks.fifo')

@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/transform', methods=['POST'])
def transform():
    from_format = request.args.get('from_format')
    to_format = request.args.get('to_format')
    filename = request.args.get('filename')
    print(queue.url)
    message = {
	"from_format": from_format,
	"to_format": to_format,
	"filename": filename
	}

    response = queue.send_message(MessageBody=json.dumps(message), MessageGroupId="tasks")
    response_id = response.get('MessageId')
    return f'Received transform request for {filename} from {from_format} to {to_format}. Your request ID is {response_id}'

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)
