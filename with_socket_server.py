import socket
from ecdh import ECDH, encrypt_data, decrypt_data

# Initialize ECDH server and wait for client connection
server = ECDH()

# Set up the server to listen for incoming connections
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('localhost', 12345))
    s.listen()

    # Accept a client connection
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")

        # Receive the client's public key
        client_public_key_data = conn.recv(1024)
        client_public_key = ECC.import_key(client_public_key_data)

        # Send the server's public key to the client
        conn.send(server.public_key.export_key(format='PEM'))

        # Perform the ECDH exchange and compute the shared secret
        server.exchange(client_public_key)

        # Derive the AES key from the shared secret
        aes_key, salt = server.derive_key()

        # Receive the encrypted data
        encrypted_data = conn.recv(1024)

        # Decrypt the data
        decrypted_data = decrypt_data(encrypted_data, aes_key)
        print(f"Decrypted data: {decrypted_data.decode()}")
      
