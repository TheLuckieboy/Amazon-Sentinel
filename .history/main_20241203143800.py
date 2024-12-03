import pyautogui, threading, keyboard, time, json, string, pyperclip, logging, datetime, os, sys, zipfile, importlib.util, shutil
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QGridLayout, QStackedWidget, QWidget, \
    QTextEdit, QComboBox, QHBoxLayout, QLineEdit, QCheckBox, QSpacerItem, QSizePolicy, QMessageBox, QCompleter, \
    QFrame, QVBoxLayout
from PyQt5.QtGui import QPixmap, QIcon, QFont, QRegExpValidator, QIntValidator, QColor, QPainter, QPen, QPainterPath
from PyQt5.QtCore import QSize, QRect, Qt, pyqtSignal, QRegExp, QPoint
from PyQt5 import QtCore, QtGui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException

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

def save_settings_to_json():
    # Define the path to settings.json
    settings_path = resource_path(os.path.join("Resources", "settings.json"))

    # Save the updated settings back to the file
    with open(settings_path, "w") as f:
        json.dump(settings, f, indent=4)

def load_settings():
    try:
        # Define the path to settings.json
        settings_path = resource_path(os.path.join("Resources", "settings.json"))

        # Open and load the settings from the file
        with open(settings_path, "r") as f:
            return json.load(f)

    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Error decoding JSON from settings file.")
        return {}

def Save_Widget_Settings(widgets):
    if not isinstance(widgets, list):
        widgets = [widgets]

    for widget in widgets:
        widget_name = widget.objectName()

        # Save line edit text
        if hasattr(widget, "line_edit"):
            settings[widget_name] = widget.line_edit.text()

        # Save combo box 1 text
        elif hasattr(widget, "combo_box1") and not (hasattr(widget, "button") or hasattr(widget, "checkmark")):
            settings[widget_name] = widget.combo_box1.currentText()

        # Save combo box 2 text
        elif hasattr(widget, "combo_box2") and not (hasattr(widget, "button") or hasattr(widget, "checkmark")):
            settings[widget_name] = widget.combo_box2.currentText()

        # Save checkmark state and combo boxes text
        elif hasattr(widget, "checkmark"):
            checkmark_state = widget.checkmark.isChecked()
            if hasattr(widget, "combo_box1") and hasattr(widget, "combo_box2"):
                combo_box1_text = widget.combo_box1.currentText()
                combo_box2_text = widget.combo_box2.currentText()
                settings[widget_name] = checkmark_state, combo_box1_text, combo_box2_text
            elif hasattr(widget, "combo_box1"):
                combo_box1_text = widget.combo_box1.currentText()
                settings[widget_name] = checkmark_state, combo_box1_text
            elif hasattr(widget, "combo_box2"):
                combo_box2_text = widget.combo_box2.currentText()
                settings[widget_name] = checkmark_state, combo_box2_text
            else:
                settings[widget_name] = checkmark_state

        # Save button states
        elif hasattr(widget, "button"):
            button_state = widget.button.isChecked()
            if hasattr(widget, "button2"):
                button2_state = widget.button2.isChecked()
                if hasattr(widget, "combo_box1") and hasattr(widget, "combo_box2"):
                    settings[
                        widget_name] = button_state, button2_state, widget.combo_box1.currentText(), widget.combo_box2.currentText()
                elif hasattr(widget, "combo_box1"):
                    settings[widget_name] = button_state, button2_state, widget.combo_box1.currentText()
                elif hasattr(widget, "combo_box2"):
                    settings[widget_name] = button_state, button2_state, widget.combo_box2.currentText()
                else:
                    settings[widget_name] = button_state, button2_state
            else:
                if hasattr(widget, "combo_box1") and hasattr(widget, "combo_box2"):
                    settings[
                        widget_name] = button_state, widget.combo_box1.currentText(), widget.combo_box2.currentText()
                elif hasattr(widget, "combo_box1"):
                    settings[widget_name] = button_state, widget.combo_box1.currentText()
                elif hasattr(widget, "combo_box2"):
                    settings[widget_name] = button_state, widget.combo_box2.currentText()
                else:
                    settings[widget_name] = button_state

        else:
            print("Can't Save Widget", widget_name)

    save_settings_to_json()

settings = load_settings()

class BasePage(QMainWindow):
    page_stack = None
    sidebar_expanded = False
    sidebar_expanded_changed = pyqtSignal(bool)
    page_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sentinel V0.0.2")
        # self.setMinimumSize(1202, 310)
        # self.setMaximumSize(1920, 1080)
        self.setFixedSize(1280, 720)
        self.setWindowIcon(QIcon(Icon_Image))

        self.setup_sidebar()
        self.setup_corner_images()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        def position_corner_images():
            rect = self.rect()

            bottom_left_x = 0
            bottom_left_y = rect.height() - self.bottom_left_label.pixmap().height()
            self.bottom_left_label.setGeometry(bottom_left_x, bottom_left_y,
                                               self.bottom_left_label.pixmap().width(),
                                               self.bottom_left_label.pixmap().height())

            bottom_right_x = rect.width() - self.bottom_right_label.pixmap().width()
            bottom_right_y = rect.height() - self.bottom_right_label.pixmap().height()
            self.bottom_right_label.setGeometry(bottom_right_x, bottom_right_y,
                                                self.bottom_right_label.pixmap().width(),
                                                self.bottom_right_label.pixmap().height())

        self.SideBar_Widget_Icon.setGeometry(30, 30, 0, ((self.height()) - 60))
        self.SideBar_Widget_IconWithDescription.setGeometry(30, 30, 0, ((self.height()) - 60))
        position_corner_images()

    def paintEvent(self, event):
        BORDER_COLOR = QColor("#3c9ef9")
        BORDER_THICKNESS = 30

        painter = QPainter(self)
        rect = self.rect()

        painter.setPen(BORDER_COLOR)
        painter.setBrush(BORDER_COLOR)

        painter.drawRect(0, 0, BORDER_THICKNESS, rect.height())  # Left
        painter.drawRect(rect.width() - BORDER_THICKNESS, 0, BORDER_THICKNESS, rect.height())  # Right
        painter.drawRect(0, 0, rect.width(), BORDER_THICKNESS)  # Top
        painter.drawRect(0, rect.height() - BORDER_THICKNESS, rect.width(), BORDER_THICKNESS)  # Bottom

    def switch_page(self, index):
        self.page_changed.emit(index)
        self.page_stack.setCurrentIndex(index)
        settings["Page_Stack_Index"] = self.page_stack.currentIndex()
        save_settings_to_json()

    # ----------------------------------------------------------------------------------------------- #

    def setup_sidebar(self):
        self.SideBar_Widget_Icon = self.create_sidebar_widget(50)
        self.SideBar_Widget_IconWithDescription = self.create_sidebar_widget(200)
        self.SideBar_Widget_IconWithDescription.hide()

        self.setup_sidebar_buttons()

    def create_sidebar_widget(self, width):
        sidebar_widget = QWidget(self)
        sidebar_widget.setStyleSheet("background-color: #3c69f9;")
        sidebar_widget.setFixedWidth(width)

        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        return sidebar_widget

    def setup_button(self, icon_path, size, object_name, stylesheet, page=None):
        button = QPushButton("", self)
        icon = QIcon(icon_path)
        button.setIcon(icon)
        button.setIconSize(QSize(size, 50))
        button.setObjectName(object_name)
        button.setStyleSheet(stylesheet)
        if page is not None:
            button.clicked.connect(lambda: self.switch_page(page))
        else:
            button.clicked.connect(self.toggle_sidebar_state)
        return button

    def setup_sidebar_buttons(self):
        icons = [
            (icons_WO_desc1, "BurgerMenuButton"),
            (icons_WO_desc2, "functionsButton", 0),
            (icons_WO_desc3, "helpButton", 1),
            (icons_WO_desc4, "extraButton", 2),
        ]

        icons_with_desc = [
            (icons_with_desc1, "BurgerMenuButton"),
            (icons_with_desc2, "functionsButton", 0),
            (icons_with_desc3, "helpButton", 1),
            (icons_with_desc4, "extraButton", 2),
        ]

        self.add_buttons_to_sidebar(self.SideBar_Widget_Icon, icons, 50)
        self.add_buttons_to_sidebar(self.SideBar_Widget_IconWithDescription, icons_with_desc, 200)

    def add_buttons_to_sidebar(self, sidebar_widget, icons, Xsize):
        sidebar_layout = sidebar_widget.layout()

        for icon in icons:
            if len(icon) == 3:
                button = self.setup_button(icon[0], Xsize, icon[1], stylesheet, icon[2])
            else:
                button = self.setup_button(icon[0], Xsize, icon[1], stylesheet)
            sidebar_layout.addWidget(button)

            if icon[1] == "helpButton":
                sidebar_layout.addStretch(1)

    def setup_corner_images(self):
        self.bottom_left_label = QLabel(self)
        self.bottom_right_label = QLabel(self)

        self.bottom_left_label.setPixmap(QPixmap(bottom_left_image_path))
        self.bottom_right_label.setPixmap(QPixmap(bottom_right_image_path))

        self.bottom_left_label.setStyleSheet("background: transparent;")
        self.bottom_right_label.setStyleSheet("background: transparent;")

    def toggle_sidebar_state(self):
        self.sidebar_expanded = not self.sidebar_expanded
        self.sidebar_expanded_changed.emit(self.sidebar_expanded)  # Emit the signal when the variable is updated
        self.toggle_sidebar()

    def toggle_sidebar(self):
        if self.sidebar_expanded:
            self.SideBar_Widget_Icon.hide()
            self.SideBar_Widget_IconWithDescription.show()
        else:
            self.SideBar_Widget_Icon.show()
            self.SideBar_Widget_IconWithDescription.hide()

