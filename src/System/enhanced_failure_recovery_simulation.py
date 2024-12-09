
import os
import time
import base64
import threading
import matplotlib.pyplot as plt
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class SimulatedConnection:
    def __init__(self, sender, receiver):
        self.sender = sender
        self.receiver = receiver

    def send(self, encrypted_message):
        decrypted_message = base64.b64decode(encrypted_message).decode()
        if decrypted_message == "HEARTBEAT":
            self.receiver.receive_heartbeat(self.sender.node_id)
        else:
            self.receiver.handle_incoming_message(encrypted_message, self.sender.node_id)


class ConsensusNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
        self.shared_key = None
        self.peers = {}
        self.local_data = []
        self.is_leader = False
        self.leader_id = None
        self.heartbeat_interval = 5
        self.heartbeat_timeout = 15
        self.alive = True

    def get_public_key_pem(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def send_shared_key(self, peer_public_key_pem):
        peer_public_key = serialization.load_pem_public_key(peer_public_key_pem, backend=default_backend())
        shared_key = os.urandom(32)
        encrypted_key = peer_public_key.encrypt(
            shared_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        self.shared_key = shared_key
        return encrypted_key

    def receive_shared_key(self, encrypted_key):
        decrypted_key = self.private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        self.shared_key = decrypted_key

    def encrypt_message(self, plaintext):
        if not self.shared_key:
            raise ValueError("Shared key not established!")
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.shared_key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
        return base64.b64encode(iv + ciphertext).decode()

    def decrypt_message(self, ciphertext):
        if not self.shared_key:
            raise ValueError("Shared key not established!")
        data = base64.b64decode(ciphertext)
        iv, actual_ciphertext = data[:16], data[16:]
        cipher = Cipher(algorithms.AES(self.shared_key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()
        return plaintext.decode()

    def add_peer(self, peer_id, connection):
        self.peers[peer_id] = {"connection": connection, "last_heartbeat": time.time()}

    def simulate_connection(self, peer):
        peer_public_key = peer.get_public_key_pem()
        encrypted_key_for_peer = self.send_shared_key(peer_public_key)
        peer.receive_shared_key(encrypted_key_for_peer)
        connection = SimulatedConnection(sender=self, receiver=peer)
        self.add_peer(peer.node_id, connection)
        peer.add_peer(self.node_id, SimulatedConnection(sender=peer, receiver=self))

    def receive_heartbeat(self, peer_id):
        if peer_id in self.peers:
            self.peers[peer_id]["last_heartbeat"] = time.time()

    def send_heartbeat(self):
        while self.alive:
            peers_copy = list(self.peers.items())
            for peer_id, peer_info in peers_copy:
                try:
                    message = "HEARTBEAT"
                    encrypted_message = self.encrypt_message(message)
                    peer_info["connection"].send(encrypted_message.encode())
                except Exception as e:
                    print(f"Failed to send heartbeat to peer {peer_id}: {e}")
            time.sleep(self.heartbeat_interval)

    def check_heartbeat(self):
        while self.alive:
            current_time = time.time()
            peers_copy = list(self.peers.items())
            for peer_id, peer_info in peers_copy:
                if current_time - peer_info["last_heartbeat"] > self.heartbeat_timeout:
                    print(f"Peer {peer_id} is marked as failed.")
                    del self.peers[peer_id]
            time.sleep(1)

    def start_heartbeat_monitor(self):
        threading.Thread(target=self.send_heartbeat, daemon=True).start()
        threading.Thread(target=self.check_heartbeat, daemon=True).start()

    def handle_node_leave(self, departing_node_id):
        if departing_node_id in self.peers:
            del self.peers[departing_node_id]

    def reintegrate_node(self, peers):
        for peer_id, peer_info in peers.items():
            peer = peer_info["connection"].receiver
            self.simulate_connection(peer)

    def start_election(self):
        highest_id = self.node_id
        for peer_id in self.peers.keys():
            if peer_id > highest_id:
                highest_id = peer_id

        if highest_id == self.node_id:
            self.is_leader = True
            self.leader_id = self.node_id
            print(f"Node {self.node_id} is now the leader.")
        else:
            self.is_leader = False
            self.leader_id = highest_id
            print(f"Node {self.node_id} recognizes Node {self.leader_id} as the leader.")

    def replicate_data(self, data):
        encrypted_data = self.encrypt_message(data)
        for peer_id, peer_info in self.peers.items():
            try:
                peer_info["connection"].send(encrypted_data.encode())
            except Exception as e:
                print(f"Failed to replicate data to peer {peer_id}: {e}")

    def handle_incoming_message(self, encrypted_message, peer_id):
        decrypted_message = self.decrypt_message(encrypted_message.decode())
        print(f"Node {self.node_id} received message from Node {peer_id}: {decrypted_message}")
        self.local_data.append(decrypted_message)

# Simulation
def system_failure_recovery_simulation():
    node1 = ConsensusNode(node_id=1)
    node2 = ConsensusNode(node_id=2)
    node3 = ConsensusNode(node_id=3)

    node1.simulate_connection(node2)
    node2.simulate_connection(node3)
    node3.simulate_connection(node1)

    node1.start_heartbeat_monitor()
    node2.start_heartbeat_monitor()
    node3.start_heartbeat_monitor()

    node1.start_election()
    node2.start_election()
    node3.start_election()

    timeline = []
    total_time = 120
    failure_interval = 30
    recovery_time = 20

    current_time = 0
    while current_time < total_time:
        if current_time % failure_interval == 0 and current_time != 0:
            print(f"Simulating failure of Node 2 at time {current_time}s.")
            node1.handle_node_leave(2)
            node3.handle_node_leave(2)
            timeline.append((current_time, "Node 2 Failed"))

            time.sleep(recovery_time // 2)
            current_time += recovery_time // 2

            print(f"Simulating recovery of Node 2 at time {current_time}s.")
            node2.reintegrate_node(node1.peers)
            timeline.append((current_time, "Node 2 Recovered"))

        timeline.append((current_time, "System Stable"))
        time.sleep(5)
        current_time += 5

    return timeline

simulation_timeline = system_failure_recovery_simulation()
times = [time for time, status in simulation_timeline]
statuses = [status for time, status in simulation_timeline]

plt.figure(figsize=(12, 6))
for t, s in simulation_timeline:
    plt.scatter(t, 1 if "Stable" in s else 0, label=s, alpha=0.6)

plt.yticks([0, 1], ["Failed/Recovering", "Stable"])
plt.xlabel("Time (s)")
plt.ylabel("System Status")
plt.title("Failure and Recovery Simulation Using Designed System with Replication")
plt.grid(True)
plt.legend(set(statuses), loc="upper right")
plt.show()
