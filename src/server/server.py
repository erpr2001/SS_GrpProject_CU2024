import socket
import ssl
import threading

# Load SSL certificates
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="C:/Users/Spectre/OneDrive/Desktop/Carleton/Fall24/Secure Systems Engineering/CityServe/certificates/server.crt", keyfile="C:/Users/Spectre/OneDrive/Desktop/Carleton/Fall24/Secure Systems Engineering/CityServe/certificates/server.key")

# Set up server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secure_socket = context.wrap_socket(server_socket, server_side=True)
    secure_socket.bind(('localhost', 8443))
    secure_socket.listen(5)
    print("Server is listening...")

    while True:
        client_conn, client_addr = secure_socket.accept()
        print(f"Connected to {client_addr}")
        threading.Thread(target=handle_client, args=(client_conn,)).start()

def handle_client(conn):
    try:
        data = conn.recv(1024)
        print(f"Received encrypted data: {data}")
        # Process data here (decrypt if needed)
        conn.sendall(b"Message received securely.")
    finally:
        conn.close()

start_server()
