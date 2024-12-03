from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, hashes
import os
import base64

# Function to derive a key from a password
def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Function to encrypt a file
def encrypt_file(file_path: str, password: str):
    # Generate a salt
    salt = os.urandom(16)
    key = derive_key(password, salt)
    
    # Read file content
    with open(file_path, 'rb') as file:
        plaintext = file.read()
    
    # Add padding
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()
    
    # Encrypt
    iv = os.urandom(16)  # Initialization vector
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    
    # Write the encrypted file
    with open(file_path + '.enc', 'wb') as encrypted_file:
        encrypted_file.write(salt + iv + ciphertext)  # Store salt and IV along with ciphertext
    print(f"Encrypted: {file_path} -> {file_path}.enc")

# Specify the files and password
files_to_encrypt = ["file1.py", "file2.py"]  # Replace with your file names
encryption_password = "your-secure-password"  # Replace with your password

# Encrypt each file
for file in files_to_encrypt:
    encrypt_file(file, encryption_password)