class FunctionsGUI(BasePage):
    def __init__(self, parent=None):
        super().__init__()
        self.driver, self.window_handles, self.DriverIsPresentlyOpen = "DoesNotExist", [], False
        self.kill_switch_active = False
        self.Confirm_Function_Variable = False
        self.Script_Widgets = []

        self.main_widget = QWidget(self)
        self.main_widget.lower()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(80, 30, 30, 30)
        self.main_layout.setSpacing(0)

        self.grid_layout = QGridLayout()

        self.Plugin_Settings()
        self.Execution_Output()
        self.Script_Configuration()
        self.Script_Specific_Settings()
        self.Description_Changed()

        self.main_layout.addLayout(self.grid_layout)
        self.setCentralWidget(self.main_widget)

        # Start the keyboard listener in a thread
        self.keyboard_listener_thread = threading.Thread(target=self.start_keyboard_listener)
        self.keyboard_listener_thread.start()

    def Plugin_Settings(self):
        # Access the Plugins function dynamically
        Plugin_Settings = getattr(utilities_file, "Plugin_Settings", None)
        if not Plugin_Settings:
            raise ImportError("The function 'Plugins' was not found in Utilities_File.")

        # Use the Plugins function
        self.Plugins = Plugin_Settings(settings)
        self.Length_Plugins = len(self.Plugins) // 4

    def Execution_Output(self):
        self.Confirm_Function_Green = None
        self.Confirm_Function_Red = None
        self.Confirm_Function = None

        # Create the main widget and layout for this section
        self.Execution_Output_section_widget = QWidget()
        self.Execution_Output_section_widget.setFixedWidth(419)

        section_layout = QHBoxLayout(self.Execution_Output_section_widget)
        section_layout.setContentsMargins(0, 8, 8, 8)
        section_layout.setSpacing(8)

        def Function_Section():
            Function_Section = QWidget()
            Function_Section_Layout = QVBoxLayout(Function_Section)
            Function_Section_Layout.setContentsMargins(8, 0, 0, 0)
            Function_Section_Layout.setSpacing(8)

            def Confirm_Function_Image():
                self.Confirm_Function_Red = QLabel()
                red_pixmap = QPixmap(Red_Confirmation_Img)
                self.Confirm_Function_Red.setPixmap(red_pixmap)
                self.Confirm_Function_Red.setFixedSize(red_pixmap.size())
                self.Confirm_Function_Red.setAlignment(Qt.AlignCenter)

                self.Confirm_Function_Green = QLabel()
                green_pixmap = QPixmap(Green_Confirmation_Img)
                self.Confirm_Function_Green.setPixmap(green_pixmap)
                self.Confirm_Function_Green.setFixedSize(red_pixmap.size())
                self.Confirm_Function_Green.setAlignment(Qt.AlignCenter)
                self.Confirm_Function_Green.hide()

                Function_Section_Layout.addWidget(self.Confirm_Function_Red)
                Function_Section_Layout.addWidget(self.Confirm_Function_Green)

            Confirm_Function_Image()

            def Confirm_Function_Buttons():
                layout = QVBoxLayout()
                layout.setSpacing(8)

                buttons = [
                    ('Kill Confirmation', 'Kill_Confirmation'),
                    ('Open Chrome', 'Open_Chrome'),
                    ('Open Firefox', 'Open_Firefox'),
                    ('Open Edge', 'Open_Edge'),
                    ('Open Excel', 'Open_Excel'),
                ]
                Buttons = []

                self.Confirm_Function = QPushButton("Confirm Function")
                self.Confirm_Function.setFixedSize(146, 30)
                self.Confirm_Function.setObjectName("Confirm_Function")
                self.Confirm_Function.setCheckable(True)
                self.Confirm_Function.setChecked(False)
                layout.addWidget(self.Confirm_Function, alignment=Qt.AlignCenter)
                Buttons.append(self.Confirm_Function)

                for (text, name) in buttons:
                    button = QPushButton(text)
                    button.setFixedSize(146, 30)
                    button.setObjectName(name)
                    if 'Open' in text:
                        button.clicked.connect(lambda _, b=name: self.Kill_Confirmation_Function())
                        button.clicked.connect(lambda _, b=name: self.Open_Browser(**{b.split('_')[1]: True}))
                    layout.addWidget(button, alignment=Qt.AlignCenter)
                    if 'Kill Confirmation' in text:
                        # Add a spacer to force the buttons closer together
                        spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
                        layout.addItem(spacer)
                    Buttons.append(button)

                Function_Section_Layout.addLayout(layout)
                return Buttons

            Buttons = Confirm_Function_Buttons()

            section_layout.addWidget(Function_Section)

            return Buttons

        def Console_widget_Function():
            # Create a QTextEdit widget for displaying print statements
            #self.console_widget = QTextEdit()
            #self.console_widget.setReadOnly(True)
            self.console_widget = QWidget()
            self.console_widget.setFixedSize(250, 644)

            # Ensure auto-scrolling to the bottom
            #scrollbar = self.console_widget.verticalScrollBar()
            #scrollbar.setValue(scrollbar.maximum())

            # Add the console widget to the layout
            section_layout.addWidget(self.console_widget)

        Console_widget_Function()
        section_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        Button_Widgets = Function_Section()

        def Button_Signals(button):
            sender = button
            if sender == Confirm_Function:
                self.Confirm_Function.setChecked(True)
                self.Confirm_Function_Variable = True
                self.Confirm_Function_Red.hide()
                self.Confirm_Function_Green.show()
            if sender == Kill_Confirmation:
                self.Kill_Confirmation_Function()

        for Button in Button_Widgets:
            if Button.objectName() == "Confirm_Function":
                Confirm_Function = Button
                Confirm_Function.clicked.connect(lambda state, b=Button: Button_Signals(b))
            if Button.objectName() == "Kill_Confirmation":
                Kill_Confirmation = Button
                Kill_Confirmation.clicked.connect(lambda state, b=Button: Button_Signals(b))

        # Add the section widget to the main grid layout
        self.grid_layout.addWidget(self.Execution_Output_section_widget, 0, 1, 2, 1)

    def Script_Configuration(self):
        """if hasattr(self, 'Script_Configuration_section_widget') and self.Script_Configuration_section_widget:
            # Destroy the existing widget if it exists
            self.Script_Configuration_section_widget.hide()
            self.Script_Configuration_section_widget.deleteLater()
            self.Script_Configuration_section_widget = None"""

        self.Keyboard_Listener_Widget1 = None
        self.Keyboard_Listener_Widget2 = None

        self.Script_Configuration_section_widget = QWidget()
        self.Script_Configuration_section_widget.setFixedHeight(142)

        section_layout = QHBoxLayout(self.Script_Configuration_section_widget)
        section_layout.setContentsMargins(8, 8, 0, 0)
        section_layout.setSpacing(0)

        section_layoutA = QVBoxLayout()
        section_layoutA.setContentsMargins(0, 0, 4, 0)
        section_layoutA.setSpacing(8)

        section_layoutB = QVBoxLayout()
        section_layoutB.setContentsMargins(4, 0, 8, 8)
        section_layoutB.setSpacing(8)

        self.Script_Configuration_Widgets_List = []

        def Combo_box_Function():
            Layout = QHBoxLayout()
            Layout.setSpacing(8)

            function_combobox = QComboBox()
            function_names = []

            index1 = 0
            index2 = 1

            for _ in range(self.Length_Plugins):
                if self.Plugins[index1]:
                    function_names.append(self.Plugins[index2])
                index1 = index1 + 4
                index2 = index2 + 4

            function_combobox.addItems(function_names)
            function_combobox.setStyleSheet("background-color: lightgray;")
            function_combobox.setFont(QFont("Arial", 12))
            function_combobox.setFixedSize(300, 30)

            # Set the initial index from settings
            function_combobox.setCurrentText(settings.get("function_combobox", "Invalid"))

            def Save_Update():
                settings["function_combobox"] = function_combobox.currentText()
                save_settings_to_json()

            # Connect the signal to the Save_Update function
            function_combobox.currentTextChanged.connect(lambda: Save_Update())
            function_combobox.currentTextChanged.connect(lambda: self.Description_Changed())
            function_combobox.currentTextChanged.connect(lambda: self.Kill_Confirmation_Function())

            def ScriptExplination_Overlay():
                Selected_Function = function_combobox.currentText()
                message = None
                index2 = 1
                index4 = 3

                for _ in range(self.Length_Plugins):
                    if Selected_Function == self.Plugins[index2]:
                        message = self.Plugins[index4]
                    index2 = index2 + 4
                    index4 = index4 + 4

                self.overlay = QWidget(self)
                self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 200);")
                self.overlay.setGeometry(0, 0, self.width(), self.height())
                Font = QFont("Sans-serif", 14, weight=QFont.Bold)

                vertical_layout = QVBoxLayout(self.overlay)
                vertical_layout.addItem(QSpacerItem(40, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))
                vertical_layout.setContentsMargins(0, 0, 0, 0)
                vertical_layout.setSpacing(20)

                message_label = QLabel(message, self.overlay)
                message_label.setStyleSheet("color: white;")
                message_label.setFont(Font)
                message_label.setWordWrap(True)
                vertical_layout.addWidget(message_label, alignment=Qt.AlignCenter)
                vertical_layout.addItem(QSpacerItem(0, 400, QSizePolicy.Expanding, QSizePolicy.Minimum))

                exit_label = QLabel(f'Press "esc" to close overlay', self.overlay)
                exit_label.setStyleSheet("color: white;")
                exit_label.setFont(Font)
                vertical_layout.addWidget(exit_label, alignment=Qt.AlignCenter)
                vertical_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

                self.overlay.show()

            More_Info = QPushButton("?")
            More_Info.setFixedSize(30, 30)
            More_Info.setObjectName("More_Info")
            More_Info.clicked.connect(lambda: ScriptExplination_Overlay())
            More_Info.clicked.connect(lambda: self.Kill_Confirmation_Function())

            # Add widgets to the layouts
            Layout.addWidget(function_combobox)
            Layout.addWidget(More_Info)
            section_layoutA.addLayout(Layout)

            #self.Script_Configuration_Widgets_List.append(function_combobox)
            return function_combobox

        def Toggle_Buttons():
            Layout = QHBoxLayout()
            Layout.setSpacing(8)

            def toggle_buttons():
                sender = QApplication.instance().sender()
                self.Kill_Confirmation_Function()
                if sender == Quip_Database.button:
                    Quip_Database.button.setChecked(True)
                    Excel_Database.button.setChecked(False)
                elif sender == Excel_Database.button:
                    Quip_Database.button.setChecked(False)
                    Excel_Database.button.setChecked(True)
                Save_Widget_Settings(self.Script_Configuration_Widgets_List)

            # Create Toggle Buttons
            Quip_Database = self.Widget_Creator(ButtonLabel='Quip DataBase', ButtonWidget=True)
            Quip_Database.button.setChecked(settings.get("Quip_Database", False))
            Quip_Database.button.clicked.connect(toggle_buttons)
            Quip_Database.setObjectName("Quip_Database")
            Quip_Database.button.setFixedSize(165, 50)
            Layout.addWidget(Quip_Database)

            Excel_Database = self.Widget_Creator(ButtonLabel='Excel DataBase', ButtonWidget=True)
            Excel_Database.button.setChecked(settings.get("Excel_Database", False))
            Excel_Database.button.clicked.connect(toggle_buttons)
            Excel_Database.setObjectName("Excel_Database")
            Excel_Database.button.setFixedSize(165, 50)
            Layout.addWidget(Excel_Database)

            self.Script_Configuration_Widgets_List.append(Quip_Database)
            self.Script_Configuration_Widgets_List.append(Excel_Database)
            section_layoutA.addLayout(Layout)

        def Starting_Row():
            Layout = QHBoxLayout()
            Layout.setSpacing(8)
            Widget_list = []

            self.Starting_Row_Widget = self.Widget_Creator("Starting Row:", Font_Size=8, Line_Edit=50, EditBox=True, IntValidator=True)
            self.Starting_Row_Widget.setFixedSize(165, 30)
            self.Starting_Row_Widget.setObjectName("Starting Row")
            Layout.addWidget(self.Starting_Row_Widget)

            Command_Line_Widget = self.Widget_Creator("Command\nLine Column:", Column_Letter_Box=True, Font_Size=7)
            Command_Line_Widget.setFixedSize(165, 30)
            Command_Line_Widget.setObjectName("CommandLine Column")
            Layout.addWidget(Command_Line_Widget)

            self.Script_Configuration_Widgets_List.append(self.Starting_Row_Widget)
            self.Script_Configuration_Widgets_List.append(Command_Line_Widget)
            section_layoutA.addLayout(Layout)

            return self.Starting_Row_Widget

        self.function_combobox = Combo_box_Function()
        Toggle_Buttons()
        self.Starting_Row_Widget = Starting_Row()

        # Add a spacer to force the combo box and buttons closer together
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        section_layoutA.addItem(spacer)

        def Keyboard_Listener_Keys():
            Layout = QVBoxLayout()
            Layout.setSpacing(8)

            """Advanced_Settings_Button = self.Widget_Creator(ButtonLabel='Advanced Settings', Font_Size=7, ButtonWidget=True)
            #Advanced_Settings_Button.button.clicked.connect(toggle_buttons)
            Advanced_Settings_Button.setObjectName("Advanced_Settings_Button")
            Advanced_Settings_Button.button.setFixedHeight(40)
            Layout.addWidget(Advanced_Settings_Button)

            spacer = QSpacerItem(0, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            Layout.addItem(spacer)"""

            self.Keyboard_Listener_Widget1 = self.Widget_Creator("Run Function Key", Font_Size=9, Line_Edit=200,
                                                                 EditBox=True, StrValidator=True)
            self.Keyboard_Listener_Widget1.setFixedHeight(35)
            self.Keyboard_Listener_Widget1.setObjectName("Run Function Key")
            self.Keyboard_Listener_Widget1.line_edit.editingFinished.connect(
                lambda: self.restart_keyboard_listener())
            self.Script_Configuration_Widgets_List.append(self.Keyboard_Listener_Widget1)
            Layout.addWidget(self.Keyboard_Listener_Widget1)

            self.Keyboard_Listener_Widget2 = self.Widget_Creator("Kill Switch Key", Font_Size=9, Line_Edit=200,
                                                                 EditBox=True, StrValidator=True)
            self.Keyboard_Listener_Widget2.setFixedHeight(35)
            self.Keyboard_Listener_Widget2.setObjectName("Kill Switch Key")
            self.Keyboard_Listener_Widget2.line_edit.editingFinished.connect(
                lambda: self.restart_keyboard_listener())
            self.Script_Configuration_Widgets_List.append(self.Keyboard_Listener_Widget2)
            Layout.addWidget(self.Keyboard_Listener_Widget2)

            section_layoutB.addLayout(Layout)

        Keyboard_Listener_Keys()

        # Add the vertical layouts to the horizontal layout
        section_layout.addLayout(section_layoutA, 3)
        section_layout.addLayout(section_layoutB, 1)

        # Add the section_widget to the grid layout
        self.grid_layout.addWidget(self.Script_Configuration_section_widget, 0, 0)
        self.connect_widget_signals(self.Script_Configuration_Widgets_List, settings, Save_Widget_Settings)

    def Script_Specific_Settings(self):
        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)
        section_layout.setContentsMargins(0, 0, 0, 0)
        section_layout.setSpacing(0)

        index1 = 0

        # Access the Plugin_Widget_Setup Function
        Plugin_Widget_Setup = getattr(utilities_file, "Plugin_Widget_Setup", None)
        if not Plugin_Widget_Setup:
            raise ImportError("The function 'Plugin_Widget_Setup' was not found in Utilities_File.")

        for _ in range(self.Length_Plugins):
            if self.Plugins[index1]:
                widget = QWidget()
                Script_Widget = Plugin_Widget_Setup(self, widget, settings, Save_Widget_Settings, self.grid_layout, self.Script_Widgets, index1)
                section_layout.addWidget(Script_Widget)
                self.Script_Widgets.append(Script_Widget)
            else:
                self.Script_Widgets.append("BlankIndex1")
                self.Script_Widgets.append("BlankIndex2")
            index1 = index1 + 4

        self.grid_layout.addWidget(section_widget, 1, 0)

    def Hide_Main_Widgets(self, Hide=True):
        self.Hide_Script_Widgets()
        Selected_Function = self.function_combobox.currentText()
        if Hide:
            self.Script_Configuration_section_widget.hide()
            self.Execution_Output_section_widget.hide()
        else:
            self.Script_Configuration_section_widget.show()
            self.Execution_Output_section_widget.show()

            index2 = 1
            Script = 1

            for _ in range(self.Length_Plugins):
                if Selected_Function == self.Plugins[index2]:
                    try:
                        self.Script_Widgets[Script].show()
                        break
                    except (AttributeError, IndexError):
                        pass
                index2 = index2 + 4
                Script = Script + 2

    def Hide_Script_Widgets(self):
        for widget in self.Script_Widgets:
            if widget != "BlankIndex1":
                if widget != "BlankIndex2":
                    widget.hide()

    def Description_Changed(self):
        Selected_Function = self.function_combobox.currentText()
        self.Hide_Script_Widgets()

        index2 = 1
        Script = 1

        for _ in range(self.Length_Plugins):
            if Selected_Function == self.Plugins[index2]:
                try:
                    self.Script_Widgets[Script].show()
                    break
                except (AttributeError, IndexError):
                    pass
            index2 = index2 + 4
            Script = Script + 2

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and self.overlay:
            self.overlay.hide()

    # ------------------------------------------------------------------------------------------------ #

    def Widget_Creator(self, label_text="Add Label", label_text2="Add Label", ButtonLabel="Add Label",
                       ButtonLabel2="Add Label",
                       Title_Label=False, Checkmark=False, Column_Letter_Box=False, Quip_Color_Box=False,
                       SiteLocation=False,
                       EditBox=False, Add_QLabel_Left=False, Add_QLabel_Right=False, ButtonWidget=False,
                       ButtonWidget2=False,
                       IntValidator=False, StrValidator=False, Font_Size=6, Line_Edit=150, Button_Width=None,
                       Button_Width2=None):

        widget = QWidget(self)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        Color_List = ([
            "Gray80", "Gray60", "Gray30", "Gray10", "Gray5", "White",
            "Red80", "Red60", "Red40", "Red20", "Red10", "Red5",
            "Orange70", "Orange60", "Orange50", "Orange20", "Orange10", "Orange5",
            "Yellow70", "Yellow60", "Yellow50", "Yellow20", "Yellow10", "Yellow5",
            "Gold70", "Gold60", "Gold40", "Gold20", "Gold10", "Gold5",
            "Green70", "Green60", "Green50", "Green20", "Green10", "Green5",
            "Cyan80", "Cyan60", "Cyan40", "Cyan20", "Cyan10", "Cyan5",
            "Blue80", "Blue60", "Blue40", "Blue20", "Blue10", "Blue5",
            "Purple80", "Purple60", "Purple40", "Purple20", "Purple10", "Purple5",
            "Magenta80", "Magenta60", "Magenta40", "Magenta20", "Magenta10", "Magenta5"
        ])
        ColumnLetter_List = [letter for letter in string.ascii_uppercase]

        def Add_QLabel(layout, widget):
            widget.label = QLabel(label_text, self)
            widget.label.setFont(QFont("Sans-serif", Font_Size, weight=QFont.Bold))
            layout.addWidget(widget.label)
            layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        if Checkmark and not Title_Label:
            widget.checkmark = QCheckBox(widget)
            widget.checkmark.stateChanged.connect(lambda: self.Kill_Confirmation_Function())
            layout.addWidget(widget.checkmark)
        if Column_Letter_Box and Quip_Color_Box:
            Add_QLabel(layout, widget)
            self.addComboBox(layout, widget, ColumnLetter_List, Color_List, Checkmark)
        elif Column_Letter_Box and not ButtonWidget:
            Add_QLabel(layout, widget)
            self.addComboBox(layout, widget, ColumnLetter_List, None, Checkmark)
        elif Quip_Color_Box:
            Add_QLabel(layout, widget)
            self.addComboBox(layout, widget, None, Color_List, Checkmark)
        elif SiteLocation:
            Add_QLabel(layout, widget)

            try:
                # Import the encrypted and zipped Site_Locations.txt
                Site_Location_List_Content = Import_File("Site_Locations", resource_path(os.path.join("Resources/Test/Utilities/Site_Locations.zip")))

                # Parse the file contents into a list
                Site_Location_List = [
                    line.strip() for line in Site_Location_List_Content.splitlines()
                ]

            except FileNotFoundError:
                Site_Location_List = []
                print("Site_Locations.txt file not found or could not be loaded.")
            except Exception as e:
                Site_Location_List = []
                print(f"An error occurred while loading Site_Locations.txt: {e}")


            self.addComboBox(layout, widget, None, Site_Location_List, Checkmark)
        elif Title_Label:
            Add_QLabel(layout, widget)
            widget.button = QPushButton()
            widget.button.setCheckable(True)
            widget.button.clicked.connect(lambda: self.Kill_Confirmation_Function())
            if ButtonLabel:
                widget.button.setText(ButtonLabel)
            if Button_Width:
                widget.button.setFixedWidth(Button_Width)
            layout.addWidget(widget.button)
        elif ButtonWidget:
            if Add_QLabel_Left:
                Add_QLabel(layout, widget)
            widget.button = QPushButton(ButtonLabel)
            widget.button.setCheckable(True)
            widget.button.clicked.connect(lambda: self.Kill_Confirmation_Function())
            if Button_Width:
                widget.button.setFixedWidth(Button_Width)
            layout.addWidget(widget.button)
            if ButtonWidget2:
                widget.button2 = QPushButton(ButtonLabel2)
                widget.button2.setCheckable(True)
                widget.button2.clicked.connect(lambda: self.Kill_Confirmation_Function())
                if Button_Width2:
                    widget.button.setFixedWidth(Button_Width2)
                layout.addWidget(widget.button2)
            if Add_QLabel_Right:
                Add_QLabel(layout, widget)
            if Column_Letter_Box:
                self.addComboBox(layout, widget, ColumnLetter_List)
        elif EditBox:
            Add_QLabel(layout, widget)
            self.addLineEdit(layout, widget, Line_Edit, IntValidator, StrValidator)
        else:
            Add_QLabel(layout, widget)

        return widget

    def addComboBox(self, layout, widget, itemList1, itemList2=None, Checkmark=False):
        Font = QFont("Sans-serif", 8, weight=QFont.Bold)
        if itemList1:
            def Edit_Valiadator():
                current_text = widget.combo_box1.currentText()
                if current_text not in itemList1:
                    widget.combo_box1.clear()
                    widget.combo_box1.addItems(itemList1)
                    widget.combo_box1.setCurrentIndex(0)

            def Change_Valiadator():
                current_text = widget.combo_box1.currentText()
                if (any(char.isdigit() for char in current_text)) or (len(current_text) > 1):
                    if len(current_text) > 1:
                        # Keep only the first character if it's a letter
                        first_char = current_text[0]
                        if first_char.isalpha():
                            widget.combo_box1.lineEdit().setText(first_char)
                        else:
                            widget.combo_box1.setCurrentIndex(0)
                    else:
                        widget.combo_box1.setCurrentIndex(0)

            widget.combo_box1 = QComboBox(self)
            widget.combo_box1.setEditable(True)
            widget.combo_box1.addItems(itemList1)
            widget.combo_box1.setFont(Font)
            widget.combo_box1.setMinimumWidth(50)
            widget.combo_box1.view().setMinimumWidth(75)
            widget.combo_box1.setMaxVisibleItems(5)
            widget.combo_box1.currentTextChanged.connect(lambda: self.Kill_Confirmation_Function())
            widget.combo_box1.lineEdit().editingFinished.connect(lambda: Edit_Valiadator())
            widget.combo_box1.lineEdit().textChanged.connect(lambda: Change_Valiadator())
            completer = QCompleter(itemList1, widget.combo_box1)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            completer.popup().setStyleSheet("background-color: #dddddd;")
            completer.popup().setFont(Font)
            widget.combo_box1.setCompleter(completer)
            layout.addWidget(widget.combo_box1)

        if itemList2:
            def Valiadator():
                if widget.combo_box2.currentText() not in itemList2:
                    widget.combo_box2.clear()
                    widget.combo_box2.addItems(itemList2)
                    widget.combo_box2.setCurrentIndex(0)

            widget.combo_box2 = QComboBox(self)
            widget.combo_box2.setEditable(True)
            widget.combo_box2.addItems(itemList2)
            widget.combo_box2.setFont(Font)
            widget.combo_box2.setMinimumWidth(130)
            widget.combo_box2.view().setMinimumWidth(150)
            widget.combo_box2.setMaxVisibleItems(5)
            widget.combo_box2.currentTextChanged.connect(lambda: self.Kill_Confirmation_Function())
            widget.combo_box2.lineEdit().editingFinished.connect(lambda: Valiadator())
            completer2 = QCompleter(itemList2, widget.combo_box2)
            completer2.setCaseSensitivity(Qt.CaseInsensitive)
            completer2.popup().setStyleSheet("background-color: #dddddd;")
            completer2.popup().setFont(Font)
            widget.combo_box2.setCompleter(completer2)
            layout.addWidget(widget.combo_box2)

        if Checkmark:
            if itemList1:
                widget.combo_box1.setEnabled(False)
                widget.checkmark.stateChanged.connect(
                    lambda state: widget.combo_box1.setEnabled(state == Qt.Checked))
            if itemList2:
                widget.combo_box2.setEnabled(False)
                widget.checkmark.stateChanged.connect(
                    lambda state: widget.combo_box2.setEnabled(state == Qt.Checked))

    def addLineEdit(self, layout, widget, Line_Edit, IntValidator, StrValidator):
        def StrValidator_function():
            text = widget.line_edit.text()
            parts = text.split('+')
            capitalized_parts = [part.capitalize() for part in parts]
            capitalized_text = '+'.join(capitalized_parts)

            if capitalized_text in ("Ctrl+C", "Ctrl+V", "Alt+Tab", "Shift+Tab", "Alt+F4"):
                widget.line_edit.setText("")
            else:
                widget.line_edit.setText(capitalized_text)  # Set the capitalized text back to the line edit

        def IntValidator_function():
            entered_number = widget.line_edit.text().strip()

            if not entered_number:
                return

            # Ensure the entered input consists only of digits
            if not entered_number.isdigit():
                widget.line_edit.setText("2")
                return

            if entered_number.startswith('0') or '+' in entered_number:
                entered_number = entered_number.lstrip('0').replace('+', '')
                widget.line_edit.setText(entered_number)
            elif int(entered_number) < 1:
                widget.line_edit.setText("2")
            elif int(entered_number) > 9999:
                FourDigitNumber = entered_number[:4]
                widget.line_edit.setText(FourDigitNumber)

        def EditingFinished_function():
            entered_number = widget.line_edit.text().strip()
            if not entered_number:
                widget.line_edit.setText("2")
            elif int(entered_number) < 2:
                widget.line_edit.setText("2")
            elif int(entered_number) > 9999:
                FourDigitNumber = entered_number[:4]
                widget.line_edit.setText(FourDigitNumber)

        widget.line_edit = QLineEdit(self)
        widget.line_edit.setMaximumWidth(Line_Edit)
        widget.line_edit.setFont(QFont("Sans-serif", 8, weight=QFont.Bold))
        widget.line_edit.textChanged.connect(lambda: self.Kill_Confirmation_Function())

        if IntValidator:
            widget.line_edit.textChanged.connect(lambda: IntValidator_function())
            widget.line_edit.editingFinished.connect(lambda: EditingFinished_function())

        if StrValidator:
            widget.line_edit.editingFinished.connect(lambda: StrValidator_function())

        layout.addWidget(widget.line_edit)

    def connect_widget_signals(self, widget_list, settings, Save_Widget_Settings):
        for widget in widget_list:
            widget_name = widget.objectName()

            if hasattr(widget, "line_edit"):
                self.connect_line_edit(widget, widget_name, settings, Save_Widget_Settings)
            elif hasattr(widget, "checkmark"):
                self.connect_checkmark(widget, widget_name, settings, Save_Widget_Settings)
            elif (hasattr(widget, "combo_box1") or hasattr(widget, "combo_box2")) and not (
                    hasattr(widget, "button") or hasattr(widget, "button2")):
                self.connect_combo_box(widget, widget_name, settings, Save_Widget_Settings)
            elif (hasattr(widget, "combo_box1") or hasattr(widget, "combo_box2")) and (
                    hasattr(widget, "button") or hasattr(widget, "button2")):
                self.connect_combo_box(widget, widget_name, settings, Save_Widget_Settings, Has_Button=True)
            elif hasattr(widget, "button") and not hasattr(widget, "combo_box1"):
                self.connect_button(widget, widget_name, settings, Save_Widget_Settings)
            else:
                print(f"Can't connect Widget {widget_name}")

    def connect_line_edit(self, widget, widget_name, settings, Save_Widget_Settings):
        text = settings.get(widget_name, "")
        widget.line_edit.setText(text)
        widget.line_edit.textChanged.connect(lambda text: Save_Widget_Settings(widget))

    def connect_checkmark(self, widget, widget_name, settings, Save_Widget_Settings):
        state = settings.get(widget_name, [False, "", ""])
        widget.checkmark.setChecked(state[0])
        if hasattr(widget, "combo_box1"):
            widget.combo_box1.setCurrentText(state[1])
            widget.combo_box1.currentTextChanged.connect(lambda text: Save_Widget_Settings(widget))
            if hasattr(widget, "combo_box2"):
                widget.combo_box2.setCurrentText(state[2])
                widget.combo_box2.currentTextChanged.connect(lambda text: Save_Widget_Settings(widget))
        elif hasattr(widget, "combo_box2"):
            widget.combo_box2.setCurrentText(state[1])
            widget.combo_box2.currentTextChanged.connect(lambda text: Save_Widget_Settings(widget))
        widget.checkmark.stateChanged.connect(lambda state: Save_Widget_Settings(widget))

    def connect_combo_box(self, widget, widget_name, settings, Save_Widget_Settings, Has_Button=None):
        text = None
        if Has_Button:
            if hasattr(widget, "button2"):
                buttonState1, buttonState2, text = settings.get(widget_name, [False, False, ""])
                widget.button.setChecked(buttonState1)
                widget.button2.setChecked(buttonState2)
                widget.button.clicked.connect(lambda state: Save_Widget_Settings(widget))
                widget.button2.clicked.connect(lambda state: Save_Widget_Settings(widget))
            else:
                buttonState1, text = settings.get(widget_name, [False, ""])
                widget.button.setChecked(buttonState1)
                widget.button.clicked.connect(lambda state: Save_Widget_Settings(widget))
        else:
            text = settings.get(widget_name, "")

        if hasattr(widget, "combo_box1"):
            widget.combo_box1.setCurrentText(text)
            widget.combo_box1.currentTextChanged.connect(lambda text: Save_Widget_Settings(widget))
        if hasattr(widget, "combo_box2"):
            widget.combo_box2.setCurrentText(text)
            widget.combo_box2.currentTextChanged.connect(lambda text: Save_Widget_Settings(widget))

    def connect_button(self, widget, widget_name, settings, Save_Widget_Settings):
        if hasattr(widget, "button2"):
            state = settings.get(widget_name, [False, False])
            widget.button.setChecked(state[0])
            widget.button2.setChecked(state[1])
            widget.button.clicked.connect(lambda state: Save_Widget_Settings(widget))
            widget.button2.clicked.connect(lambda state: Save_Widget_Settings(widget))
        else:
            state = settings.get(widget_name, False)
            widget.button.setChecked(state)
            widget.button.clicked.connect(lambda state: Save_Widget_Settings(widget))

    # ------------------------------------------------------------------------------------------------ #

    def Open_Browser(self, Chrome=False, Firefox=False, Edge=False):
        # Access the Open_Browser Function
        Open_Browser = getattr(utilities_file, "Open_Browser", None)
        if not Open_Browser:
            raise ImportError("The function 'Open_Browser' was not found in Utilities_File.")

        if not self.DriverIsPresentlyOpen:
            self.driver, self.window_handles = Open_Browser(self, self.Plugins, self.function_combobox, Chrome, Firefox, Edge)
        else:
            print("Driver is still Open")

    def check_driver_status(self):
        while True:
            try:
                self.DriverIsPresentlyOpen = self.driver.find_elements(By.CSS_SELECTOR, "head")
            except:
                try:
                    time.sleep(3)
                    self.DriverIsPresentlyOpen = self.driver.find_elements(By.CSS_SELECTOR, "head")
                except:
                    print("Driver is no longer Open")
                    break

            time.sleep(1)
        self.driver.quit()
        self.driver, self.DriverIsPresentlyOpen = None, False
        print("Driver has been Closed")

    def PluginEvent(self):
        print("Plugin Event")

        self.Kill_Confirmation_Function()

        for widget in self.Script_Widgets:
            if widget not in ["BlankIndex1", "BlankIndex2"]:
                widget.hide()
                widget.deleteLater()

        for widget in self.Script_Configuration_Widgets_List:
            if widget not in ["BlankIndex"]:
                widget.hide()
                widget.deleteLater()

        self.Script_Configuration_section_widget.hide()
        self.Script_Configuration_section_widget.deleteLater()

        self.Script_Configuration_Widgets_List.clear()
        self.Script_Widgets.clear()

        self.kill_switch_active = False
        self.Confirm_Function_Variable = False
        self.Script_Widgets = []

        self.Plugin_Settings()
        self.Script_Configuration()
        self.Script_Specific_Settings()
        self.restart_keyboard_listener()
        self.Description_Changed()
        self.Execution_Output_section_widget.show()

        settings["function_combobox"] = self.function_combobox.currentText()
        save_settings_to_json()

    def update_sidebar_expanded(self, state):
        self.sidebar_expanded = state
        self.toggle_sidebar()

    def update_sidebar_expanded_plus(self):
        if self.sidebar_expanded:
            self.main_layout.setContentsMargins(230, 30, 30, 30)
            self.Execution_Output_section_widget.setFixedWidth(269)
            self.console_widget.hide()
        else:
            self.main_layout.setContentsMargins(80, 30, 30, 30)
            self.Execution_Output_section_widget.setFixedWidth(419)
            self.console_widget.show()

    # -------------------------------------------------------------------- #

    def start_keyboard_listener(self):
        print("Starting Listener")

        # Retrieve hotkey settings from the settings dictionary
        self.RunFunctionKey = settings.get("Run Function Key", "F2")
        self.KillSwitchKey = settings.get("Kill Switch Key", "Ctrl+Alt+Shift")

        keyboard.unhook_all()

        try:
            # Listen for the hotkey for the RunFunctionKey
            keyboard.add_hotkey(self.RunFunctionKey, self.run_selected_function)

            # Listen for the hotkey for the KillSwitchKey
            keyboard.add_hotkey(self.KillSwitchKey, self.activate_kill_switch)

            # Connect signals to stop keyboard listener thread
            # keyboard.wait()

        except ValueError as e:
            # Check and fix invalid hotkey string for RunFunctionKey
            if not self.is_valid_hotkey(self.RunFunctionKey):
                self.Keyboard_Listener_Widget1.line_edit.setText("F2")
                save_settings_to_json()

            # Check and fix invalid hotkey string for KillSwitchKey
            if not self.is_valid_hotkey(self.KillSwitchKey):
                self.Keyboard_Listener_Widget2.line_edit.setText("Ctrl+Alt+Shift")
                save_settings_to_json()

            self.restart_keyboard_listener()

    def is_valid_hotkey(self, hotkey):
        try:
            keyboard.parse_hotkey(hotkey)
            return True
        except ValueError:
            return False

    def restart_keyboard_listener(self):
        print("Re-Starting Listener")
        time.sleep(gtime)

        # Stop the current keyboard listener thread
        keyboard.unhook_all()

        # Start the keyboard listener in a new thread
        self.keyboard_listener_thread = threading.Thread(target=self.start_keyboard_listener)
        self.keyboard_listener_thread.start()

    def Temp_Test_Print(self, stop_event):
        try:
            check_stop_event(stop_event)
            print("Hello")
            time.sleep(.25)
            print("Log: BTS")
            time.sleep(.25)
            return True
        except StopFunctionException:
            return False

    def run_selected_function(self):
        if not self.Confirm_Function_Variable:
            print("Function not confirmed. Confirm first.")
            return

        keyboard.unhook_all()

        # Listen for the hotkey for the KillSwitchKey
        keyboard.add_hotkey(self.KillSwitchKey, self.activate_kill_switch)

        # Define the functions corresponding to each index
        function_mapping = {}

        # Function to find the next available index in the function mapping
        def get_next_index(mapping):
            if mapping:
                return max(mapping.keys()) + 1
            else:
                return 0

        index1 = 0

        # Access the Script_Launcher Function
        Script_Launcher = getattr(utilities_file, "Script_Launcher", None)
        if not Script_Launcher:
            raise ImportError("The function 'Script_Launcher' was not found in Utilities_File.")

        for _ in range(self.Length_Plugins):
            if self.Plugins[index1]:
                Script_Launcher(get_next_index, function_mapping, index1)
            index1 = index1 + 4

        # Get the selected function index
        selected_function_index, DriverIsNeeded = self.function_combobox.currentIndex(), self.Plugins[((4*self.function_combobox.currentIndex())+2)]

        # Get the corresponding function
        selected_function = function_mapping.get(selected_function_index)
        #selected_function = self.Temp_Test_Print

        # Execute the selected function in a new thread
        thread = threading.Thread(target=self.run_function_with_kill_switch, args=(selected_function, DriverIsNeeded))
        thread.start()

    def run_function_with_kill_switch(self, func, DriverIsNeeded):
        # Define a stop event
        stop_event = threading.Event()
        self.stop_event = stop_event

        # Start the kill switch thread
        self.kill_switch_active = False
        kill_switch_thread = threading.Thread(target=self.kill_switch, args=(stop_event,))
        kill_switch_thread.start()

        WorkingRow = settings.get("Starting Row", "2")
        WorkingRow = int(WorkingRow) - 1

        try:
            DriverDoesExist = self.driver
        except AttributeError:
            DriverDoesExist = None

        try:
            if DriverIsNeeded:
                if func is None:
                    print("Invalid function Selected, ", self.function_combobox.currentText())
                else:
                    if self.DriverIsPresentlyOpen:
                        # Run the selected function until the stop event is set
                        while not stop_event.is_set():
                            if not func(self.driver, self.window_handles, WorkingRow, settings=settings, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event):
                                break  # Exit the loop if the function returns False
                            WorkingRow = int(WorkingRow) + 1

                        WorkingRow = int(WorkingRow) + 1
                        self.driver.switch_to.window(self.window_handles[0])
                        settings["Starting Row"] = str(WorkingRow)
                        save_settings_to_json()
                        self.Starting_Row_Widget.line_edit.setText(str(WorkingRow))
                    else:
                        print("A Webdriver must be open to run this script")

            else:
                if func is None:
                    print("Invalid function Selected, ", self.function_combobox.currentText())
                else:
                        # Run the selected function until the stop event is set
                        while not stop_event.is_set():
                            if not func(stop_event=stop_event):
                                break  # Exit the loop if the function returns False
        except Exception as e:
            print(e)
    
        self.Kill_Confirmation_Function()
        selected_text = '"' + self.function_combobox.currentText() + '"'
        print("The Function", selected_text, "has completed the task or has been stopped by the kill switch")

    """
        if DriverDoesExist is not None:
            if func is None:
                print("Invalid function Selected, ", self.function_combobox.currentText())
            else:
                # Run the selected function until the stop event is set
                while not stop_event.is_set():
                    if not func(self.driver, self.window_handles, WorkingRow, settings=settings, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event):
                        break  # Exit the loop if the function returns False
                    WorkingRow = int(WorkingRow) + 1

                WorkingRow = int(WorkingRow) + 1
                self.driver.switch_to.window(self.window_handles[0])
                settings["Starting Row"] = str(WorkingRow)
                save_settings_to_json()
                self.Starting_Row_Widget.line_edit.setText(str(WorkingRow))
                DriverDoesExist = None

        else:
            if func is None:
                print("Invalid function Selected, ", self.function_combobox.currentText())
            else:
                try:
                    # Run the selected function until the stop event is set
                    while not stop_event.is_set():
                        if not func(stop_event=stop_event):
                            break  # Exit the loop if the function returns False
                except TypeError:
                    print("A Webdriver must be open to run this script")
                except Exception as e:
                    print(e)
    """

    def activate_kill_switch(self):
        print("Kill Switch Detected")
        self.Kill_Confirmation_Function()

    def kill_switch(self, stop_event):
        while not stop_event.is_set():
            if self.kill_switch_active:
                print("Kill Switch Activated")
                stop_event.set()
                self.Kill_Confirmation_Function()
                time.sleep(0.05)
                self.kill_switch_active = False  # Reset the kill switch flag
                break
            time.sleep(0.05)
        self.restart_keyboard_listener()

    def Kill_Confirmation_Function(self, index=None):
        self.Confirm_Function.setChecked(False)
        self.Confirm_Function_Variable = False
        self.kill_switch_active = True
        self.Confirm_Function_Green.hide()
        self.Confirm_Function_Red.show()

    # -------------------------------------------------------------------- #

