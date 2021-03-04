import time


def request(x):
    print(x)
    # raise ValueError('invalid')
    return add(*x)


def add(x, y, z, key_word):
    raise ValueError("invalid")
    return x + y + z + key_word


def retryable_request(request, *args, **kwargs):
    retry_count = kwargs.pop("retry", 5)
    retry_count = min(
        retry_count, 6
    )  # max retry count as 6, or else wait time could be too long
    wait_time = 0.5
    multiplier = 2
    for i in range(retry_count):
        print(wait_time)
        try:
            res = request(*args, **kwargs)
            return res
        except Exception as e:
            # rethrow exception on the last retry
            if i < retry_count - 1:
                print(f"fail - {i} - {e}")
            else:
                raise e
        time.sleep(wait_time)
        wait_time *= multiplier


res = None
try:
    res = retryable_request(add, 1, 2, 3, retry=2, key_word=5)
except ValueError as e:
    print(e)
