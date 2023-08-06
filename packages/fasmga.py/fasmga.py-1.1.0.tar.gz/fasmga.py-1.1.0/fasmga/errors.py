class HTTPException(Exception):
    def __init__(self, request, data):
        msg = f"HTTP request returned {request.status} status code."
        self.request = request

        for k, v in data.items():
            setattr(self, k, v)
            msg += f"\nIn {k}: {v}"
        
        return super().__init__(msg)


class TooManyRequests(HTTPException):
    pass


class BadRequest(HTTPException):
    pass
