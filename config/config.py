import os

# Server settings
SERVER_HOST = "localhost"  # The server's IP or hostname
SERVER_PORT = 65432        # The port for server communication

# SSL settings
CERT_FILE = "certificates/server.crt"
KEY_FILE = "certificates/server.key"

# Encryption settings (AES and RSA)
AES_KEY_SIZE = 256  # Bits
RSA_KEY_SIZE = 2048 # Bits
