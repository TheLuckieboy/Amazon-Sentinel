import time, pyautogui, pyperclip, threading, keyboard, json, string, logging, datetime, os, sys
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QGridLayout, QStackedWidget, QWidget, QTextEdit, QComboBox, QHBoxLayout, QLineEdit, QCheckBox, QSpacerItem, QSizePolicy, QMessageBox, QCompleter, QFrame, QVBoxLayout
from PyQt5.QtGui import QPixmap, QIcon, QFont, QRegExpValidator, QIntValidator, QColor, QPainter, QPen, QPainterPath
from PyQt5.QtCore import QSize, QRect, Qt, pyqtSignal, QRegExp, QPoint
from PyQt5 import QtCore, QtGui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

gtime = 0.25
SearchBarResultCount = 0
BadgeValuesNonLoadCount = 0
AccessValuesNonLoadCount = 0

# ------------------------------------------------------------------------------------------------------------------------------------------ #

def Cardholder_Verification(driver, window_handles, WorkingRow, settings=None, StopFunctionException=None, check_stop_event=None, stop_event=None):
    print("Test")
    return False

def Main_Widgets(FunctionsGUI, grid_layout):
    List_of_Widget = []
    rows = [
        {
            "label_text": "SearchBy Column:",
            "font_size": 7,
            "button_widget": True,
            "button_widget2": True,
            "button_label": "SearchBy EID",
            "button_label2": "SearchBy Login",
            "add_qlabel_right": True,
            "column_letter_box": True,
            "grid_params": (1, 0, 1, 3),
            "object_name": "SearchBy_Column_Widget"
        }, # SearchBy_Column_Widget
        {
            "label_text": "Check Employee's\nHome Site:",
            "font_size": 7,
            "site_location": True,
            "grid_params": (1, 3, 1, 2),
            "object_name": "Home_Site_Widget"
        }, # Home_Site_Widget

        {
            "gap_row": True,
            "grid_params": (2, 0, 1, 3)
        },  # Gap Row

        {
            "label_text": "Cardholder Tab Information",
            "font_size": 12,
            "title_label": True,
            "button_label": "Inactive",
            "button_width": 80,
            "grid_params": (3, 0, 1, 3),
            "object_name": "Cardholder_Tab_Info_Widget"
        }, # Cardholder_Tab_Info_Widget
        {
            "label_text": "EID:",
            "checkmark": True,
            "column_letter_box": True,
            "grid_params": (3, 3, 1, 1),
            "object_name": "EID_Widget"
        }, # EID_Widget
        {
            "label_text": "Login:",
            "checkmark": True,
            "column_letter_box": True,
            "grid_params": (3, 4, 1, 1),
            "object_name": "Login_Widget"
        }, # Login_Widget

        {
            "label_text": "First\nName:",
            "checkmark": True,
            "column_letter_box": True,
            "grid_params": (4, 0, 1, 1),
            "object_name": "FirstName_Widget"
        },  # FirstName_Widget
        {
            "label_text": "Last\nName:",
            "checkmark": True,
            "column_letter_box": True,
            "grid_params": (4, 1, 1, 1),
            "object_name": "LastName_Widget"
        },  # LastName_Widget
        {
            "label_text": "Employee\nType:",
            "checkmark": True,
            "column_letter_box": True,
            "grid_params": (4, 2, 1, 1),
            "object_name": "EmployeeType_Widget"
        },  # EmployeeType_Widget
        {
            "label_text": "Employee\nStatus:",
            "checkmark": True,
            "column_letter_box": True,
            "grid_params": (4, 3, 1, 1),
            "object_name": "EmployeeStatus_Widget"
        },  # EmployeeStatus_Widget
        {
            "label_text": "Manager\nLogin:",
            "checkmark": True,
            "column_letter_box": True,
            "grid_params": (4, 4, 1, 1),
            "object_name": "ManagerLogin_Widget"
        },  # ManagerLogin_Widget

        {
            "label_text": "Person\nID:",
            "checkmark": True,
            "column_letter_box": True,
            "grid_params": (5, 0, 1, 1),
            "object_name": "PersonID_Widget"
        },  # PersonID_Widget
        {
            "label_text": "Barcode:",
            "checkmark": True,
            "column_letter_box": True,
            "grid_params": (5, 1, 1, 1),
            "object_name": "Barcode_Widget"
        },  # Barcode_Widget
        {
            "label_text": "Tenure:",
            "checkmark": True,
            "column_letter_box": True,
            "grid_params": (5, 2, 1, 1),
            "object_name": "Tenure_Widget"
        },  # Tenure_Widget
        {
            "label_text": "Region:",
            "checkmark": True,
            "column_letter_box": True,
            "grid_params": (5, 3, 1, 1),
            "object_name": "Region_Widget"
        },  # Region_Widget
        {
            "label_text": "Building:",
            "checkmark": True,
            "column_letter_box": True,
            "grid_params": (5, 4, 1, 1),
            "object_name": "Building_Widget"
        },  # Building_Widget

        {
            "gap_row": True,
            "grid_params": (6, 0, 1, 3)
        },  # Gap Row

        {
            "label_text": "Badge Tab Information:",
            "font_size": 12,
            "title_label": True,
            "button_label": "Inactive",
            "button_width": 80,
            "grid_params": (7, 0, 1, 3),
            "object_name": "Badge_Tab_Info_Widget"
        },  # Badge_Tab_Info_Widget
        {
            "label_text": "Badge\nStatus:",
            "checkmark": True,
            "column_letter_box": True,
            "grid_params": (7, 3, 1, 1),
            "object_name": "BadgeStatus_Widget"
        },  # BadgeStatus_Widget
        {
            "label_text": "Badge\nType:",
            "checkmark": True,
            "column_letter_box": True,
            "grid_params": (7, 4, 1, 1),
            "object_name": "BadgeType_Widget"
        },  # BadgeType_Widget

        {
            "label_text": "Badge\nCount:",
            "checkmark": True,
            "column_letter_box": True,
            "grid_params": (8, 0, 1, 1),
            "object_name": "BadgeCount_Widget"
        },  # BadgeCount_Widget
        {
            "label_text": "Badge\nID:",
            "checkmark": True,
            "column_letter_box": True,
            "grid_params": (8, 1, 1, 1),
            "object_name": "BadgeID_Widget"
        },  # BadgeID_Widget
        {
            "label_text": "Activate\nOn:",
            "checkmark": True,
            "column_letter_box": True,
            "grid_params": (8, 2, 1, 1),
            "object_name": "ActiveOn_Widget_Badge"
        },  # ActiveOn_Widget
        {
            "label_text": "Deactive\nOn:",
            "checkmark": True,
            "column_letter_box": True,
            "grid_params": (8, 3, 1, 1),
            "object_name": "DeactiveOn_Widget_Badge"
        },  # DeactiveOn_Widget
        {
            "label_text": "Last\nUpdate:",
            "checkmark": True,
            "column_letter_box": True,
            "grid_params": (8, 4, 1, 1),
            "object_name": "LastUpdate_Widget"
        },  # LastUpdate_Widget

        {
            "label_text": "Last\nRead:",
            "checkmark": True,
            "column_letter_box": True,
            "grid_params": (9, 0, 1, 1),
            "object_name": "LastRead_Widget"
        },  # LastRead_Widget
        {
            "label_text": "Last Time\nstamp:",
            "checkmark": True,
            "column_letter_box": True,
            "grid_params": (9, 1, 1, 1),
            "object_name": "LastTimestamp_Widget"
        },  # LastTimestamp_Widget
        {
            "label_text": "Event\nType:",
            "checkmark": True,
            "column_letter_box": True,
            "grid_params": (9, 2, 1, 1),
            "object_name": "EventType_Widget"
        },  # LastType_Widget
        {
            "label_text": "Active Badge Present?:",
            "font_size": 7,
            "checkmark": True,
            "column_letter_box": True,
            "grid_params": (9, 3, 1, 2),
            "object_name": "ActiveBadgePresent_Widget"
        },  # ActiveBadgePresent_Widget

        {
            "gap_row": True,
            "grid_params": (10, 0, 1, 3)
        },  # Gap Row

        {
            "label_text": "Access Lvl Tab Information:",
            "font_size": 12,
            "title_label": True,
            "button_label": "Inactive",
            "button_width": 80,
            "grid_params": (11, 0, 1, 3),
            "object_name": "AccessLvl_Tab_Info_Widget"
        },  # AccessLvl_Tab_Info_Widget
        {
            "label_text": "Has General Access to Site?:",
            "font_size": 7,
            "checkmark": True,
            "column_letter_box": True,
            "grid_params": (11, 3, 1, 2),
            "object_name": "GeneralAccess_Widget"
        },  # GeneralAccess_Widget
        {
            "label_text": "AccessLvl\nCount:",
            "checkmark": True,
            "column_letter_box": True,
            "grid_params": (12, 1, 1, 1),
            "object_name": "AccessLvlCount_Widget"
        },  # AccessLvlCount_Widget
        {
            "label_text": "Activate\nOn:",
            "checkmark": True,
            "column_letter_box": True,
            "grid_params": (12, 2, 1, 1),
            "object_name": "ActivateOn_Widget_AccessLvl"
        },  # AccessLvlType_Widget
        {
            "label_text": "Deactive\nOn:",
            "checkmark": True,
            "column_letter_box": True,
            "grid_params": (12, 3, 1, 1),
            "object_name": "DeactiveOn_Widget_AccessLvl"
        }, # DeactiveOn_Widget
    ]

    for row_info in rows:
        if "gap_row" in row_info and row_info["gap_row"]:
            # Insert gap row
            spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
            grid_layout.addItem(spacer, *row_info["grid_params"])
        else:
            widget = FunctionsGUI.Widget_Creator(
                label_text=row_info["label_text"],
                label_text2=row_info["label_text"],
                ButtonLabel=row_info.get("button_label", "Add_Label"),
                ButtonLabel2=row_info.get("button_label2", "Add_Label"),

                Title_Label=row_info.get("title_label", False),
                Checkmark=row_info.get("checkmark", False),
                Column_Letter_Box=row_info.get("column_letter_box", False),
                Quip_Color_Box=row_info.get("quip_color_box", False),
                SiteLocation=row_info.get("site_location", False),
                EditBox=row_info.get("edit_box", False),

                Add_QLabel_Left=row_info.get("add_qlabel_left", False),
                Add_QLabel_Right=row_info.get("add_qlabel_right", False),

                ButtonWidget=row_info.get("button_widget", False),
                ButtonWidget2=row_info.get("button_widget2", False),

                IntValidator=row_info.get("int_validator", False),
                StrValidator=row_info.get("str_validator", False),
                Font_Size = row_info.get("font_size", 6),
                Line_Edit = row_info.get("line_edit", 150),
                Button_Width = row_info.get("button_width", None),
                Button_Width2 = row_info.get("button_width2", None)
            )
            widget.setObjectName(row_info["object_name"])
            grid_layout.addWidget(widget, *row_info["grid_params"])

            List_of_Widget.append(widget)
    return List_of_Widget

