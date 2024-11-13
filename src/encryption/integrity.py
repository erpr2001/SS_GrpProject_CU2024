from cryptography.hazmat.primitives import hashes

def compute_hash(data):
    digest = hashes.Hash(hashes.SHA256())
    digest.update(data.encode())
    return digest.finalize()

message = "Important data"
hash_value = compute_hash(message)
print("SHA-256 hash:", hash_value)


# Example to simulate a check
# Assume the sender sends the message and its hash, and the receiver performs the check
received_message = "Important data"  # This could be the decrypted message
received_hash = hash_value  # Hash sent along with the message

# The receiver checks if the hash matches
if compute_hash(received_message) == received_hash:
    print("Data integrity verified!")
else:
    print("Data integrity check failed!")