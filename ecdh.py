from Crypto.PublicKey import ECC
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt
from Crypto.Hash import SHA256
import os

class ECDH:
    def __init__(self):
        # Generate the ECDH private key (this will be done for both server and client)
        self.private_key = ECC.generate(curve='P-256')
        self.public_key = self.private_key.public_key()
        self.shared_secret = None

    def exchange(self, other_public_key):
        """
        Perform ECDH key exchange. This method computes the shared secret 
        from this instance's private key and the other party's public key.
        """
        # Compute the shared secret using our private key and the other party's public key
        self.shared_secret = self.private_key.exchange(ECC.ECDH(), other_public_key)

        # Return the public key so the other party can perform their own ECDH exchange
        return self.public_key

    def derive_key(self, salt=None):
        """
        Derive the AES key from the shared secret using scrypt.
        Optionally use a salt to strengthen the key derivation.
        """
        if salt is None:
            salt = get_random_bytes(16)  # Random salt
        
        # Use scrypt to derive the AES key
        aes_key = scrypt(self.shared_secret, salt, dkLen=32)  # AES-256 key (32 bytes)
        return aes_key, salt


def encrypt_data(data, aes_key):
    """
    Encrypt data using AES-256-GCM mode with the given AES key.
    """
    nonce = get_random_bytes(16)  # Generate a random nonce
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    
    return nonce + tag + ciphertext  # Combine nonce, tag, and ciphertext


def decrypt_data(encrypted_data, aes_key):
    """
    Decrypt data using AES-256-GCM mode with the given AES key.
    """
    nonce = encrypted_data[:16]  # Extract the nonce
    tag = encrypted_data[16:32]  # Extract the tag
    ciphertext = encrypted_data[32:]  # Extract the ciphertext

    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    
    return data
