import sys, os

# Import function
"""def Import_File(File_Name: str, zip_path: str, Zip_Password="PASSWORD", File_Password="PASSWORD", temp_dir="./temp"):
    import zipfile
    import importlib.util
    import shutil
    import os
    import sys
    from pathlib import Path
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import padding, hashes
    from PyQt5.QtGui import QPixmap

    # Utility: Derive encryption key
    def derive_key(password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(password.encode())

    # Utility: Decrypt a single file
    def decrypt_file(encrypted_path: Path, output_folder: Path, password: str):
        try:
            with open(encrypted_path, 'rb') as enc_file:
                content = enc_file.read()
                if len(content) < 32:
                    raise ValueError("Invalid encrypted file format.")

                salt = content[:16]
                iv = content[16:32]
                ciphertext = content[32:]

                key = derive_key(password, salt)
                cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
                decryptor = cipher.decryptor()

                padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

                unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
                plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

                output_file = output_folder / encrypted_path.stem
                output_file.write_bytes(plaintext)

                return output_file
        except Exception as e:
            print(f"Error decrypting {encrypted_path}: {e}")
            return None

    # Utility: Extract ZIP files
    def extract_zip(zip_path: Path, output_folder: Path, password: str):
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.setpassword(password.encode())
                zf.extractall(output_folder)
        except Exception as e:
            print(f"Error extracting {zip_path}: {e}")
            pass

    try:
        os.makedirs(temp_dir, exist_ok=True)

        # Extract the ZIP file
        extract_folder = Path(temp_dir) / "extracted_files"
        extract_folder.mkdir(parents=True, exist_ok=True)
        extract_zip(Path(zip_path), extract_folder, Zip_Password)

        # Search for the encrypted file (any file that matches File_Name and ends with .enc)
        encrypted_files = list(extract_folder.glob(f"{File_Name}*.enc"))
        if not encrypted_files:
            raise FileNotFoundError(f"Encrypted file for {File_Name} not found.")

        # Assume there's only one matching .enc file, but we can handle multiple if needed
        encrypted_path = encrypted_files[0]

        # Decrypt the file
        decrypted_path = decrypt_file(encrypted_path, extract_folder, File_Password)

        # Determine file type from the decrypted file name
        file_extension = decrypted_path.suffix.lower()

        # Handle based on file type
        if file_extension == ".py":
            # Import Python file as a module
            spec = importlib.util.spec_from_file_location(File_Name, str(decrypted_path))
            Imported_File = importlib.util.module_from_spec(spec)
            sys.modules[File_Name] = Imported_File
            spec.loader.exec_module(Imported_File)
            return Imported_File
        elif file_extension in [".txt", ".qss"]:
            # Return text file content
            with open(decrypted_path, "r", encoding="utf-8") as file:
                return file.read()
        elif file_extension == ".png":
            # Return image as QPixmap
            return QPixmap(str(decrypted_path))
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

    except Exception as e:
        print(f"Error importing file: {e}")
        return None
    finally:
        # Cleanup
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
"""
# Import function
def Import_File(File_Name: str, zip_path: str, Zip_Password="PASSWORD", File_Password="PASSWORD", temp_dir="./temp"):
    import zipfile
    import importlib.util
    import shutil
    import os
    import sys
    from pathlib import Path
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import padding, hashes
    from PyQt5.QtGui import QPixmap

    # Utility: Derive encryption key
    def derive_key(password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(password.encode())

    # Utility: Decrypt a single file
    def decrypt_file(encrypted_path: Path, output_folder: Path, password: str):
        """global Called
        Called = Called + 1
        print(Called)"""
        try:
            with open(encrypted_path, 'rb') as enc_file:
                content = enc_file.read()
                if len(content) < 32:
                    raise ValueError("Invalid encrypted file format.")

                salt = content[:16]
                iv = content[16:32]
                ciphertext = content[32:]

                key = derive_key(password, salt)
                cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
                decryptor = cipher.decryptor()

                padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

                unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
                plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

                output_file = output_folder / encrypted_path.stem
                output_file.write_bytes(plaintext)

                #print(f"Decrypted: {encrypted_path} -> {output_file}")
                return output_file
        except Exception as e:
            print(f"Error decrypting {encrypted_path}: {e}")
            return None

    # Utility: Extract ZIP files
    def extract_zip(zip_path: Path, output_folder: Path, password: str):
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.setpassword(password.encode())
                zf.extractall(output_folder)
                #print(f"Extracted ZIP: {zip_path} -> {output_folder}")
        except Exception as e:
            print(f"Error extracting {zip_path}: {e}")
            pass

    try:
        os.makedirs(temp_dir, exist_ok=True)

        # Extract the ZIP file
        extract_folder = Path(temp_dir) / "extracted_files"
        extract_folder.mkdir(parents=True, exist_ok=True)
        extract_zip(Path(zip_path), extract_folder, Zip_Password)

        # Search for the encrypted file (any file that matches File_Name and ends with .enc)
        encrypted_files = list(extract_folder.glob(f"{File_Name}*.enc"))
        if not encrypted_files:
            raise FileNotFoundError(f"Encrypted file for {File_Name} not found.")

        # Assume there's only one matching .enc file, but we can handle multiple if needed
        encrypted_path = encrypted_files[0]

        # Decrypt the file
        decrypted_path = decrypt_file(encrypted_path, extract_folder, File_Password)

        # Determine file type from the decrypted file name
        file_extension = decrypted_path.suffix.lower()
        #print(f"Detected file extension: {file_extension}")

        # Handle based on file type
        if file_extension == ".py":
            # Import Python file as a module
            spec = importlib.util.spec_from_file_location(File_Name, str(decrypted_path))
            Imported_File = importlib.util.module_from_spec(spec)
            sys.modules[File_Name] = Imported_File
            spec.loader.exec_module(Imported_File)
            return Imported_File
        elif file_extension in [".txt", ".qss"]:
            # Return text file content
            with open(decrypted_path, "r", encoding="utf-8") as file:
                return file.read()
        elif file_extension == ".png":
            # Return image as QPixmap
            return QPixmap(str(decrypted_path))
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

    except Exception as e:
        print(f"Error importing file: {e}")
        return None
    finally:
        # Cleanup
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

Cardholder_Verification_File, Skyline_Terminate_AA_File = None, None


try:
    #Cardholder_Verification_File = Import_File("Cardholder_Verification_File", resource_path(os.path.join("Resources/Test/Scripts/Cardholder_Verification.zip")))
    Cardholder_Verification_File = Import_File("Cardholder_Verification_File", resource_path(os.path.join("Resources", "Test", "Scripts", "Cardholder_Verification.zip")))
    if Cardholder_Verification_File is None:
        raise FileNotFoundError("Import_File returned None. File may not exist or is inaccessible.")
    elif Cardholder_Verification_File is not None:
        print("Hello")
    else:
        print("Hi")
except FileNotFoundError as e:
    print(f"Error: {e}")
    Cardholder_Verification_File = None
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    Cardholder_Verification_File = None