class Request:
    def __init__(self, request_string: str) -> None:
        """
        Initialize a new request object from the given request string

        :param request_string: String representing the entire request
        """
        try:
            request_lines = request_string.split("\r\n")
            request_line = request_lines[0]
            self.method, self.url, self.protocol = request_line.split()
            self.headers = {}
            for line in request_lines[1:]:
                if not line:
                    break
                name, value = line.split(": ")
                self.headers[name] = value
            self.body = "\r\n".join(request_lines[len(self.headers) + 2:])
        except Exception as e:
            pass