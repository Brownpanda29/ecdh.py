import socket
from ecdh import ECDH, encrypt_data, decrypt_data

# Create the ECDH server and wait for the client's key exchange
server = ECDH()

# For example, we get the client's public key via socket or another method
client_public_key = ...  # Receive or fetch the client's public key

# Perform the ECDH exchange with the client
client_public_key = server.exchange(client_public_key)

# Derive the AES key from the shared secret
aes_key, salt = server.derive_key()

# Set up the server to listen for incoming connections
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('localhost', 12345))  # Listen on localhost and port 12345
    s.listen()
    
    # Accept a connection from the client
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        
        # Receive encrypted data
        encrypted_data = conn.recv(1024)
        
        # Decrypt the data
        decrypted_data = decrypt_data(encrypted_data, aes_key)
        print(f"Decrypted data: {decrypted_data.decode()}")
      