def Interpreter_ColorCode_Widgets(FunctionsGUI, layout):
    List_of_Widget = []
    rows = [
        {
            "label_text": "Color Code Settings:",
            "font_size": 12,
            "title_label": True,
            "button_label": "Inactive",
            "button_width": 80,
            "object_name": "ColorCodeSettings_Widget"
        },  # Cardholder_Tab_Info_Widget
        {
            "label_text": "Active AA, Active Badge\n@ Site:",
            "font_size": 7,
            "checkmark": True,
            "quip_color_box": True,
            "object_name": "Active AA, Active Badge @ Site_Widget"
        }, # Active AA, Active Badge @ Site_Widget
        {
            "label_text": "Active AA, Active Badge\n@ Other Site:",
            "font_size": 7,
            "checkmark": True,
            "quip_color_box": True,
            "object_name": "Active AA, Active Badge @ Other Site_Widget"
        },  # Active AA, Active Badge @ Other Site_Widget
        {
            "label_text": "Active AA, Inactive Badge\n@ Site:",
            "font_size": 7,
            "checkmark": True,
            "quip_color_box": True,
            "object_name": "Active AA, Inactive Badge @ Site_Widget"
        },  # Active AA, Inactive Badge @ Site_Widget
        {
            "label_text": "Active AA, Inactive Badge\n@ Other Site:",
            "font_size": 7,
            "checkmark": True,
            "quip_color_box": True,
            "object_name": "Active AA, Inactive Badge @ Other Site_Widget"
        },  # Active AA, Inactive Badge @ Other Site_Widget
        {
            "label_text": "Terminated AA @ Site:",
            "font_size": 7,
            "checkmark": True,
            "quip_color_box": True,
            "object_name": "Terminated AA @ Site_Widget"
        },  # Terminated AA @ Site_Widget
        {
            "label_text": "Terminated AA @ Other Site:",
            "font_size": 7,
            "checkmark": True,
            "quip_color_box": True,
            "object_name": "Terminated AA @ Other Site_Widget"
        },  # erminated AA @ Other Site_Widget
        {
            "label_text": "*Fail Safe Measure*\nBad EID/Login:",
            "font_size": 7,
            "checkmark": True,
            "quip_color_box": True,
            "object_name": "*Fail Safe Measure* Bad EID/Login_Widget"
        },  # *Fail Safe Measure* Bad EID/Login_Widget
        {
            "label_text": "*Color a Column*\nRow Complete:",
            "font_size": 7,
            "checkmark": True,
            "column_letter_box": True,
            "quip_color_box": True,
            "object_name": "*Color a Column* Row Complete_Widget"
        },  # *Color a Column* Row Complete_Widget
    ]

    for row_info in rows:
        if "gap_row" in row_info and row_info["gap_row"]:
            # Insert gap row
            spacer = QSpacerItem(20, 200, QSizePolicy.Minimum, QSizePolicy.Expanding)
            layout.addItem(spacer)
        else:
            widget = FunctionsGUI.Widget_Creator(
                label_text=row_info["label_text"],
                label_text2=row_info["label_text"],
                ButtonLabel=row_info.get("button_label", "Add_Label"),
                ButtonLabel2=row_info.get("button_label2", "Add_Label"),

                Title_Label=row_info.get("title_label", False),
                Checkmark=row_info.get("checkmark", False),
                Column_Letter_Box=row_info.get("column_letter_box", False),
                Quip_Color_Box=row_info.get("quip_color_box", False),
                SiteLocation=row_info.get("site_location", False),
                EditBox=row_info.get("edit_box", False),

                Add_QLabel_Left=row_info.get("add_qlabel_left", False),
                Add_QLabel_Right=row_info.get("add_qlabel_right", False),

                ButtonWidget=row_info.get("button_widget", False),
                ButtonWidget2=row_info.get("button_widget2", False),

                IntValidator=row_info.get("int_validator", False),
                StrValidator=row_info.get("str_validator", False),
                Font_Size = row_info.get("font_size", 6),
                Line_Edit = row_info.get("line_edit", 150),
                Button_Width = row_info.get("button_width", None),
                Button_Width2 = row_info.get("button_width2", None)
            )
            widget.setObjectName(row_info["object_name"])
            widget.setMaximumWidth(400)
            layout.addWidget(widget)

            List_of_Widget.append(widget)
    return List_of_Widget

