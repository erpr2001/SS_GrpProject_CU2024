import socket
import ssl

def start_client():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations("C:/Users/Spectre/OneDrive/Desktop/Carleton/Fall24/Secure Systems Engineering/CityServe/certificates/server.crt")

    client_socket = socket.create_connection(('localhost', 8443))
    secure_client_socket = context.wrap_socket(client_socket, server_hostname="localhost")

    secure_client_socket.sendall(b"Hello, secure server!")
    response = secure_client_socket.recv(1024)
    print("Server response:", response)

    secure_client_socket.close()