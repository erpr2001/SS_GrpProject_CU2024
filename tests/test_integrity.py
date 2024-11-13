import unittest
from src.encryption.integrity import compute_hash

class TestIntegrity(unittest.TestCase):
    
    def test_compute_hash(self):
        message = "Important data"
        expected_hash = b"\x90\x8f\x8a\x7f\x22\xe6\x61\x5b\x44\xf7\x56\x59\xd3\x13\x51\x57\xb2\xd2\x28\xfd\x5e\x16\x9f\x61\x28\xb6\x58\xba\x6f\xe5\x0a\xd4\xbe"  # Replace with actual expected value
        computed_hash = compute_hash(message)
        
        # Assert that the computed hash matches the expected value
        self.assertEqual(computed_hash, expected_hash)
    
    def test_data_integrity_check(self):
        original_message = "Confidential message"
        # Compute hash of the original message
        original_hash = compute_hash(original_message)

        # Simulate the transmission process where the message and its hash are sent together
        received_message = original_message  # In a real scenario, the message is decrypted here
        received_hash = original_hash  # Assume the hash was sent along with the message
        
        # Check if the received data's hash matches the original hash
        self.assertEqual(compute_hash(received_message), received_hash)

        # Simulate a modified message (tampering occurs)
        tampered_message = "Confidential messag"  # Altered message
        self.assertNotEqual(compute_hash(tampered_message), received_hash)

if __name__ == "__main__":
    unittest.main()
