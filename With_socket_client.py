import socket
from ecdh import ECDH, encrypt_data, decrypt_data

# Initialize ECDH and perform key exchange with server
client = ECDH()

# Connect to the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('localhost', 12345))

    # Send the client's public key to the server
    s.send(client.public_key.export_key(format='PEM'))  # Export the public key in PEM format

    # Receive the server's public key
    server_public_key_data = s.recv(1024)
    server_public_key = ECC.import_key(server_public_key_data)

    # Perform the ECDH exchange and compute the shared secret
    client.exchange(server_public_key)

    # Derive the AES key from the shared secret
    aes_key, salt = client.derive_key()

    # Encrypt data to send
    data_to_send = b"Hello, secure server!"
    encrypted_data = encrypt_data(data_to_send, aes_key)

    # Send encrypted data to the server
    s.send(encrypted_data)
  
