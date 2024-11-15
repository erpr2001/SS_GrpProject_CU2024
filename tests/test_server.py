import unittest
import socket
import ssl
from src.server.server import start_server
import threading
import time 
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


class TestServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Start the server in a separate thread before running the tests"""
        cls.server_thread = threading.Thread(target=start_server, daemon=True)
        cls.server_thread.start()
        
        # Give the server some time to start up
        time.sleep(1)  # Adjust the sleep time based on how long the server needs to start


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
