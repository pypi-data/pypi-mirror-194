class Response:
    def __init__(self, body=None, headers=None, status="200 OK") -> None:
        """
        Initialize a new Response instance
        
        :param body: The body of the response, defaults to None
        :param headers: The headers of the response, defaults to None
        :param status: The status code of the response, defaults to "200 OK"
        """
        self.body = body
        self.headers = headers or {}
        self.status = status

    def compile(self) -> bytes:
        """
        Compile the response into a bytes object
        """
        headers_str = "\r\n".join(f"{name}: {value}" for name, value in self.headers.items())
        return f"HTTP/1.1 {self.status}\r\n{headers_str}\r\n\r\n{self.body}".encode()