class HelpGUI(BasePage):
    def __init__(self, parent=None):
        super().__init__()

        self.main_widget = QWidget(self)
        self.main_widget.lower()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(80, 30, 30, 30)
        self.main_layout.setSpacing(0)

        self.HelpGUI_Widget(page1, settings, Save_Widget_Settings)

        self.setCentralWidget(self.main_widget)

    def HelpGUI_Widget(self, page1, settings, Save_Widget_Settings):
        # Access the Help_GUI Function
        Help_GUI = getattr(utilities_file, "Help_GUI", None)
        if not Help_GUI:
            raise ImportError("The function 'Help_GUI' was not found in Utilities_File.")
        
        HelpGUI_Widget = Help_GUI(page1, settings, Save_Widget_Settings)
        self.main_layout.addWidget(HelpGUI_Widget)

    def update_sidebar_expanded(self, state):
        self.sidebar_expanded = state
        self.toggle_sidebar()

    def update_sidebar_expanded_plus(self):
        if self.sidebar_expanded:
            self.main_layout.setContentsMargins(230, 30, 30, 30)
        else:
            self.main_layout.setContentsMargins(80, 30, 30, 30)

class ExtraGUI(BasePage):
    def __init__(self, parent=None):
        super().__init__()

        self.main_widget = QWidget(self)
        self.main_widget.lower()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(80, 30, 30, 30)
        self.main_layout.setSpacing(0)

        self.ExtraGUI_Widget(page1, settings, Save_Widget_Settings)

        self.setCentralWidget(self.main_widget)

    def ExtraGUI_Widget(self, page1, settings, Save_Widget_Settings):
        # Access the Extra_GUI Function
        Extra_GUI = getattr(utilities_file, "Extra_GUI", None)
        if not Extra_GUI:
            raise ImportError("The function 'Extra_GUI' was not found in Utilities_File.")

        ExtraGUI_Widget = Extra_GUI(page1, settings, Save_Widget_Settings)
        self.main_layout.addWidget(ExtraGUI_Widget)

    def update_sidebar_expanded(self, state):
        self.sidebar_expanded = state
        self.toggle_sidebar()

    def update_sidebar_expanded_plus(self):
        if self.sidebar_expanded:
            self.main_layout.setContentsMargins(230, 30, 30, 30)
        else:
            self.main_layout.setContentsMargins(80, 30, 30, 30)

