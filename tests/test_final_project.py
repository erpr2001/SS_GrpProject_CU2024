
from final_project_code import ConsensusNode

def main():
    # Create three nodes for testing
    node1 = ConsensusNode(node_id=1)
    node2 = ConsensusNode(node_id=2)
    node3 = ConsensusNode(node_id=3)

    # Simulate connections between nodes
    node1.simulate_connection(node2)
    node2.simulate_connection(node3)
    node3.simulate_connection(node1)

    # Start heartbeat monitoring for all nodes
    node1.start_heartbeat_monitor()
    node2.start_heartbeat_monitor()
    node3.start_heartbeat_monitor()

    # Start leader election
    node1.start_election()
    node2.start_election()
    node3.start_election()

    # Leader broadcasts data
    if node1.is_leader:
        node1.leader_broadcast("Initial data from Leader Node 1")

    # Node 3 joins the system dynamically (already connected in this test setup)
    print(f"Node 3's peers: {list(node3.peers.keys())}")

    # Simulate Node 3 leaving the system
    node1.handle_node_leave(node3.node_id)
    print(f"Node 1's peers after Node 3 leaves: {list(node1.peers.keys())}")

    # Simulate Node 3 reintegrating into the system
    node3.reintegrate_node(node1.peers)
    print(f"Node 3's local data after reintegration: {node3.local_data}")

    # Simulate leader failure and re-election
    if node1.is_leader:
        node1.peers.pop(node2.node_id, None)  # Simulate Node 2 failure
        node3.detect_leader_failure()

    # New leader broadcasts data
    if node3.is_leader:
        node3.leader_broadcast("Data from new Leader Node 3")

if __name__ == "__main__":
    main()
