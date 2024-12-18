import os, sys


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

    
    def derive_key(password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(password.encode())

    
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
            
            return None

    
    def extract_zip(zip_path: Path, output_folder: Path, password: str):
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.setpassword(password.encode())
                zf.extractall(output_folder)
                
        except Exception as e:
            
            pass

    try:
        os.makedirs(temp_dir, exist_ok=True)

        
        extract_folder = Path(temp_dir) / "extracted_files"
        extract_folder.mkdir(parents=True, exist_ok=True)
        extract_zip(Path(zip_path), extract_folder, Zip_Password)

        
        encrypted_files = list(extract_folder.glob(f"{File_Name}*.enc"))
        if not encrypted_files:
            raise FileNotFoundError(f"Encrypted file for {File_Name} not found.")

        
        encrypted_path = encrypted_files[0]

        
        decrypted_path = decrypt_file(encrypted_path, extract_folder, File_Password)

        
        file_extension = decrypted_path.suffix.lower()
        

        
        if file_extension == ".py":
            
            spec = importlib.util.spec_from_file_location(File_Name, str(decrypted_path))
            Imported_File = importlib.util.module_from_spec(spec)
            sys.modules[File_Name] = Imported_File
            spec.loader.exec_module(Imported_File)
            return Imported_File
        elif file_extension in [".txt", ".qss"]:
            
            with open(decrypted_path, "r", encoding="utf-8") as file:
                return file.read()
        elif file_extension == ".png":
            
            return QPixmap(str(decrypted_path))
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

    except Exception as e:
        
        return None
    finally:
        
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller."""
    
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.argv[0]))
    return os.path.join(base_path, relative_path)

Cardholder_Verification_File = None

try:
    Cardholder_Verification_File = Import_File("Cardholder_Verification", resource_path(os.path.join("Resources", "Test", "Scripts", "Cardholder_Verification.zip")))
    
    if Cardholder_Verification_File is None:
        raise FileNotFoundError("Import_File returned None. File may not exist or is inaccessible.")
except FileNotFoundError as e:
    print(f"Error: {e}")
    Cardholder_Verification_File = None
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    Cardholder_Verification_File = None

class StopFunctionException(Exception):
    pass

def check_stop_event(stop_event=None):
    if stop_event.is_set():
        raise StopFunctionException

def Plugin_Settings(settings):
    Plugins = []

    Plugins.append(settings.get("Cardholder_Verification_Plugin", False)) 
    Plugins.append("Cardholder Verification")
    Plugins.append(True) 
    Plugins.append("This script retrieves a list of employee EIDs or Logins from your selected database, "
               "searches each profile in the Cardholder Management System, and copies the requested "
               "information back to the database. The available options streamline the data transfer process, "
               "making it easier to complete your tasks efficiently")

    Plugins.append(False)
    Plugins.append("Placeholder_Name0")
    Plugins.append(True) 
    Plugins.append("Message")

    Plugins.append(False)
    Plugins.append("Placeholder_Name1")
    Plugins.append(True) 
    Plugins.append("Message")

    Plugins.append(False)
    Plugins.append("Placeholder_Name2")
    Plugins.append(True) 
    Plugins.append("Message")

    Plugins.append(False)
    Plugins.append("Placeholder_Name3")
    Plugins.append(True) 
    Plugins.append("Message")

    return Plugins

def Plugin_Widget_Setup(FunctionsGUI, widget, settings, Save_Widget_Settings, grid_layout, Script_Widgets, index1):
    if index1 == 0:
        if Cardholder_Verification_File:
            Widget_Setup = getattr(Cardholder_Verification_File, "Widget_Setup", None)
            if Widget_Setup:
                Widget_Setup(FunctionsGUI, widget, settings, Save_Widget_Settings, grid_layout, Script_Widgets)
            else:
                widget = widget
                Script_Widgets.append(widget)
        else:
            widget = widget
            Script_Widgets.append(widget)

    elif index1 == 3:
        widget = widget
        Script_Widgets.append(widget)

    return widget

def Script_Launcher(get_next_index, function_mapping, index1):
    if index1 == 0:
        if Cardholder_Verification_File:
            Cardholder_Verification = getattr(Cardholder_Verification_File, "Cardholder_Verification", None)
            if Cardholder_Verification:
                next_index = get_next_index(function_mapping)
                function_mapping[next_index] = Cardholder_Verification
            else:
                next_index = get_next_index(function_mapping)
                function_mapping[next_index] = None
        else:
            next_index = get_next_index(function_mapping)
            function_mapping[next_index] = None

    elif index1 == 3:
        next_index = get_next_index(function_mapping)
        function_mapping[next_index] = None

def Open_Browser(FunctionsGUI, Plugins, function_combobox, Chrome=False, Firefox=False, Edge=False):
    from selenium import webdriver
    import threading, time
    gtime = 0.25

    if Chrome:
        
        user_data_dir = "/ChromeData"

        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--user-data-dir=" + user_data_dir)

        
        driver = webdriver.Chrome(options=chrome_options)

    if Firefox:
        
        user_data_dir = "/FirefoxData"

        
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument("--start-maximized")
        firefox_options.add_argument(user_data_dir)

        
        driver = webdriver.Firefox(options=firefox_options)

    if Edge:
        
        user_data_dir = "/EdgeData"

        
        edge_options = webdriver.EdgeOptions()
        edge_options.add_argument("--start-maximized")
        edge_options.add_argument(user_data_dir)

        
        driver = webdriver.Edge(options=edge_options)

    
    window_handles = []

    
    driver.get("https://quip-amazon.com/all")
    original_window = driver.current_window_handle
    window_handles.append(original_window)
    time.sleep(gtime)

    if (Plugins[0] and function_combobox.currentText() == Plugins[1]):
        driver.execute_script("window.open('" + "http://localhost:8000/Website1/html/index.html?" + "', '_blank');")
        window_handles.append(driver.window_handles[-1])
        time.sleep(gtime)

    if (Plugins[4] and function_combobox.currentText() == Plugins[5]):
        driver.execute_script(
            "window.open('" + "" + "', '_blank');")
        window_handles.append(driver.window_handles[-1])
        time.sleep(gtime)

    if (Plugins[8] and function_combobox.currentText() == Plugins[9]):
        driver.execute_script("window.open('" + "" + "', '_blank');")
        window_handles.append(driver.window_handles[-1])
        time.sleep(gtime)

    if (Plugins[12] and function_combobox.currentText() ==Plugins[13]):
        driver.execute_script(
            "window.open('" + "" + "', '_blank');")
        window_handles.append(driver.window_handles[-1])
        time.sleep(gtime)

    if (Plugins[16] and function_combobox.currentText() == Plugins[17]):
        driver.execute_script("window.open('" + "" + "', '_blank');")
        window_handles.append(driver.window_handles[-1])
        time.sleep(gtime)

    
    driver.switch_to.window(original_window)

    
    check_driver_thread = threading.Thread(target=FunctionsGUI.check_driver_status)
    check_driver_thread.daemon = True
    check_driver_thread.start()

    return driver, window_handles

def Help_GUI(FunctionsGUI, settings, Save_Widget_Settings):
    from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
    from PyQt5.QtGui import QFont

    HelpPage_Widget = QWidget()
    section_layout = QVBoxLayout(HelpPage_Widget)
    section_layout.setContentsMargins(24, 8, 24, 8)
    section_layout.setSpacing(8)
    Widgets = []

    LabelText = QLabel("The Help page is a work in progress, please contact support or Michael Luckie, wmichluc, for any help needed")
    LabelText.setFont(QFont("Sans-serif", 22, weight=QFont.Bold))
    LabelText.setWordWrap(True)
    section_layout.addWidget(LabelText)

    return HelpPage_Widget

def Extra_GUI(FunctionsGUI, settings, Save_Widget_Settings):
    from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
    from PyQt5.QtGui import QFont

    Plugin_Widget = QWidget()
    section_layout = QVBoxLayout(Plugin_Widget)
    section_layout.setContentsMargins(8, 8, 8, 8)
    section_layout.setSpacing(8)
    Widgets = []

    LabelText = QLabel("The Extra page is a work in progress, please contact support or Michael Luckie, wmichluc, for any help needed")
    LabelText.setFont(QFont("Sans-serif", 22, weight=QFont.Bold))
    LabelText.setWordWrap(True)
    section_layout.addWidget(LabelText)

    return Plugin_Widget
