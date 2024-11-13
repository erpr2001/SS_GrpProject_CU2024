from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

def encrypt_message_aes(message, key=None):
    if key is None:
        key = os.urandom(32)  # AES-256 key
    iv = os.urandom(16)   # Initialization vector
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message.encode()) + encryptor.finalize()
    return key, iv, ciphertext

def decrypt_message_aes(key, iv, ciphertext):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()

# Example usage
key, iv, ciphertext = encrypt_message_aes("Confidential message")
plaintext = decrypt_message_aes(key, iv, ciphertext)
print("Decrypted:", plaintext.decode())
