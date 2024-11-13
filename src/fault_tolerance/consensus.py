import random
import time
import logging

class ConsensusNode:
    def __init__(self, node_id, nodes):
        self.node_id = node_id
        self.nodes = nodes  # List of all nodes in the cluster
        self.is_leader = False

    def start_election(self):
        logging.info(f"Node {self.node_id} is starting an election.")
        election_results = self.send_election_requests()
        self.process_election_results(election_results)

    def send_election_requests(self):
        logging.info(f"Node {self.node_id} sending election requests to other nodes.")
        election_results = {}
        for node in self.nodes:
            if node != self.node_id:
                election_results[node] = random.choice([True, False])  # Randomly elect some nodes as 'yes'
        return election_results

    def process_election_results(self, election_results):
        votes = sum([1 for vote in election_results.values() if vote])
        if votes > len(self.nodes) // 2:
            self.is_leader = True
            logging.info(f"Node {self.node_id} is elected as the leader.")
        else:
            self.is_leader = False
            logging.info(f"Node {self.node_id} failed to be elected as the leader.")

    def join_network(self):
        # Simulate the process of a new node joining the network
        logging.info(f"Node {self.node_id} joining the network.")
        self.start_election()

def simulate_consensus(nodes_count):
    nodes = [ConsensusNode(i, list(range(nodes_count))) for i in range(nodes_count)]
    for node in nodes:
        node.join_network()
        time.sleep(1)  # Simulate time between different nodes starting their elections

if __name__ == "__main__":
    simulate_consensus(5)  # Simulating 5 nodes in the cluster
