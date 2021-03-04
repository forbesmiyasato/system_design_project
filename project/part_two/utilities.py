def split_s3_path(s3_path):
    # Copied from stackoverflow
    # retrieve bucket name and object key from s3_path
    path_parts = s3_path.replace("s3://", "").split("/")
    bucket = path_parts.pop(0)
    key = "/".join(path_parts)
    return bucket, key


def retryable_request(request, *args, **kwargs):
    retry_count = kwargs.pop("retry", 5)
    retry_count = min(
        retry_count, 6
    )  # max retry count as 6, or else wait time could be too long
    wait_time = 0.5
    multiplier = 2
    for i in range(retry_count):
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
