from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# RSA key generation
def generate_rsa_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

# Encrypt and decrypt messages
def encrypt_with_rsa(public_key, message):
    return public_key.encrypt(
        message,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

def decrypt_with_rsa(private_key, encrypted_message):
    return private_key.decrypt(
        encrypted_message,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

# Usage
private_key, public_key = generate_rsa_keys()
message = b"Secret key for AES"
encrypted_message = encrypt_with_rsa(public_key, message)
decrypted_message = decrypt_with_rsa(private_key, encrypted_message)
print("Decrypted message:", decrypted_message)