def Interpreter_NamePrint_Widgets(FunctionsGUI, layout):
    List_of_Widget = []
    rows = [
        {
            "label_text": "Last name, First name",
            "checkmark": True,
            "font_size": 8,
            "object_name": "LastNameComma_FirstName_CardholderVerification"
        },  # Replace
        {
            "label_text": "First name, Last name",
            "checkmark": True,
            "font_size": 8,
            "object_name": "FirstNameComma_LastName_CardholderVerification"
        },  # Replace
        {
            "label_text": "First name Last name",
            "checkmark": True,
            "font_size": 8,
            "object_name": "FirstName_LastName_CardholderVerification"
        },  # Replace
        {
            "gap_row": True,
        },  # Gap Row
    ]

    for row_info in rows:
        if "gap_row" in row_info and row_info["gap_row"]:
            # Insert gap row
            spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
            layout.addItem(spacer)
        else:
            widget = FunctionsGUI.Widget_Creator(
                label_text=row_info["label_text"],
                label_text2=row_info["label_text"],
                ButtonLabel=row_info.get("button_label", "Add_Label"),
                ButtonLabel2=row_info.get("button_label2", "Add_Label"),

                Title_Label=row_info.get("title_label", False),
                Checkmark=row_info.get("checkmark", False),
                Column_Letter_Box=row_info.get("column_letter_box", False),
                Quip_Color_Box=row_info.get("quip_color_box", False),
                SiteLocation=row_info.get("site_location", False),
                EditBox=row_info.get("edit_box", False),

                Add_QLabel_Left=row_info.get("add_qlabel_left", False),
                Add_QLabel_Right=row_info.get("add_qlabel_right", False),

                ButtonWidget=row_info.get("button_widget", False),
                ButtonWidget2=row_info.get("button_widget2", False),

                IntValidator=row_info.get("int_validator", False),
                StrValidator=row_info.get("str_validator", False),
                Font_Size = row_info.get("font_size", 6),
                Line_Edit = row_info.get("line_edit", 150),
                Button_Width = row_info.get("button_width", None),
                Button_Width2 = row_info.get("button_width2", None)
            )
            widget.setObjectName(row_info["object_name"])
            layout.addWidget(widget)

            List_of_Widget.append(widget)
    return List_of_Widget

