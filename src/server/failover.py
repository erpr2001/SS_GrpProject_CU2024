active_server = "primary"
standby_server = "secondary"

def check_server():
    global active_server
    try:
        # Simulate primary server check
        print("Checking primary server...")
        # Raise an error to simulate primary failure
        raise ConnectionError("Primary server down")
    except ConnectionError:
        print("Failover to standby server.")
        active_server = standby_server

check_server()
print("Active server:", active_server)
