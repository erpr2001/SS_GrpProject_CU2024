# test_encryption.py
import unittest
from src.encryption.aes import encrypt_message_aes, decrypt_message_aes
from src.encryption.rsa import generate_rsa_keys, encrypt_with_rsa, decrypt_with_rsa

class TestEncryption(unittest.TestCase):
    def test_aes_encryption(self):
        # key = b"thisisaverysecretkey256bits!!"  
        original_data = b"Hello, this is a test."
        # Or let the function generate a random key
        key, iv, encrypted_data = encrypt_message_aes(original_data, key)  # Returns key, iv, and ciphertext
        decrypted_data = decrypt_message_aes(key, iv, encrypted_data)   # Decrypt with the same key and iv
        self.assertEqual(decrypted_data, original_data)

    def test_rsa_encryption(self):
        private_key, public_key = generate_rsa_keys()
        original_data = b"Hello, RSA!"
        encrypted_data = encrypt_with_rsa(public_key, original_data)
        decrypted_data = decrypt_with_rsa(private_key, encrypted_data)
        self.assertEqual(decrypted_data, original_data)

if __name__ == "__main__":
    unittest.main()
