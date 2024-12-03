from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, hashes
from pathlib import Path
import os

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
def encrypt_file(file_path: str, password: str, output_directory: str = None):
    try:
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
        
        # Determine output path
        file_path = Path(file_path)
        output_directory = Path(output_directory) if output_directory else file_path.parent
        output_directory.mkdir(parents=True, exist_ok=True)  # Create output dir if needed
        encrypted_file_path = output_directory / (file_path.name + '.enc')
        
        # Write the encrypted file
        with open(encrypted_file_path, 'wb') as encrypted_file:
            encrypted_file.write(salt + iv + ciphertext)  # Store salt and IV along with ciphertext
        print(f"Encrypted: {file_path} -> {encrypted_file_path}")
    except Exception as e:
        print(f"Failed to encrypt {file_path}: {e}")

# Specify the folder containing files and the password
source_folder = "Resources/Utilities"  # Replace with the folder containing your files
files_to_encrypt = ["Utilities_File.py", "Quip_Utilities_File.py"]  # Replace with file names
files_to_encrypt = [os.path.join(source_folder, file) for file in files_to_encrypt]  # Prepend folder path
encryption_password = os.getenv("PASSWORD", "default_password")  # Use environment variable or fallback
output_dir = "Encrypted_Files"  # Output directory for encrypted files

# Encrypt each file
for file in files_to_encrypt:
    encrypt_file(file, encryption_password, output_dir)
