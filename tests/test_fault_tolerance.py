import unittest
from src.fault_tolerance.replication import replicate_data
from src.fault_tolerance.recovery import monitor_health, recovery_action
import os
import shutil
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


class TestFaultTolerance(unittest.TestCase):
    def test_data_replication(self):
        # Setup
        source_file = "test_data.txt"
        dest_dir = "replicated_data"

        # Create a test data file
        os.makedirs(dest_dir, exist_ok=True)
        with open(source_file, "w") as file:
            file.write("Test data replication.")

        # Replicate the file
        replicate_data(source_file, dest_dir)
        
        # Assert the file exists in the destination directory
        self.assertTrue(os.path.exists(os.path.join(dest_dir, "test_data.txt")))

        # Cleanup
        shutil.rmtree(dest_dir)
        os.remove(source_file)
    
    def mock_node_status(self):
        # Simulate a node failure (returns False)
        return False

    def test_recovery_action(self):
        # Mock the node failure scenario and recovery action
        try:
            monitor_health(self.mock_node_status, recovery_action)
        except Exception as e:
            self.fail(f"Error during fault tolerance test: {e}")

    

if __name__ == "__main__":
    unittest.main()
