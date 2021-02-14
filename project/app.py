import boto3
from flask import Flask

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


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)
