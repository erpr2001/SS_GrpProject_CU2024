import threading
import time

def send_heartbeat(node_id):
    while True:
        print(f"Sending heartbeat from Node {node_id}")
        time.sleep(5)  # Send a heartbeat every 5 seconds

# Start heartbeats for multiple nodes
threading.Thread(target=send_heartbeat, args=(1,)).start()
threading.Thread(target=send_heartbeat, args=(2,)).start()
