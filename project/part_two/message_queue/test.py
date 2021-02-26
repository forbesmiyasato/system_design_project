from rest_queue import RestQueue

queue = RestQueue()

try:
    queue.send_message(
        {"from_format": "1", "to_format": "2", "key": "3", "bucket": "4"}
    )
except ValueError:
    print("error")
