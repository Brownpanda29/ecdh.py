import socket
from ecdh import ECDH, encrypt_data, decrypt_data

# Create the ECDH client and perform the key exchange with the server
client = ECDH()

# Assuming you already have the server's public key somehow (for example, received from the server)
server_public_key = ...  # Fetch or exchange the public key (this could be done beforehand)

# Perform the ECDH exchange with the server
server_public_key = client.exchange(server_public_key)

# Derive the AES key from the shared secret
aes_key, salt = client.derive_key()

# Encrypt some data to send to the server
data_to_send = b"Hello, secure server!"
encrypted_data = encrypt_data(data_to_send, aes_key)

# Send the encrypted data to the server (you can send the nonce, tag, and ciphertext over the socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('localhost', 12345))  # Replace with server address
    s.send(encrypted_data)