class QPushButton(QPushButton):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            return
        super().keyPressEvent(event)

class CustomPrint2:
    def __init__(self, parent=None):
        super().__init__()
        # Save the original sys.stdout
        self.original_stdout = sys.stdout

    def write(self, text):
        self.original_stdout.write(text)

"""class CustomPrint:
    def __init__(self, parent=None):
        super().__init__()
        # Save the original sys.stdout
        self.original_stdout = sys.stdout

    def print_and_copy(self, text):
        # Redirect stdout to the QTextEdit
        sys.stdout = page1.console_widget
        print(text)

        sys.stdout = self.original_stdout
        print(text)"""

class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

if __name__ == "__main__":

    app = QApplication(sys.argv)

    gtime = 0.25
    stylesheet = None

    bottom_left_image_path = Import_File("bottom_left_corner", resource_path(os.path.join("Resources", "Test", "Utilities", "Images.zip")))
    bottom_right_image_path = Import_File("bottom_right_corner", resource_path(os.path.join("Resources", "Test", "Utilities", "Images.zip")))
    Icon_Image = Import_File("App_Icon", resource_path(os.path.join("Resources", "Test", "Utilities", "Images.zip")))

    icons_WO_desc1 = Import_File("BurgerMenuIcon", resource_path(os.path.join("Resources", "Test", "Utilities", "Images.zip")))
    icons_WO_desc2 = Import_File("FunctionsIcon", resource_path(os.path.join("Resources", "Test", "Utilities", "Images.zip")))
    icons_WO_desc3 = Import_File("HelpIcon", resource_path(os.path.join("Resources", "Test", "Utilities", "Images.zip")))
    icons_WO_desc4 = Import_File("ExtraIcon", resource_path(os.path.join("Resources", "Test", "Utilities", "Images.zip")))

    icons_with_desc1 = Import_File("BurgerMenuIconWithDescription", resource_path(os.path.join("Resources", "Test", "Utilities", "Images.zip")))
    icons_with_desc2 = Import_File("FunctionsIconWithDescription", resource_path(os.path.join("Resources", "Test", "Utilities", "Images.zip")))
    icons_with_desc3 = Import_File("HelpIconWithDescription", resource_path(os.path.join("Resources", "Test", "Utilities", "Images.zip")))
    icons_with_desc4 = Import_File("ExtraIconWithDescription", resource_path(os.path.join("Resources", "Test", "Utilities", "Images.zip")))
    
    Red_Confirmation_Img = Import_File("ConfirmedRed", resource_path(os.path.join("Resources", "Test", "Utilities", "Images.zip")))
    Green_Confirmation_Img = Import_File("ConfirmedGreen", resource_path(os.path.join("Resources", "Test", "Utilities", "Images.zip")))

    # Load the utilities_file
    utilities_file = Import_File("Utilities_File", resource_path(os.path.join("Resources/Test/Utilities/Utilities_File.zip")))

    # Assigning StopFunctionException and check_stop_event
    StopFunctionException, check_stop_event = getattr(utilities_file, "StopFunctionException", None), getattr(utilities_file, "check_stop_event", None)

    # Window closing
    def close_application(event):
        print("Closing application")

        try:
            page1.Kill_Confirmation_Function()
        except Exception as e:
            print(f"Error stopping confirmation function: {e}")

        try:
            page1.stop_event.set()
        except:
            print("Stop event not found.")

        sys.stdout = sys.__stdout__

        if page1.DriverIsPresentlyOpen:
            try:
                page1.driver.quit()
            except Exception as e:
                print(f"Error while quitting the driver: {e}")

        keyboard.unhook_all()

        try:
            QApplication.quit()
        except Exception as e:
            print(f"Error while quitting the application: {e}")

        sys.exit()

    try:
        # Load the stylesheet from the encrypted zip
        stylesheet = Import_File("styles", resource_path(os.path.join("Resources/Test/Utilities/styles.zip")))
        if stylesheet:
            app.setStyleSheet(stylesheet)
    except FileNotFoundError:
        print("styles.qss file not found or could not be loaded.")
    except Exception as e:
        print(f"An error occurred: {e}")

    page_stack = QStackedWidget()
    CustomPrint3 = CustomPrint2()

    page1 = FunctionsGUI()
    page2 = HelpGUI()
    page3 = ExtraGUI()

    # PrintOut = CustomPrint()

    main_window = BasePage()
    BasePage.page_stack = page_stack

    page_stack.addWidget(page1)
    page_stack.addWidget(page2)
    page_stack.addWidget(page3)

    open_page = settings.get("Page_Stack_Index", 0)

    main_window.setCentralWidget(page_stack)
    page_stack.setCurrentIndex(open_page)
    main_window.show()
    main_window.closeEvent = close_application

    pages = [page1, page2, page3]

    for i, page in enumerate(pages):
        for j, other_page in enumerate(pages):
            if i != j:
                page.sidebar_expanded_changed.connect(other_page.update_sidebar_expanded)

    for page in pages:
        page.sidebar_expanded_changed.connect(page1.update_sidebar_expanded_plus)
        page.sidebar_expanded_changed.connect(page2.update_sidebar_expanded_plus)
        page.sidebar_expanded_changed.connect(page3.update_sidebar_expanded_plus)
        page.page_changed.connect(page1.Kill_Confirmation_Function)
        page.page_changed.connect(lambda: page1.Kill_Confirmation_Function())

    sys.exit(app.exec())
