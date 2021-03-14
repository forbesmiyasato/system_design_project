queue_type = "sqs"

if queue_type == "rest":
    from .rest_queue import RestQueue as queue
elif queue_type == "sqs":
    from .sqs_queue import SQS as queue
else:
    raise ValueError("No appropriate message queue configured.")

backend_queue = queue()


def get_model():
    return backend_queue
