import unittest
import socket
import ssl
from src.server.server import start_server

class TestServer(unittest.TestCase):
    def test_server_connection(self):
        # Simulate a client connecting to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        secure_socket = context.wrap_socket(client_socket, server_hostname="localhost")

        try:
            secure_socket.connect(('localhost', 65432))
            secure_socket.sendall(b'Hello Server')
            response = secure_socket.recv(1024)
            self.assertEqual(response, b"Message received")
        finally:
            secure_socket.close()

if __name__ == "__main__":
    unittest.main()
