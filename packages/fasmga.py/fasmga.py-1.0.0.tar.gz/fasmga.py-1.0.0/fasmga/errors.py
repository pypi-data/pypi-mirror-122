class HTTPException(Exception):
    def __init__(self, status, data):
        msg = f"HTTP request returned {status} status code."

        for k, v in data.items():
            setattr(self, k, v)
            msg += f"\nIn {k}: {v}"


class TooManyRequests(HTTPException):
    pass


class BadRequest(HTTPException):
    pass