def Widget_Setup(FunctionsGUI, Main_Widget, settings, Save_Widget_Settings, Main_GridLayout, Script_Widgets):
    grid_layout = QGridLayout(Main_Widget)
    grid_layout.setContentsMargins(8, 0, 8, 8)
    grid_layout.setSpacing(8)

    Widgets_List = Main_Widgets(FunctionsGUI, grid_layout)
    cardholder_widget_list = ["EID_Widget", "Login_Widget", "FirstName_Widget", "LastName_Widget",
                              "EmployeeType_Widget", "EmployeeStatus_Widget", "ManagerLogin_Widget",
                              "PersonID_Widget", "Barcode_Widget", "Tenure_Widget", "Region_Widget",
                              "Building_Widget"]
    Badge_Tab_widget_list = ["BadgeStatus_Widget", "BadgeType_Widget", "BadgeCount_Widget", "BadgeID_Widget",
                             "ActiveOn_Widget_Badge", "DeactiveOn_Widget_Badge", "LastUpdate_Widget", "LastRead_Widget",
                             "LastTimestamp_Widget", "LastType_Widget", "ActiveBadgePresent_Widget"]
    AccessLvl_Tab_widget_list = ["GeneralAccess_Widget", "AccessLvlCount_Widget",
                                 "ActivateOn_Widget_AccessLvl", "DeactiveOn_Widget_AccessLvl"]

    def Interpreter_Settings():
        Interpreter_Settings_Widget = QWidget()
        QVLayout = QVBoxLayout(Interpreter_Settings_Widget)
        QVLayout.setContentsMargins(8, 8, 8, 8)
        QVLayout.setSpacing(8)

        def Open_Settings():
            QHLayout1 = QHBoxLayout()
            QHLayout1.setContentsMargins(0, 0, 0, 0)
            QHLayout1.setSpacing(8)

            QHLayout2 = QHBoxLayout()
            QHLayout2.setContentsMargins(0, 0, 0, 0)
            QHLayout2.setSpacing(8)

            def Color_Code_Widgets():
                Color_Code_Widget = QWidget()
                section_layout = QVBoxLayout(Color_Code_Widget)
                section_layout.setContentsMargins(0, 0, 0, 0)
                section_layout.setSpacing(8)

                Color_Code_Widgets = Interpreter_ColorCode_Widgets(FunctionsGUI, section_layout)

                def toggle_widgets(main_widget_name, widget_list, Connect=True, StartingState=False):
                    main_widget = None
                    for widget in Color_Code_Widgets:
                        if widget.objectName() == main_widget_name:
                            main_widget = widget
                            break

                    if main_widget:
                        if Connect:
                            if not main_widget.button.isChecked():
                                main_widget.button.setText("Inactive")
                                for widget in Color_Code_Widgets:
                                    if hasattr(widget, "checkmark"):
                                        widget.checkmark.setDisabled(True)
                                    if hasattr(widget, "combo_box1"):
                                        widget.combo_box1.setDisabled(True)
                                    if hasattr(widget, "combo_box2"):
                                        widget.combo_box2.setDisabled(True)
                            else:
                                main_widget.button.setText("Active")
                                for widget in Color_Code_Widgets:
                                    if hasattr(widget, "checkmark"):
                                        widget.checkmark.setEnabled(True)
                                        if widget.checkmark.isChecked():
                                            if hasattr(widget, "combo_box1"):
                                                widget.combo_box1.setEnabled(True)
                                            if hasattr(widget, "combo_box2"):
                                                widget.combo_box2.setEnabled(True)
                        else:
                            if StartingState:
                                for widget in Color_Code_Widgets:
                                    if hasattr(widget, "checkmark"):
                                        widget.checkmark.setEnabled(True)
                                        if widget.checkmark.isChecked():
                                            if hasattr(widget, "combo_box1"):
                                                widget.combo_box1.setEnabled(True)
                                            if hasattr(widget, "combo_box2"):
                                                widget.combo_box2.setEnabled(True)
                            else:
                                for widget in Color_Code_Widgets:
                                    if hasattr(widget, "checkmark"):
                                        widget.checkmark.setDisabled(True)
                                    if hasattr(widget, "combo_box1"):
                                        widget.combo_box1.setDisabled(True)
                                    if hasattr(widget, "combo_box2"):
                                        widget.combo_box2.setDisabled(True)

                FunctionsGUI.connect_widget_signals(Color_Code_Widgets, settings, Save_Widget_Settings)
                for widget in Color_Code_Widgets:
                    if widget.objectName() == "ColorCodeSettings_Widget":
                        if settings.get("ColorCodeSettings_Widget", False):
                            widget.button.setText("Active")
                            widget.button.setChecked(True)
                            toggle_widgets("ColorCodeSettings_Widget", Color_Code_Widgets, False, True)
                        else:
                            widget.button.setText("Inactive")
                            widget.button.setChecked(False)
                            toggle_widgets("ColorCodeSettings_Widget", Color_Code_Widgets, False, False)
                        widget.button.clicked.connect(
                            lambda: toggle_widgets("ColorCodeSettings_Widget", Color_Code_Widgets, True))

                QHLayout1.addWidget(Color_Code_Widget)
            Color_Code_Widgets()

            def NamePrint_Widgets():
                NamePrint_Widget = QWidget()
                section_layout = QVBoxLayout(NamePrint_Widget)
                section_layout.setContentsMargins(24, 0, 0, 0)
                section_layout.setSpacing(8)

                LabelText = FunctionsGUI.Widget_Creator("One Column, Both Names:", Font_Size=12)
                section_layout.addWidget(LabelText)

                def toggle_checkmarks(widget):
                    sender = widget
                    if sender == LastNameComma_FirstName_CardholderVerification:
                        LastNameComma_FirstName_CardholderVerification.checkmark.setChecked(True)
                        FirstNameComma_LastName_CardholderVerification.checkmark.setChecked(False)
                        FirstName_LastName_CardholderVerification.checkmark.setChecked(False)
                    elif sender == FirstNameComma_LastName_CardholderVerification:
                        LastNameComma_FirstName_CardholderVerification.checkmark.setChecked(False)
                        FirstNameComma_LastName_CardholderVerification.checkmark.setChecked(True)
                        FirstName_LastName_CardholderVerification.checkmark.setChecked(False)
                    elif sender == FirstName_LastName_CardholderVerification:
                        LastNameComma_FirstName_CardholderVerification.checkmark.setChecked(False)
                        FirstNameComma_LastName_CardholderVerification.checkmark.setChecked(False)
                        FirstName_LastName_CardholderVerification.checkmark.setChecked(True)
                    Save_Widget_Settings(NamePrint_Widgets)

                NamePrint_Widgets = Interpreter_NamePrint_Widgets(FunctionsGUI, section_layout)

                for widget in NamePrint_Widgets:
                    if widget.objectName() == "LastNameComma_FirstName_CardholderVerification":
                        LastNameComma_FirstName_CardholderVerification = widget
                        LastNameComma_FirstName_CardholderVerification.checkmark.setChecked(settings.get("LastNameComma_FirstName_CardholderVerification", False))
                        LastNameComma_FirstName_CardholderVerification.checkmark.clicked.connect(lambda state, w=widget: toggle_checkmarks(w))
                    if widget.objectName() == "FirstNameComma_LastName_CardholderVerification":
                        FirstNameComma_LastName_CardholderVerification = widget
                        FirstNameComma_LastName_CardholderVerification.checkmark.setChecked(settings.get("FirstNameComma_LastName_CardholderVerification", False))
                        FirstNameComma_LastName_CardholderVerification.checkmark.clicked.connect(lambda state, w=widget: toggle_checkmarks(w))
                    if widget.objectName() == "FirstName_LastName_CardholderVerification":
                        FirstName_LastName_CardholderVerification = widget
                        FirstName_LastName_CardholderVerification.checkmark.setChecked(settings.get("FirstName_LastName_CardholderVerification", False))
                        FirstName_LastName_CardholderVerification.checkmark.clicked.connect(lambda state, w=widget: toggle_checkmarks(w))

                QHLayout1.addWidget(NamePrint_Widget)
            NamePrint_Widgets()

            def Close_Interpreter_Settings():
                Interpreter_Settings_Button = FunctionsGUI.Widget_Creator(ButtonLabel='Close Interpreter Settings',
                                                                  ButtonWidget=True, Button_Width=284)
                Interpreter_Settings_Button.button.clicked.connect(lambda: FunctionsGUI.Hide_Main_Widgets(False))
                Interpreter_Settings_Button.button.clicked.connect(lambda: Interpreter_Settings_Widget.hide())
                Interpreter_Settings_Button.button.clicked.connect(lambda: FunctionsGUI.Kill_Confirmation_Function())
                Interpreter_Settings_Button.setObjectName("Close_Interpreter_Settings")
                Interpreter_Settings_Button.button.setFixedHeight(35)
                QHLayout2.addWidget(Interpreter_Settings_Button)
            Close_Interpreter_Settings()

            QHLayout1.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
            QHLayout2.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

            QVLayout.addLayout(QHLayout1)
            QVLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
            QVLayout.addLayout(QHLayout2)

            Script_Widgets.append(Interpreter_Settings_Widget)
            Main_GridLayout.addWidget(Interpreter_Settings_Widget)
            Interpreter_Settings_Widget.hide()
        Open_Settings()

        def Closed_Settings():
            spacer = QSpacerItem(0, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            grid_layout.addItem(spacer, 13, 0, 1, 5)

            Interpreter_Settings_Button = FunctionsGUI.Widget_Creator(ButtonLabel='Interpreter Settings',
                                                                      ButtonWidget=True)
            Interpreter_Settings_Button.button.clicked.connect(lambda: FunctionsGUI.Hide_Main_Widgets(True))
            Interpreter_Settings_Button.button.clicked.connect(lambda: Interpreter_Settings_Widget.show())
            Interpreter_Settings_Button.button.clicked.connect(lambda: Interpreter_Settings_Widget.raise_())
            Interpreter_Settings_Button.setObjectName("Interpreter_Settings")
            Interpreter_Settings_Button.button.setFixedHeight(35)
            grid_layout.addWidget(Interpreter_Settings_Button, 14, 0, 1, 2)
        Closed_Settings()
    Interpreter_Settings()

    FunctionsGUI.connect_widget_signals(Widgets_List, settings, Save_Widget_Settings)

    def toggle_widgets(main_widget_name, widget_list, Connect=True, StartingState=False):
        main_widget = None
        for widget in Widgets_List:
            if widget.objectName() == main_widget_name:
                main_widget = widget
                break

        if main_widget:
            if Connect:
                if not main_widget.button.isChecked():
                    main_widget.button.setText("Inactive")
                    for widget in Widgets_List:
                        widget_name = widget.objectName()
                        if widget_name in widget_list:
                            if hasattr(widget, "combo_box1"):
                                widget.combo_box1.setDisabled(True)
                            if hasattr(widget, "checkmark"):
                                widget.checkmark.setDisabled(True)
                else:
                    main_widget.button.setText("Active")
                    for widget in Widgets_List:
                        widget_name = widget.objectName()
                        if widget_name in widget_list:
                            if hasattr(widget, "checkmark"):
                                widget.checkmark.setEnabled(True)
                                if widget.checkmark.isChecked():
                                    if hasattr(widget, "combo_box1"):
                                        widget.combo_box1.setEnabled(True)

            else:
                if StartingState:
                    for widget in Widgets_List:
                        widget_name = widget.objectName()
                        if widget_name in widget_list:
                            if hasattr(widget, "checkmark"):
                                widget.checkmark.setEnabled(True)
                                if widget.checkmark.isChecked():
                                    if hasattr(widget, "combo_box1"):
                                        widget.combo_box1.setEnabled(True)
                else:
                    for widget in Widgets_List:
                        widget_name = widget.objectName()
                        if widget_name in widget_list:
                            if hasattr(widget, "combo_box1"):
                                widget.combo_box1.setDisabled(True)
                            if hasattr(widget, "checkmark"):
                                widget.checkmark.setDisabled(True)
    for widget in Widgets_List:
        if widget.objectName() == "SearchBy_Column_Widget":
            def toggle_buttons(checked, widget=widget):
                sender = widget.sender()
                if sender == widget.button:
                    widget.button.setChecked(True)
                    widget.button2.setChecked(False)
                elif sender == widget.button2:
                    widget.button.setChecked(False)
                    widget.button2.setChecked(True)
                Save_Widget_Settings(widget)

            widget.button.clicked.connect(toggle_buttons)
            widget.button2.clicked.connect(toggle_buttons)

        if widget.objectName() == "Cardholder_Tab_Info_Widget":
            if settings.get("Cardholder_Tab_Info_Widget", False):
                widget.button.setText("Active")
                widget.button.setChecked(True)
                toggle_widgets("Cardholder_Tab_Info_Widget", cardholder_widget_list, False, True)
            else:
                widget.button.setText("Inactive")
                widget.button.setChecked(False)
                toggle_widgets("Cardholder_Tab_Info_Widget", cardholder_widget_list, False, False)
            widget.button.clicked.connect(
                lambda: toggle_widgets("Cardholder_Tab_Info_Widget", cardholder_widget_list, True))

        if widget.objectName() == "Badge_Tab_Info_Widget":
            if settings.get("Badge_Tab_Info_Widget", False):
                widget.button.setText("Active")
                widget.button.setChecked(True)
                toggle_widgets("Badge_Tab_Info_Widget", Badge_Tab_widget_list, False, True)
            else:
                widget.button.setText("Inactive")
                widget.button.setChecked(False)
                toggle_widgets("Badge_Tab_Info_Widget", Badge_Tab_widget_list, False, False)
            widget.button.clicked.connect(
                lambda: toggle_widgets("Badge_Tab_Info_Widget", Badge_Tab_widget_list, True))

        if widget.objectName() == "AccessLvl_Tab_Info_Widget":
            if settings.get("AccessLvl_Tab_Info_Widget", False):
                widget.button.setText("Active")
                widget.button.setChecked(True)
                toggle_widgets("AccessLvl_Tab_Info_Widget", AccessLvl_Tab_widget_list, False, True)
            else:
                widget.button.setText("Inactive")
                widget.button.setChecked(False)
                toggle_widgets("AccessLvl_Tab_Info_Widget", AccessLvl_Tab_widget_list, False, False)
            widget.button.clicked.connect(
                lambda: toggle_widgets("AccessLvl_Tab_Info_Widget", AccessLvl_Tab_widget_list, True))

# ------------------------------------------------------------------------------------------------------------------------------------------ #

# Setup code to get the IDs
EID_ID = None
First_Name_ID = None
Last_Name_ID = None
Login_ID = None
SearchButton_Element = None

class CardHolder_General_Failsafe(Exception):
    pass

def Cardholder_Failsafe_GeneralError(driver):
    for attempt in range(3):
        try:
            Element_List = driver.find_elements(By.CSS_SELECTOR, "[class*='awsui_large']")

            for Element in Element_List:
                class_name = Element.get_attribute('class')
                if 'awsui_breakpoint' in class_name:
                        time.sleep(gtime)
                        raise CardHolder_General_Failsafe
        except (StaleElementReferenceException, NoSuchElementException) as E:
            print(f"Cardholder_Failsafe_GeneralError: {E}")

def CardHolder_GetID_First_Last_Name(driver, StopFunctionException=None, check_stop_event=None, stop_event=None):
    global First_Name_ID, Last_Name_ID
    try:
        check_stop_event(stop_event)
        Cardholder_Failsafe_GeneralError(driver)
        if First_Name_ID is None and Last_Name_ID is None:
            # Find all input elements with the specified class name
            input_elements = driver.find_elements(By.CSS_SELECTOR, 'input[class*="awsui_input_"]')
            check_stop_event(stop_event)
            Cardholder_Failsafe_GeneralError(driver)

            First_Name_ID = input_elements[4].get_attribute("id")
            Last_Name_ID = input_elements[5].get_attribute("id")

        check_stop_event(stop_event)
        Cardholder_Failsafe_GeneralError(driver)
        return First_Name_ID, Last_Name_ID
    except (StopFunctionException, ElementClickInterceptedException, StaleElementReferenceException, CardHolder_General_Failsafe):
        return False

def CardHolder_GetID_EID(driver, StopFunctionException=None, check_stop_event=None, stop_event=None):
    global EID_ID
    try:
        check_stop_event(stop_event)
        Cardholder_Failsafe_GeneralError(driver)
        if EID_ID is None:
            # Find all input elements with the specified class name
            input_elements = driver.find_elements(By.CSS_SELECTOR, 'input[class*="awsui_input_"]')
            check_stop_event(stop_event)
            Cardholder_Failsafe_GeneralError(driver)

            EID_ID = input_elements[1].get_attribute("id")

        check_stop_event(stop_event)
        Cardholder_Failsafe_GeneralError(driver)
        return EID_ID
    except (StopFunctionException, ElementClickInterceptedException, StaleElementReferenceException, CardHolder_General_Failsafe):
        return False

def CardHolder_GetID_Login(driver, StopFunctionException=None, check_stop_event=None, stop_event=None):
    global Login_ID
    try:
        check_stop_event(stop_event)
        Cardholder_Failsafe_GeneralError(driver)
        if Login_ID is None:
            # Find all input elements with the specified class name
            input_elements = driver.find_elements(By.CSS_SELECTOR, 'input[class*="awsui_input_"]')
            check_stop_event(stop_event)
            Cardholder_Failsafe_GeneralError(driver)

            Login_ID = input_elements[0].get_attribute("id")

        check_stop_event(stop_event)
        Cardholder_Failsafe_GeneralError(driver)
        return Login_ID
    except (StopFunctionException, ElementClickInterceptedException, StaleElementReferenceException, CardHolder_General_Failsafe):
        return False

def CardHolder_GetElement_SearchButton(driver, StopFunctionException=None, check_stop_event=None, stop_event=None):
    global SearchButton_Element
    try:
        check_stop_event(stop_event)
        Cardholder_Failsafe_GeneralError(driver)
        if SearchButton_Element is None:
            Button_Elements = driver.find_elements(By.CSS_SELECTOR, "[class*='awsui_button_vjswe']")
            SearchButton_Element = Button_Elements[2]

        check_stop_event(stop_event)
        Cardholder_Failsafe_GeneralError(driver)
        return SearchButton_Element
    except (StopFunctionException, ElementClickInterceptedException, StaleElementReferenceException, CardHolder_General_Failsafe):
        return False

def CardHolder_Paste_EID(driver, StopFunctionException=None, check_stop_event=None, stop_event=None):
    try:
        for attempt in range(2):
            try:
                if EID_ID is None:
                    # Get the EID_ID if not already obtained
                    ReturnID = CardHolder_GetID_EID(driver, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)

                check_stop_event(stop_event)
                Cardholder_Failsafe_GeneralError(driver)
            
                input_element = driver.find_element(By.ID, ReturnID)
                actions = ActionChains(driver)
                actions.click(input_element).click(input_element).click(input_element).perform()

                time.sleep(gtime)
                check_stop_event(stop_event)
                Cardholder_Failsafe_GeneralError(driver)

                clipboard_text = driver.execute_script("return navigator.clipboard.readText();")
                input_element.send_keys(clipboard_text)
                time.sleep(gtime)

                check_stop_event(stop_event)
                Cardholder_Failsafe_GeneralError(driver)
                input_element.send_keys(Keys.ENTER)
                return
            except NoSuchElementException:
                global EID_ID
                EID_ID = None
                continue

    except (StopFunctionException, ElementClickInterceptedException, StaleElementReferenceException, CardHolder_General_Failsafe):
        return False

def CardHolder_Paste_Login(driver, StopFunctionException=None, check_stop_event=None, stop_event=None):
    try:
        for attempt in range(2):
            try:
                if Login_ID:
                    # Get the EID_ID if not already obtained
                    ReturnID = CardHolder_GetID_Login(driver, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                
                check_stop_event(stop_event)
                Cardholder_Failsafe_GeneralError(driver)

                input_element = driver.find_element(By.ID, ReturnID)
                actions = ActionChains(driver)
                actions.click(input_element).click(input_element).click(input_element).perform()

                time.sleep(gtime)
                check_stop_event(stop_event)
                Cardholder_Failsafe_GeneralError(driver)

                clipboard_text = driver.execute_script("return navigator.clipboard.readText();")
                check_stop_event(stop_event)
                Cardholder_Failsafe_GeneralError(driver)
                input_element.send_keys(clipboard_text)
                time.sleep(gtime)

                check_stop_event(stop_event)
                Cardholder_Failsafe_GeneralError(driver)
                input_element.send_keys(Keys.ENTER)
                return
            except NoSuchElementException:
                global Login_ID
                Login_ID = None
                continue

    except (StopFunctionException, ElementClickInterceptedException, StaleElementReferenceException, CardHolder_General_Failsafe):
        return False

def Cardholder_Verify_ProfileLoaded(driver, StopFunctionException=None, check_stop_event=None, stop_event=None):
    try:
        current_time = datetime.datetime.now()
        print(f"Cardholder_Verify_ProfileLoaded: Trigger1 @ {current_time}")
        elements = driver.find_elements(By.CSS_SELECTOR, 'div[class*="awsui_content_1d2i7"]')
        time.sleep(gtime)
        # Iterate through the elements
        for element in elements:
            check_stop_event(stop_event)
            Cardholder_Failsafe_GeneralError(driver)
            # Check if the element contains the desired text
            if "Cannot find cardholder, please modify search fields and try again." in element.text:
                check_stop_event(stop_event)
                Cardholder_Failsafe_GeneralError(driver)
                current_time = datetime.datetime.now()
                print(f"Cardholder_Verify_ProfileLoaded: Trigger2 @ {current_time}")
                return True, False  # Found the desired text, return False

        # If the loop completes without finding the desired text, return True
        check_stop_event(stop_event)
        Cardholder_Failsafe_GeneralError(driver)
        current_time = datetime.datetime.now()
        print(f"Cardholder_Verify_ProfileLoaded: Trigger3 @ {current_time}")
        return True, True
    except (StopFunctionException, ElementClickInterceptedException, StaleElementReferenceException, CardHolder_General_Failsafe):
        return False, False

def CardHolder_WaitFor_Loading(driver, MainProfile=False, Element=None, StopFunctionException=None, check_stop_event=None, stop_event=None):
    try:
        current_time = datetime.datetime.now()
        print(f"CardHolder_WaitFor_Loading: Trigger1 @ {current_time}")
        Time = 0

        for attempt in range(30):
            check_stop_event(stop_event)
            Cardholder_Failsafe_GeneralError(driver)
            if MainProfile:
                print(f"Wainting for MainProfile: {Time} Seconds")
                Time = Time + 1
                class_name = Element.get_attribute('class')
                
                if 'awsui_disabled_vjswe' in class_name:
                    time.sleep(1)  # Short delay between attempts
                else:
                    time.sleep(gtime)
                    current_time = datetime.datetime.now()
                    print(f"CardHolder_WaitFor_Loading: Trigger2 @ {current_time}")
                    return True, True
            else:
                print(f"Wainting for other Values: {Time} Seconds")
                Time = Time + 1
                try:
                    driver.find_element(By.CSS_SELECTOR, "[class*='awsui_icon_1cbgc']")
                    time.sleep(1)
                except NoSuchElementException:
                    time.sleep(gtime)
                    current_time = datetime.datetime.now()
                    print(f"CardHolder_WaitFor_Loading: Trigger3 @ {current_time}")
                    return True, True

        # Final status if the loop completes without returning
        current_time = datetime.datetime.now()
        print(f"CardHolder_WaitFor_Loading: Trigger4 @ {current_time}")
        return True, False
    
    except (StopFunctionException, ElementClickInterceptedException, CardHolder_General_Failsafe) as E:
        # StaleElementReferenceException
        print(E)
        return False, False
    except Exception as E:
        print(E)
        return False, False

def Cardholder_TryAgain_LoadProfile(driver, settings=None, StopFunctionException=None, check_stop_event=None, stop_event=None):
    try:
        SearchBy_EID, SearchBy_Login, _ = settings.get("SearchBy_Column_Widget", [True, False, "A"])        
        check_stop_event(stop_event)
        Cardholder_Failsafe_GeneralError(driver)

        pyautogui.press('esc')
        time.sleep(gtime)

        if SearchBy_EID:
            CardHolder_Paste_EID(driver, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
            return True
        elif SearchBy_Login:
            CardHolder_Paste_Login(driver, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
            return True
        else:
            print("Invalid Paste method, Failsafe Measure Ending Script")
            return False
                
    except (StopFunctionException, ElementClickInterceptedException, CardHolder_General_Failsafe) as E:
        # StaleElementReferenceException
        print(E)
        return False
    except Exception as E:
        print(E)
        return False

def CardHolder_ClickOn_BadgeTab(driver):
    for attempt in range(5):
        elements = driver.find_elements(By.CSS_SELECTOR, 'span[class*="awsui_tabs-tab-label_14rmt"]')
        for element in elements:
            if element.text == "Badge":
                element.click()
                return  # Break the loop after clicking the text "Badge"
        time.sleep(gtime)

def CardHolder_ClickOn_AccessLvlTab(driver):
    for attempt in range(5):
        elements = driver.find_elements(By.CSS_SELECTOR, 'span[class*="awsui_tabs-tab-label_14rmt"]')
        for element in elements:
            if element.text == "Access Level":
                element.click()
                return  # Break the loop after clicking the text "Cardholder",
        time.sleep(gtime)

def CardHolder_ClickOn_SortActiveBadge(driver):
    try:
        # Find the div element with the specified class name and text
        xpath = '//div[contains(@class, "awsui_header-cell-text_1spae") and text()="Activate On"]'
        ActiveSort = driver.find_element(By.XPATH, xpath)
        ActiveSort.click()
        time.sleep(0.5)
        ActiveSort.click()
        time.sleep(0.5)
    except ElementClickInterceptedException:
        return

def CardHolder_GetInfo_ProfileInfo(driver, StopFunctionException=None, check_stop_event=None, stop_event=None):
    try:
        current_time = datetime.datetime.now()
        print(f"CardHolder_GetInfo_ProfileInfo: Trigger1 @ {current_time}")
        check_stop_event(stop_event)
        Cardholder_Failsafe_GeneralError(driver)
        # Find all input elements with the specified class names
        input_elements = driver.find_elements(By.CSS_SELECTOR, 'input[class*="awsui_input_"]')
        values = []

        check_stop_event(stop_event)
        Cardholder_Failsafe_GeneralError(driver)

        for i in range(7, 19):
            check_stop_event(stop_event)
            Cardholder_Failsafe_GeneralError(driver)
            # Get the value attribute from each input element
            value = input_elements[i].get_attribute('value')

            # Append the value to the values list
            values.append(value)

        if '/' in values[11]:
            values[11] = values[11].split('/')[0]

        check_stop_event(stop_event)
        Cardholder_Failsafe_GeneralError(driver)

        # Return the extracted values
        current_time = datetime.datetime.now()
        print(f"CardHolder_GetInfo_ProfileInfo: Trigger2 @ {current_time}")
        return values
    except (StopFunctionException, ElementClickInterceptedException, StaleElementReferenceException, IndexError, CardHolder_General_Failsafe):
        return False

def CardHolder_GetInfo_BadgeInfo(driver, StopFunctionException=None, check_stop_event=None, stop_event=None):
    try:
        Tr_Elements = driver.find_elements(By.CSS_SELECTOR, 'tr[class*="awsui_row_wih1l"]')
        found_element = None  # Initialize a variable to store the found element

        for element in Tr_Elements:
            check_stop_event(stop_event)
            Cardholder_Failsafe_GeneralError(driver)
            try:
                # Try to find the child element with the specific class name
                child_element = element.find_element(By.CSS_SELECTOR, 'span[class*="awsui_badge-color-green"]')
                if child_element:
                    check_stop_event(stop_event)
                    Cardholder_Failsafe_GeneralError(driver)
                    found_element = element  # Store the parent element
                    break  # Exit the loop as we found the desired element
            except NoSuchElementException:
                check_stop_event(stop_event)
                Cardholder_Failsafe_GeneralError(driver)
                continue  # If the child element is not found, continue to the next parent element

        if found_element:
            tr_element = found_element
            check_stop_event(stop_event)
            Cardholder_Failsafe_GeneralError(driver)
        else:
            check_stop_event(stop_event)
            Cardholder_Failsafe_GeneralError(driver)
            CardHolder_ClickOn_SortActiveBadge(driver)
            check_stop_event(stop_event)
            Cardholder_Failsafe_GeneralError(driver)

            # Find the tr element with partial class name and specific aria-rowindex attribute
            tr_element = driver.find_element(By.CSS_SELECTOR, 'tr[class^="awsui_row_wih1l"][aria-rowindex="2"]')

        # Find all td elements within the tr element
        td_elements = tr_element.find_elements(By.CSS_SELECTOR, 'td[class*="awsui_body-cell_c6tup"]')
        check_stop_event(stop_event)
        Cardholder_Failsafe_GeneralError(driver)

        # Initialize a list to store the extracted values
        values = []

        # Iterate through the first nine td elements
        for index, td_element in enumerate(td_elements[1:10], start=1):
            check_stop_event(stop_event)
            Cardholder_Failsafe_GeneralError(driver)
            value = td_element.text.strip()
            values.append(value)

        check_stop_event(stop_event)
        Cardholder_Failsafe_GeneralError(driver)

        try:
            ActiveBadgeElement = driver.find_element(By.CSS_SELECTOR, 'span[class*="awsui_badge-color-green"]')
            check_stop_event(stop_event)
            Cardholder_Failsafe_GeneralError(driver)
            values.append(True)
            check_stop_event(stop_event)
            Cardholder_Failsafe_GeneralError(driver)
            return values
        except NoSuchElementException:
            check_stop_event(stop_event)
            Cardholder_Failsafe_GeneralError(driver)
            values.append(False)
            check_stop_event(stop_event)
            Cardholder_Failsafe_GeneralError(driver)
            return values

    except (StopFunctionException, ElementClickInterceptedException, StaleElementReferenceException, IndexError, CardHolder_General_Failsafe):
        print("Returning False")
        return False

def CardHolder_GetInfo_AccessLvlInfo(driver, settings, StopFunctionException=None, check_stop_event=None, stop_event=None):
    try:
        check_stop_event(stop_event)

        # Find the input element with the specified class name
        input_element = driver.find_element(By.CSS_SELECTOR, 'input[class*="awsui_input-type-search"]')
        input_element.click()

        Home_Site = settings.get("Home_Site", "KAFW")
        Home_Site_Access = f"{Home_Site}-1-GENERAL ACCESS"
        pyperclip.copy(Home_Site_Access)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)

        Values = []

        try:
            awsui_body_Elements = driver.find_elements(By.CSS_SELECTOR, 'div[class*="awsui_body-cell"]')

            if awsui_body_Elements[0].text.strip() == Home_Site_Access:
                for element in awsui_body_Elements:
                    text = element.text.strip()
                    Values.append(text)

                Values[0] = True
            else:
                for i in range(3):
                    Values.append(False)

        except (NoSuchElementException, IndexError):
            for i in range(3):
                Values.append(False)


        CountElement = driver.find_element(By.CSS_SELECTOR, 'span[class*="awsui_counter_"]')
        CountText = CountElement.text.strip().replace('(', '').replace(')', '')
        Values.append(CountText)

        return Values

    except (StopFunctionException, ElementClickInterceptedException, StaleElementReferenceException, CardHolder_General_Failsafe) as E:
        print(E)
        return False

# ------------------------------------------------------------------------------------------------------------------------------------------ #

def Quip_GetInfo_CellText(driver, row=0, column=0, StopFunctionException=None, check_stop_event=None, stop_event=None):
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

def Quip_ClickOn_Cell(driver, row=0, column=0, StopFunctionException=None, check_stop_event=None, stop_event=None):
    def ExceptionFunction(driver, row, StopFunctionException=None, check_stop_event=None, stop_event=None):
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
                if not ExceptionFunction(driver, row, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event):
                    return False
            """except ElementClickInterceptedException:
                ExceptionFunction(driver, row, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)"""

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

def Quip_Check_CommandLine(driver, row=0, column=0, StopFunctionException=None, check_stop_event=None, stop_event=None):
    try:
        result = Quip_GetInfo_CellText(driver, row, column, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
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

def Quip_GetInfo_LegalName(driver, StopFunctionException=None, check_stop_event=None, stop_event=None):
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

def Quip_Color_Cells(driver, Color, WorkingRow, Column="0", Row=True, StopFunctionException=None, check_stop_event=None, stop_event=None):
    try:
        try:
            pyautogui.press('esc')
            check_stop_event(stop_event)
            #time.sleep(gtime)
            Quip_ClickOn_Cell(driver, WorkingRow, Column, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
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
