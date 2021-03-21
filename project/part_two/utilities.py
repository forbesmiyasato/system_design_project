def split_s3_path(s3_path):
    """
    Splits the s3_path into bucket and key

    Parameters
    ----------
    s3_path : string
        The full s3 path to be split

    Returns
    -------
    The s3_path's bucket and key
    """
    # Copied from stackoverflow
    # retrieve bucket name and object key from s3_path
    path_parts = s3_path.replace("s3://", "").split("/")
    bucket = path_parts.pop(0)
    key = "/".join(path_parts)
    return bucket, key


def retriable_request(request, *args, **kwargs):
    """
    Network requests that are automatically retried upon failure with the 
    exponential backoff strategy

    Parameters
    ----------
    request : callable
        The network request to be invoked
    
    args : arguments
        The network requests arguments
    
    kwargs : keyword arguments
        The network requests keyword arguments. May contain the user defined
        retry count
    
    Returns
    -------
    The response from the network request is successful

    Raises
    ------
    ValueError : If the request passed in is not callable

    Exception : If the network request failed after retrying
    """
    if callable(request) is False:
        raise ValueError('The network request is not callable')

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
