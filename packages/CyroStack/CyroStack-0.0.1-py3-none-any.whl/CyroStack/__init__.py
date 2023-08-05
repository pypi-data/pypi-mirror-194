import logging
import os
from queue import Queue
import socket
import sys
from threading import Thread, Semaphore
from typing import List

from CyroStack.response import Response
from .console import Console, Logger
from .request import Request
from .router import Router

class App:
    def __init__(self, port: int, max_connections: int = 5) -> None:
        """
        Initialize the app with the given port and maximum number of connections

        :param port: Port to listen on
        :param max_connections: Maximum number of simultaneous connections
        """
        self.port = port
        self.max_connections = max_connections
        self.semaphore = Semaphore(value=max_connections)
        self.router = Router()
        self.plugins = []
        self.controlQueue = Queue()
        self.console = Console(self, False)
        consoleThread = Thread(target=self.console.run)
        consoleThread.start()
        self.logger = Logger(self.console)
        self.control_thread = Thread(target=self.control, args=(self.controlQueue,))
        self.control_thread.start()

    def control(self, controlQueue: Queue) -> None:
        while True:
            command = controlQueue.get()
            if command == "start":
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_socket.bind(("", self.port))
                self.server_socket.listen(self.max_connections)
                serverThread = Thread(target=self.start)
                serverThread.start()
            elif command == "stop":
                print("Stopping server")
                self.stop()
                serverThread.join()
            elif command == "exit":
                sys.exit()

    def route(self, path: str, methods: List[str] = ["GET"]) -> callable:
        """
        Decorator for adding a route to the app

        :param path: Path to match the route on
        :param methods: List of allowed methods for the route
        """
        def decorator(handler):
            self.router.add_route(path, handler, methods)
            return handler
        return decorator

    def start(self) -> None:
        """
        Start the server and begin listening for connections
        """
        self.logger.log(logging.INFO, f"Server started on port {self.port}")
        while self.server_socket.fileno() != -1:
            try:
                try:
                    (client_socket, client_address) = self.server_socket.accept()
                except OSError:
                    if self.server_socket.fileno() == -1:
                        break
                self.semaphore.acquire()
                Thread(target=self.handle_request, args=(client_socket,)).start()
            except Exception as e:
                self.logger.log(f"Error: {e}")
                self.semaphore.release()
                client_socket.close()

    def stop(self) -> None:
        """
        Stop the server and close the socket
        """
        self.logger.log(logging.WARNING, "Server stopped")
        self.server_socket.close()

    def pause(self) -> None:
        """
        Pause the server and stop listening for connections
        """
        self.server_socket.shutdown(socket.SHUT_RDWR)

    def resume(self) -> None:
        """
        Resume the server and begin listening for connections
        """
        self.server_socket.listen(self.max_connections)

    def reload(self) -> None:
        """
        Reload the server
        """
        command = sys.executable + " " + " ".join(sys.argv)
        os.system(command)


    def handle_request(self, client_socket: socket.socket) -> None:
        """
        Handle a single request from a client

        :param client_socket: socket object for the client connection
        """
        try:
            req_string = client_socket.recv(1024).decode()
            request = Request(client_socket.recv(1024).decode())
            skip_router, response = False, None
            for plugin in self.plugins:
                skip_router, response = plugin.on_request(request)
                if skip_router:
                    break
            if not skip_router:
                response = self.router.handle_request(request)
            for plugin in self.plugins:
                plugin.on_response(request, response)
            client_socket.sendall(response.compile())
            client_socket.close()
            self.semaphore.release()
        except Exception as e:
            response = Response()
            response.status = 500
            response.body = f"Internal Server Error: {e}"
            client_socket.sendall(response.compile())
            self.logger.exception(e)
            client_socket.close()
            self.semaphore.release()
            self.logger.exception(e)