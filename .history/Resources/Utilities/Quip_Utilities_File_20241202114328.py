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

                print(f"Decrypted: {encrypted_path} -> {output_file}")
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
                print(f"Extracted ZIP: {zip_path} -> {output_folder}")
        except Exception as e:
            print(f"Error extracting {zip_path}: {e}")

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
        print(f"Detected file extension: {file_extension}")

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

# Load the utilities_file
utilities_file = Import_File("Utilities_File", "Resources/Test/Utilities/Utilities_File.zip")
print("Quip_Utilites")

# Assigning StopFunctionException and check_stop_event
StopFunctionException, check_stop_event = getattr(utilities_file, "StopFunctionException", None), getattr(utilities_file, "check_stop_event", None)

if not StopFunctionException:
    raise ImportError("The function 'StopFunctionException' was not found in Utilities_File.")
if not check_stop_event:
    raise ImportError("The function 'check_stop_event' was not found in Utilities_File.")

# ------------------------------------------- #

gtime = 0.25

# ---------------------------------------- #

def Quip_GetInfo_CellText(driver, row=0, column=0, stop_event=None):
    try:
        for attempt in range(9):
            check_stop_event(stop_event)
            try:
                # Construct the Numbers string
                Numbers = '-cell-' + str(row) + '-' + str(column)

                # Find the element by its class attribute
                input_element = driver.find_element(By.CSS_SELECTOR, '[id^="id-temp"][id$="' + Numbers + '"]')

                # Get the text content of the cell
                cell_text = input_element.text

                # If no exception occurred, return the cell text
                return cell_text

            except NoSuchElementException:
                cells = driver.find_elements(By.CLASS_NAME, 'spreadsheet-cell.react-cell.document-content.first-col')
                FixRow, FixCol = None, None

                for cell in cells:
                    check_stop_event(stop_event)
                    try:
                        cell_id = cell.get_attribute("id")
                        _, _, _, FixRow, FixCol = cell_id.split("-")
                        break
                    except ValueError:
                        print("ValueError")

                if FixRow is not None and FixCol is not None:
                    try:
                        Numbers = '-cell-' + str(FixRow) + '-' + str(FixCol)
                        input_element = driver.find_element(By.CSS_SELECTOR, '[id^="id-temp"][id$="' + Numbers + '"]')
                        input_element.click()

                        presses = int(FixRow) - row

                        if presses < 0:
                            pyautogui.press('down', presses=abs(presses) + 3)
                        elif presses > 0:
                            pyautogui.press('up', presses=presses + 3)

                    except NoSuchElementException:
                        print(f"Element with {Numbers} still not found.")
                else:
                    print("FixRow or FixCol not found, skipping this attempt.")
                    continue

            except UnboundLocalError:
                print("UnboundLocalError: Ensure FixRow and FixCol are defined before usage.")
                return False

        return False

    except (StopFunctionException, ElementClickInterceptedException, StaleElementReferenceException) as e:
        print(f"Exception occurred: {e}")
        return False

def Quip_ClickOn_Cell(driver, row=0, column=0, stop_event=None):
    def ExceptionFunction(driver, row, stop_event=None):
        try:
            # Find the element by its class attribute
            cells = driver.find_elements(By.CLASS_NAME, 'spreadsheet-cell.react-cell.document-content.first-col')
            for cell in cells:
                try:
                    cell_id = cell.get_attribute("id")
                    _, _, _, FixRow, FixCol = cell_id.split("-")
                    break
                except ValueError:
                    pass

            try:
                # Construct the Numbers string
                Numbers = '-cell-' + str(FixRow) + '-' + str(FixCol)

                # Find the element by its class attribute
                input_element = driver.find_element(By.CSS_SELECTOR, '[id^="id-temp"][id$="' + Numbers + '"]')
                input_element.click()

                # Calculate the number of times to press the down or up arrow
                presses = int(FixRow) - row

                # Press the down or up arrow that many times
                if presses < 0:
                    check_stop_event(stop_event)
                    while not stop_event.is_set():
                        pyautogui.press('down', presses=abs(presses)+3)
                        break
                    check_stop_event(stop_event)
                elif presses > 0:
                    check_stop_event(stop_event)
                    while not stop_event.is_set():
                        pyautogui.press('up', presses=presses + 3)
                        break
                    check_stop_event(stop_event)
            except UnboundLocalError:
                pass
        except StopFunctionException:
            return False

    try:
        for attempt in range(3):
            check_stop_event(stop_event)
            try:
                # Construct the Numbers string
                Numbers = '-cell-' + str(row) + '-' + str(column)

                # Find the element by its class attribute
                input_element = driver.find_element(By.CSS_SELECTOR, '[id^="id-temp"][id$="' + Numbers + '"]')
                input_element.click()

                return input_element
            except NoSuchElementException:
                if not ExceptionFunction(driver, row, stop_event=stop_event):
                    return False
            """except ElementClickInterceptedException:
                ExceptionFunction(driver, row, stop_event=stop_event)"""

    except (StopFunctionException, ElementClickInterceptedException, StaleElementReferenceException):
        return False

