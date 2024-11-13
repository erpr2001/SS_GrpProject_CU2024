import unittest
import socket
import ssl
# import sys
# import os
from src.client.client import start_client

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestClient(unittest.TestCase):
    def test_client_connection(self):
        # Simulate the client attempting to connect to the server
        try:
            # Attempt to start the client and connect to the server
            start_client()
        except Exception as e:
            self.fail(f"Client connection failed: {e}")

if __name__ == "__main__":
    unittest.main()
