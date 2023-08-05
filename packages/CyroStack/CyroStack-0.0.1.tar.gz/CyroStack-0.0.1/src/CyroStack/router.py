from CyroStack.request import Request
from CyroStack.response import Response
import parse

class Router:
    def __init__(self) -> None:
        """
        Initialize the router with an empty list of routes
        """
        self.routes = []

    def add_route(self, path: str, handler, methods: list) -> None:
        """
        Add a route to the router
        
        :param path: The path template to match the route on
        :param handler: The function to handle the route
        :param methods: The list of allowed methods for the route
        """
        self.routes.append({'template': path, 'handler': handler, 'methods': methods})

    def handle_request(self, request: Request) -> Response:
        """
        Handle a single request by matching it to a registered route

        :param request: The Request object
        """
        path = request.url
        response = Response()
        for route in self.routes:
            try:
                result = parse.parse(route['template'], path)
                if request.method not in route["methods"]:
                    return None
                route['handler'](request, response, **(result.named if result else {}))
                return response
            except TypeError as e:
                print(e)
                pass
        response.status = "404 Not Found"
        return response