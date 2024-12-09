import socket
import ssl
import threading
from src.logs.logging import secure_logger  # Import the secure logger

# Load SSL certificates
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="C:/Users/Spectre/OneDrive/Desktop/Carleton/Fall24/Secure Systems Engineering/CityServe/certificates/server.crt", 
                        keyfile="C:/Users/Spectre/OneDrive/Desktop/Carleton/Fall24/Secure Systems Engineering/CityServe/certificates/server.key")

# Set up server
def start_server():
    try:
        # Log server start
        secure_logger.log_event(
            event_type='SERVER_START',
            message='Server started successfully and is listening on port 8443.',
            severity='INFO',
            component='Server'
        )
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        secure_socket = context.wrap_socket(server_socket, server_side=True)
        secure_socket.bind(('localhost', 8443))
        secure_socket.listen(5)
        print("Server is listening...")

        while True:
            client_conn, client_addr = secure_socket.accept()
            print(f"Connected to {client_addr}")
            
            # Log client connection
            secure_logger.log_event(
                event_type='CLIENT_CONNECTED',
                message=f'Client connected from {client_addr}',
                severity='INFO',
                component='Server'
            )
            
            threading.Thread(target=handle_client, args=(client_conn,)).start()

    except Exception as e:
        # Log any error while starting the server
        secure_logger.log_event(
            event_type='SERVER_ERROR',
            message=f"Error starting server: {e}",
            severity='ERROR',
            component='Server'
        )
        raise  # Re-raise the exception

def handle_client(conn):
    try:
        data = conn.recv(1024)
        print(f"Received encrypted data: {data}")
        
        # Log received data (note that this is still encrypted, so you may need to decrypt if required)
        secure_logger.log_event(
            event_type='DATA_RECEIVED',
            message=f"Received encrypted data: {data}",
            severity='INFO',
            component='Server'
        )
        
        # Process data here (decrypt if needed)
        conn.sendall(b"Message received securely.")
        
        # Log data sent
        secure_logger.log_event(
            event_type='DATA_SENT',
            message="Sent confirmation: 'Message received securely.'",
            severity='INFO',
            component='Server'
        )
        
    except Exception as e:
        # Log any errors during client handling
        secure_logger.log_event(
            event_type='CLIENT_ERROR',
            message=f"Error handling client data: {e}",
            severity='ERROR',
            component='Server'
        )
    finally:
        conn.close()
        # Log client disconnection
        secure_logger.log_event(
            event_type='CLIENT_DISCONNECTED',
            message='Client disconnected.',
            severity='INFO',
            component='Server'
        )

# Start the server
start_server()
