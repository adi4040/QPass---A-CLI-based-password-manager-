import hashlib
import base64
from cryptography.fernet import Fernet


def encrypt_password(passwd, string, salt):

    # Step 1: Derive key using KDF (PBKDF2)
    key = hashlib.pbkdf2_hmac(
        'sha256',              # hash algorithm
        passwd.encode(),       # convert password to bytes
        salt,                  # salt (bytes)
        100000                 # iterations (security factor)
    )

    # Step 2: Convert to Fernet-compatible key
    fernet_key = base64.urlsafe_b64encode(key)

    # Step 3: Initialize Fernet
    f = Fernet(fernet_key)

    # Step 4: Encrypt the string
    encrypted_data = f.encrypt(string.encode())
    
    return encrypted_data

def decrypt_password(passwd, encrypted_pass, salt):

    # Step 1: Derive key using KDF (PBKDF2)
    key = hashlib.pbkdf2_hmac(
        'sha256',              # hash algorithm
        passwd.encode(),       # convert password to bytes
        salt,                  # salt (bytes)
        100000                 # iterations (security factor)
    )

        # Step 2: Convert to Fernet-compatible key
    fernet_key = base64.urlsafe_b64encode(key)

    # Step 3: Initialize Fernet
    f = Fernet(fernet_key)

    # Step 4: Encrypt the string
    decrypted_data = f.decrypt(encrypted_pass).decode()
    
    return decrypted_data


