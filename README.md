# ECDH + AES-256 Encryption Example

This repository provides a simple and secure implementation of the **Elliptic Curve Diffie-Hellman (ECDH)** key exchange protocol combined with **AES-256** encryption, allowing you to securely exchange keys and communicate confidentially.

The project demonstrates how to:
- Perform **ECDH** key exchange between two parties.
- Derive a secure shared secret.
- Use the shared secret to derive an **AES-256 encryption key**.
- Encrypt and decrypt messages securely.

---

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)

---

## Introduction

The **ECDH** (Elliptic Curve Diffie-Hellman) key exchange is a cryptographic protocol that allows two parties to exchange a secret key over an insecure channel. This key exchange is then used to securely encrypt and decrypt data using the **AES-256** encryption standard.

This project simplifies the process of implementing ECDH and AES-256 encryption, making it easier to integrate secure communications into your applications. It demonstrates the power of modern cryptography, giving you access to top-tier security with minimal effort.

---

## Features

- **ECDH Key Exchange**: A secure and efficient method for two parties to agree on a shared secret.
- **AES-256 Encryption**: A robust symmetric encryption algorithm for securing messages.
- **Simple and Easy-to-Use**: Implemented in Python, easy to integrate into your projects.
- **Perfect Forward Secrecy**: Each session uses a unique shared secret, ensuring past communications are protected even if private keys are compromised in the future.

---

## Installation

To use this project, you'll need Python installed along with the following dependencies:

1. Install **PyCryptodome** (for AES encryption and cryptographic functions):

    ```bash
    pip install pycryptodome
    ```

2. Clone this repository or download the `ecdh.py` file.

---

## Usage

Here's a basic example of how to use **ECDH + AES-256** to establish a secure communication channel between a client and a server:

### Example: Client

```python
from ecdh import ECDH, encrypt_data, decrypt_data
import socket

# Initialize the client-side ECDH
client = ECDH()

# Connect to the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('localhost', 12345))

    # Send the client's public key to the server
    s.send(client.public_key.export_key(format='PEM'))

    # Receive the server's public key
    server_public_key_data = s.recv(1024)
    server_public_key = ECC.import_key(server_public_key_data)

    # Perform the ECDH key exchange and calculate the shared secret
    client.exchange(server_public_key)

    # Derive the AES key from the shared secret
    aes_key, salt = client.derive_key()

    # Encrypt a message
    message = "Hello, server!"
    encrypted_message = encrypt_data(message.encode(), aes_key)

    # Send the encrypted message to the server
    s.send(encrypted_message)
```

### Example: Server

```python
from ecdh import ECDH, encrypt_data, decrypt_data
import socket

# Initialize the server-side ECDH
server = ECDH()

# Set up the server to listen for connections
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('localhost', 12345))
    s.listen()

    # Accept a connection from the client
    conn, addr = s.accept()
    with conn:
        # Receive the client's public key
        client_public_key_data = conn.recv(1024)
        client_public_key = ECC.import_key(client_public_key_data)

        # Send the server's public key to the client
        conn.send(server.public_key.export_key(format='PEM'))

        # Perform the ECDH key exchange
        server.exchange(client_public_key)

        # Derive the AES key from the shared secret
        aes_key, salt = server.derive_key()

        # Receive the encrypted message from the client
        encrypted_message = conn.recv(1024)

        # Decrypt the message
        decrypted_message = decrypt_data(encrypted_message, aes_key)
        print(f"Decrypted message: {decrypted_message.decode()}")
```

---

## How It Works

1. **Key Generation**: 
    - Both the client and the server generate a private and public key pair using elliptic curve cryptography.

2. **Key Exchange**: 
    - The client and server exchange their public keys over the network.

3. **Shared Secret**: 
    - Using their private keys and the other party's public key, both the client and server independently calculate the same shared secret.

4. **AES Key Derivation**: 
    - The shared secret is used to derive a 256-bit AES key.

5. **Message Encryption**: 
    - The client encrypts the message using the AES key and sends it to the server.

6. **Message Decryption**: 
    - The server decrypts the message using the same AES key derived from the shared secret.

---

## Contributing

Contributions are welcome! If you'd like to improve this project, please feel free to:

1. Fork the repository.
2. Make your changes.
3. Submit a pull request with a description of the changes.

---

## License

This project is licensed under the **MIT License**. See the LICENSE file for more details.