def Quip_ClickOn_Bucket(driver):
    try:
        # Find the button element with the label "Background Color"
        element = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Background Color"]')

        # Click on the button
        element.click()
    except NoSuchElementException:
        pyautogui.press('esc')
    except ElementClickInterceptedException:
        return

def Quip_Check_CommandLine(driver, row=0, column=0, stop_event=None):
    try:
        result = Quip_GetInfo_CellText(driver, row, column, stop_event=stop_event)
        if not result:
            return False
        result = str(result).lower()
        if result == "skip":
            print("Skip")
            return result
        elif result == "stopall":
            print("Stopall")
            return result
        else:
            print("Continue")
            return result
    except (StopFunctionException, ElementClickInterceptedException, StaleElementReferenceException):
        return False

def Quip_GetInfo_LegalName(driver, stop_event=None):
    try:
        check_stop_event(stop_event)
        pyautogui.hotkey('ctrl', 'f')
        check_stop_event(stop_event)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        check_stop_event(stop_event)
        pyautogui.press('enter')
        check_stop_event(stop_event)
        pyautogui.press('esc')
        check_stop_event(stop_event)
        pyautogui.press('left', presses=2)
        check_stop_event(stop_event)
        pyautogui.hotkey('ctrl', 'c')
        check_stop_event(stop_event)
        FirstName = str(pyperclip.paste())
        pyautogui.press('right')
        check_stop_event(stop_event)
        pyautogui.hotkey('ctrl', 'c')
        LastName = str(pyperclip.paste())
        check_stop_event(stop_event)
        MixedName = f"{LastName},{FirstName}"
        check_stop_event(stop_event)
        return True, MixedName, FirstName, LastName

    except (StopFunctionException, ElementClickInterceptedException, StaleElementReferenceException):
        return False, False, False, False

# --------------------------------------------------------------------------- #

def Quip_Color_Cells(driver, Color, WorkingRow, Column="0", Row=True, stop_event=None):
    try:
        try:
            pyautogui.press('esc')
            check_stop_event(stop_event)
            #time.sleep(gtime)
            Quip_ClickOn_Cell(driver, WorkingRow, Column, stop_event=stop_event)
            if Row:
                actions = ActionChains(driver)
                actions.key_down(Keys.SHIFT).send_keys(Keys.SPACE).key_up(Keys.SHIFT).perform()
            Quip_ClickOn_Bucket(driver)

            if Color == "None":
                driver.find_element(By.CLASS_NAME, 'color-clear-swatch.button.button-flex.bordered.clickable').click()
                pyautogui.press('down')
                check_stop_event(stop_event)
                time.sleep(gtime)
            else:
                # Capitalize the first letter of the color string
                Color = Color.lower()
                formatted_color = Color.capitalize()

                driver.find_element(By.CSS_SELECTOR, f'div.color-swatch[title="{formatted_color}"]').click()
                pyautogui.press('down')
                check_stop_event(stop_event)
                #time.sleep(gtime)
        except NoSuchElementException:
            pyautogui.press('esc')
    except (StopFunctionException, ElementClickInterceptedException, StaleElementReferenceException):
        return False