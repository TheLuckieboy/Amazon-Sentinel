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
    try:
        current_time = datetime.datetime.now()
        print(f"Cardholder_Verification_Script: Trigger1 @ {current_time}")
        def SwithTo_Window(QuipWindow=False, CardholderWindow=False):
            check_stop_event(stop_event)
            if QuipWindow:
                driver.switch_to.window(window_handles[0])
                check_stop_event(stop_event)
                time.sleep(gtime)

            if CardholderWindow:
                driver.switch_to.window(window_handles[1])
                check_stop_event(stop_event)
                Cardholder_Failsafe_GeneralError(driver)
                time.sleep(gtime)

        check_stop_event(stop_event)
        if WorkingRow <= 0:
            print("Starting Row can not be 1")
            return False

        CommandLineColumn = ord((settings.get("CommandLine Column", "A")).upper()) - ord('A')
        SearchBy_EID, SearchBy_Login, SearchByColumn = settings.get("SearchBy_Column_Widget", [True, False, "A"])
        SearchByColumn = ord(SearchByColumn) - ord('A')

        Quip_Database = settings.get("Quip_Database", False)
        Excel_Database = settings.get("Excel_Database", True)
        Home_Site = settings.get("Home_Site_Widget", "KAFW")

        if Quip_Database and not Excel_Database:
            def SwitchBack_FailsafeColoring():
                check_stop_event(stop_event)
                # Switch to Quip, and write info to Quip Database
                driver.switch_to.window(window_handles[0])
                check_stop_event(stop_event)
                time.sleep(gtime)

                # Iterate over settings and perform actions
                settings_to_process = ["*Fail Safe Measure* Bad EID/Login_Widget"]
                check_stop_event(stop_event)
                time.sleep(gtime)
                for setting_name in settings_to_process:
                    check_stop_event(stop_event)
                    boolean_value, Color = settings.get(setting_name)
                    if boolean_value:
                        check_stop_event(stop_event)
                        Quip_Color_Cells(driver, Color, WorkingRow, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                        pyautogui.press('esc')

            def Write_InfoTo_Quip(ProfileValues, BadgeValues=None, AccessValues=None,
                                  Badge_Tab=True, AccessLvl_Tab=True):
                check_stop_event(stop_event)
                # Iterate over settings and perform actions
                Cardholder_Tab_Settings = [
                    "EID_Widget", "Login_Widget", "FirstName_Widget", "LastName_Widget", "EmployeeType_Widget",
                    "EmployeeStatus_Widget", "ManagerLogin_Widget", "PersonID_Widget", "Barcode_Widget",
                    "Tenure_Widget", "Region_Widget", "Building_Widget"
                ]
                Badge_Tab_Settings = [
                    "BadgeStatus_Widget", "BadgeType_Widget", "BadgeCount_Widget", "BadgeID_Widget",
                    "ActiveOn_Widget_Badge", "DeactiveOn_Widget_Badge", "LastUpdate_Widget", "LastRead_Widget",
                    "LastTimestamp_Widget", "EventType_Widget", "ActiveBadgePresent_Widget"
                ]
                AccessLvl_Tab_Settings = [
                    "GeneralAccess_Widget", "AccessLvlCount_Widget", "ActivateOn_Widget_AccessLvl",
                    "DeactiveOn_Widget_AccessLvl"
                ]
                Cardholder_Tab_Info_Widget = settings.get("Cardholder_Tab_Info_Widget", False)
                Badge_Tab_Info_Widget = settings.get("Badge_Tab_Info_Widget", False)
                AccessLvl_Tab_Info_Widget = settings.get("AccessLvl_Tab_Info_Widget", False)
                
                def Cardholder_Settings():
                    for setting_name in Cardholder_Tab_Settings:
                        check_stop_event(stop_event)
                        boolean_value, column_name = settings.get(setting_name, [False, "A"])
                        if boolean_value:
                            check_stop_event(stop_event)
                            try:
                                column_name = ord(column_name.upper()) - ord('A')
                            except TypeError:
                                column_name = 6

                            if setting_name == "EID_Widget":
                                check_stop_event(stop_event)
                                print(f"{WorkingRow}, {column_name}")
                                Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                pyperclip.copy(str(ProfileValues[1]))
                                check_stop_event(stop_event)
                                pyautogui.hotkey('ctrl', 'v')
                            elif setting_name == "Login_Widget":
                                check_stop_event(stop_event)
                                Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                pyperclip.copy(str(ProfileValues[0]))
                                check_stop_event(stop_event)
                                pyautogui.hotkey('ctrl', 'v')
                            elif setting_name == "FirstName_Widget":
                                boolean_value, column_name2 = settings.get("LastName_Widget", [False, "A"])
                                column_name2 = ord(column_name2.upper()) - ord('A')
                                if boolean_value and (column_name2 == column_name):
                                    check_stop_event(stop_event)
                                    Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    check_stop_event(stop_event)
                                    if settings.get("LastNameComma_FirstName_CardholderVerification"):
                                        pyperclip.copy(f"{ProfileValues[5]}, {ProfileValues[4]}")
                                    elif settings.get("FirstNameComma_LastName_CardholderVerification"):
                                        pyperclip.copy(f"{ProfileValues[4]}, {ProfileValues[5]}")
                                    elif settings.get("FirstName_LastName_CardholderVerification"):
                                        pyperclip.copy(f"{ProfileValues[4]} {ProfileValues[5]}")
                                    check_stop_event(stop_event)
                                    pyautogui.hotkey('ctrl', 'v')
                                else:
                                    check_stop_event(stop_event)
                                    Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    pyperclip.copy(str(ProfileValues[4]))
                                    check_stop_event(stop_event)
                                pyautogui.hotkey('ctrl', 'v')
                            elif setting_name == "LastName_Widget":
                                check_stop_event(stop_event)
                                boolean_value, column_name2 = settings.get("FirstName_Widget", [False, "A"])
                                column_name2 = ord(column_name2.upper()) - ord('A')
                                check_stop_event(stop_event)
                                if boolean_value and (column_name2 == column_name):
                                    check_stop_event(stop_event)
                                else:
                                    check_stop_event(stop_event)
                                    Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    pyperclip.copy(str(ProfileValues[5]))
                                    check_stop_event(stop_event)
                                pyautogui.hotkey('ctrl', 'v')
                            elif setting_name == "EmployeeType_Widget":
                                check_stop_event(stop_event)
                                Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                pyperclip.copy(str(ProfileValues[6]))
                                check_stop_event(stop_event)
                                pyautogui.hotkey('ctrl', 'v')
                            elif setting_name == "EmployeeStatus_Widget":
                                check_stop_event(stop_event)
                                Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                pyperclip.copy(str(ProfileValues[7]))
                                check_stop_event(stop_event)
                                pyautogui.hotkey('ctrl', 'v')
                            elif setting_name == "ManagerLogin_Widget":
                                check_stop_event(stop_event)
                                Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                pyperclip.copy(str(ProfileValues[8]))
                                check_stop_event(stop_event)
                                pyautogui.hotkey('ctrl', 'v')
                            elif setting_name == "PersonID_Widget":
                                check_stop_event(stop_event)
                                Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                pyperclip.copy(str(ProfileValues[2]))
                                check_stop_event(stop_event)
                                pyautogui.hotkey('ctrl', 'v')
                            elif setting_name == "Barcode_Widget":
                                check_stop_event(stop_event)
                                Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                pyperclip.copy(str(ProfileValues[3]))
                                check_stop_event(stop_event)
                                pyautogui.hotkey('ctrl', 'v')
                            elif setting_name == "Tenure_Widget":
                                check_stop_event(stop_event)
                                Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                pyperclip.copy(str(ProfileValues[9]))
                                check_stop_event(stop_event)
                                pyautogui.hotkey('ctrl', 'v')
                            elif setting_name == "Region_Widget":
                                check_stop_event(stop_event)
                                Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                pyperclip.copy(str(ProfileValues[10]))
                                check_stop_event(stop_event)
                                pyautogui.hotkey('ctrl', 'v')
                            elif setting_name == "Building_Widget":
                                check_stop_event(stop_event)
                                Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                pyperclip.copy(str(ProfileValues[11]))
                                check_stop_event(stop_event)
                                pyautogui.hotkey('ctrl', 'v')

                def Badge_Settings():
                    for setting_name in Badge_Tab_Settings:
                        check_stop_event(stop_event)
                        boolean_value, column_name = settings.get(setting_name, [False, "A"])
                        if boolean_value:
                            check_stop_event(stop_event)
                            try:
                                column_name = ord(column_name.upper()) - ord('A')
                            except TypeError:
                                column_name = 6

                            if BadgeValues is not None:
                                if setting_name == "BadgeStatus_Widget":
                                    check_stop_event(stop_event)
                                    Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    pyperclip.copy(str(BadgeValues[1]))
                                    check_stop_event(stop_event)
                                    pyautogui.hotkey('ctrl', 'v')
                                elif setting_name == "BadgeType_Widget":
                                    check_stop_event(stop_event)
                                    Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    pyperclip.copy(str(BadgeValues[2]))
                                    check_stop_event(stop_event)
                                    pyautogui.hotkey('ctrl', 'v')
                                elif setting_name == "BadgeCount_Widget":
                                    check_stop_event(stop_event)
                                    Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    pyperclip.copy(str(BadgeValues[10]))
                                    check_stop_event(stop_event)
                                    pyautogui.hotkey('ctrl', 'v')
                                elif setting_name == "BadgeID_Widget":
                                    check_stop_event(stop_event)
                                    Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    pyperclip.copy(str(BadgeValues[0]))
                                    check_stop_event(stop_event)
                                    pyautogui.hotkey('ctrl', 'v')
                                elif setting_name == "ActiveOn_Widget_Badge":
                                    check_stop_event(stop_event)
                                    Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    pyperclip.copy(str(BadgeValues[3]))
                                    check_stop_event(stop_event)
                                    pyautogui.hotkey('ctrl', 'v')
                                elif setting_name == "DeactiveOn_Widget_Badge":
                                    check_stop_event(stop_event)
                                    Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    pyperclip.copy(str(BadgeValues[4]))
                                    check_stop_event(stop_event)
                                    pyautogui.hotkey('ctrl', 'v')
                                elif setting_name == "LastUpdate_Widget":
                                    check_stop_event(stop_event)
                                    Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    pyperclip.copy(str(BadgeValues[5]))
                                    check_stop_event(stop_event)
                                    pyautogui.hotkey('ctrl', 'v')
                                elif setting_name == "LastRead_Widget":
                                    check_stop_event(stop_event)
                                    Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    pyperclip.copy(str(BadgeValues[6]))
                                    check_stop_event(stop_event)
                                    pyautogui.hotkey('ctrl', 'v')
                                elif setting_name == "LastTimestamp_Widget":
                                    check_stop_event(stop_event)
                                    Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    pyperclip.copy(str(BadgeValues[7]))
                                    check_stop_event(stop_event)
                                    pyautogui.hotkey('ctrl', 'v')
                                elif setting_name == "EventType_Widget":
                                    check_stop_event(stop_event)
                                    Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    pyperclip.copy(str(BadgeValues[8]))
                                    check_stop_event(stop_event)
                                    pyautogui.hotkey('ctrl', 'v')
                                elif setting_name == "ActiveBadgePresent_Widget":
                                    check_stop_event(stop_event)
                                    Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    pyperclip.copy(str(BadgeValues[9]))
                                    check_stop_event(stop_event)
                                    pyautogui.hotkey('ctrl', 'v')
                            else:
                                check_stop_event(stop_event)
                                Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                pyperclip.copy("No Badge Info Available")
                                check_stop_event(stop_event)
                                pyautogui.hotkey('ctrl', 'v')

                def AccessLvl_Settings():
                    for setting_name in AccessLvl_Tab_Settings:
                        check_stop_event(stop_event)
                        boolean_value, column_name = settings.get(setting_name, [False, "A"])
                        if boolean_value:
                            check_stop_event(stop_event)
                            try:
                                column_name = ord(column_name.upper()) - ord('A')
                            except TypeError:
                                column_name = 6

                            if AccessValues is not None:
                                check_stop_event(stop_event)
                                if (setting_name == "GeneralAccess_Widget") and AccessValues[0]:
                                    check_stop_event(stop_event)
                                    Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    pyperclip.copy("Has Access to Site")
                                    check_stop_event(stop_event)
                                    pyautogui.hotkey('ctrl', 'v')
                                elif (setting_name == "ActivateOn_Widget_AccessLvl") and AccessValues[0]:
                                    check_stop_event(stop_event)
                                    Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    pyperclip.copy(str(AccessValues[1]))
                                    check_stop_event(stop_event)
                                    pyautogui.hotkey('ctrl', 'v')
                                elif (setting_name == "DeactiveOn_Widget_AccessLvl") and AccessValues[0]:
                                    check_stop_event(stop_event)
                                    Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    pyperclip.copy(str(AccessValues[2]))
                                    check_stop_event(stop_event)
                                    pyautogui.hotkey('ctrl', 'v')
                                elif setting_name == "AccessLvlCount_Widget":
                                    check_stop_event(stop_event)
                                    Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    pyperclip.copy(str(AccessValues[3]))
                                    check_stop_event(stop_event)
                                    pyautogui.hotkey('ctrl', 'v')
                                else:
                                    check_stop_event(stop_event)
                                    Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    pyperclip.copy("Does not have Access to Site")
                                    check_stop_event(stop_event)
                                    pyautogui.hotkey('ctrl', 'v')
                            else:
                                check_stop_event(stop_event)
                                Quip_ClickOn_Cell(driver, WorkingRow, column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                pyperclip.copy("Does not have Access to Site")
                                check_stop_event(stop_event)
                                pyautogui.hotkey('ctrl', 'v')

                if Cardholder_Tab_Info_Widget:
                    Cardholder_Settings()
                if Badge_Tab_Info_Widget and Badge_Tab:
                    Badge_Settings()
                if AccessLvl_Tab_Info_Widget and AccessLvl_Tab:
                    AccessLvl_Settings()

            def Color_InfoTo_Quip(ProfileValues, AllInfo=False, TerminatedStatus=False, NoBadges=False, InActiveBadge=False, BadgeValues=None, Cardholder_Tab=False):
                if settings.get("ColorCodeSettings_Widget", False):
                    if AllInfo:
                        # Iterate over settings and perform actions
                        settings_to_process = [
                            "Active AA, Active Badge @ Site_Widget", "Active AA, Active Badge @ Other Site_Widget",
                            "Active AA, Inactive Badge @ Site_Widget", "Active AA, Inactive Badge @ Other Site_Widget",
                            "Terminated AA @ Site_Widget", "Terminated AA @ Other Site_Widget"
                        ]
                        for setting_name in settings_to_process:
                            check_stop_event(stop_event)
                            boolean_value, Color = settings.get(setting_name, (False, None))
                            if boolean_value:
                                if setting_name == "Active AA, Active Badge @ Site_Widget" and ProfileValues[7] != "Terminated" and \
                                        ProfileValues[11] == Home_Site and BadgeValues[1] == "Active":
                                    check_stop_event(stop_event)
                                    Quip_Color_Cells(driver, Color, WorkingRow, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    check_stop_event(stop_event)
                                    pyautogui.press('esc')
                                elif setting_name == "Active AA, Active Badge @ Other Site_Widget" and ProfileValues[
                                    4] != "Terminated" and \
                                        ProfileValues[11] != Home_Site and BadgeValues[1] == "Active":
                                    check_stop_event(stop_event)
                                    Quip_Color_Cells(driver, Color, WorkingRow, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    check_stop_event(stop_event)
                                    pyautogui.press('esc')
                                elif setting_name == "Active AA, Inactive Badge @ Site_Widget" and ProfileValues[
                                    4] != "Terminated" and \
                                        ProfileValues[11] == Home_Site and BadgeValues[1] != "Active" and BadgeValues[
                                    0] != "Terminated":
                                    check_stop_event(stop_event)
                                    Quip_Color_Cells(driver, Color, WorkingRow, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    check_stop_event(stop_event)
                                    pyautogui.press('esc')
                                elif setting_name == "Active AA, Inactive Badge @ Other Site_Widget" and ProfileValues[
                                    4] != "Terminated" and ProfileValues[11] != Home_Site and BadgeValues[1] != "Active" and \
                                        BadgeValues[1] != "Terminated":
                                    check_stop_event(stop_event)
                                    Quip_Color_Cells(driver, Color, WorkingRow, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    check_stop_event(stop_event)
                                    pyautogui.press('esc')
                                elif setting_name == "Terminated AA @ Site_Widget_Widget" and ProfileValues[11] == Home_Site and (
                                        BadgeValues[1] == "Terminated" or ProfileValues[7] == "Terminated"):
                                    check_stop_event(stop_event)
                                    Quip_Color_Cells(driver, Color, WorkingRow, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    check_stop_event(stop_event)
                                    pyautogui.press('esc')
                                elif setting_name == "Terminated AA @ Other Site_Widget" and ProfileValues[11] != Home_Site and (
                                        BadgeValues[1] == "Terminated" or ProfileValues[7] == "Terminated"):
                                    check_stop_event(stop_event)
                                    Quip_Color_Cells(driver, Color, WorkingRow, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    check_stop_event(stop_event)
                                    pyautogui.press('esc')

                    if TerminatedStatus:
                        # Iterate over settings and perform actions
                        settings_to_process = [
                            "Terminated AA @ Site_Widget", "Terminated AA @ Other Site_Widget"
                        ]
                        for setting_name in settings_to_process:
                            check_stop_event(stop_event)
                            boolean_value, Color = settings.get(setting_name, (False, None))
                            if boolean_value:
                                if setting_name == "Terminated AA @ Site_Widget" and ProfileValues[11] == Home_Site:
                                    check_stop_event(stop_event)
                                    Quip_Color_Cells(driver, Color, WorkingRow, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    check_stop_event(stop_event)
                                    pyautogui.press('esc')
                                elif setting_name == "Terminated AA @ Other Site_Widget" and ProfileValues[11] != Home_Site:
                                    check_stop_event(stop_event)
                                    Quip_Color_Cells(driver, Color, WorkingRow, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    check_stop_event(stop_event)
                                    pyautogui.press('esc')

                    if NoBadges:
                        if "year" in ProfileValues[9] or "years" in ProfileValues[9]:
                            TenureLength = True
                        else:
                            TenureLength = False

                        # Iterate over settings and perform actions
                        settings_to_process = [
                            "Active AA, Inactive Badge @ Site_Widget", "Active AA, Inactive Badge @ Other Site_Widget",
                            "Terminated AA @ Site_Widget", "Terminated AA @ Other Site_Widget"
                        ]
                        for setting_name in settings_to_process:
                            check_stop_event(stop_event)
                            boolean_value, Color = settings.get(setting_name, (False, None))
                            if boolean_value:
                                check_stop_event(stop_event)
                                if setting_name == "Active AA, Inactive Badge @ Site_Widget" and ProfileValues[
                                    7] != "Terminated" and \
                                        ProfileValues[11] == Home_Site and TenureLength == False:
                                    check_stop_event(stop_event)
                                    Quip_Color_Cells(driver, Color, WorkingRow, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    check_stop_event(stop_event)
                                    pyautogui.press('esc')
                                elif setting_name == "Active AA, Inactive Badge @ Other Site_Widget" and ProfileValues[
                                    7] != "Terminated" and ProfileValues[11] != Home_Site and TenureLength == False:
                                    check_stop_event(stop_event)
                                    Quip_Color_Cells(driver, Color, WorkingRow, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    check_stop_event(stop_event)
                                    pyautogui.press('esc')
                                elif setting_name == "Terminated AA @ Site_Widget" and ProfileValues[
                                    11] == Home_Site and TenureLength == True:
                                    check_stop_event(stop_event)
                                    Quip_Color_Cells(driver, Color, WorkingRow, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    check_stop_event(stop_event)
                                    pyautogui.press('esc')
                                elif setting_name == "Terminated AA @ Other Site_Widget" and ProfileValues[
                                    11] != Home_Site and TenureLength == True:
                                    check_stop_event(stop_event)
                                    Quip_Color_Cells(driver, Color, WorkingRow, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    check_stop_event(stop_event)
                                    pyautogui.press('esc')

                    if InActiveBadge:
                        # Iterate over settings and perform actions
                        settings_to_process = [
                            "Active AA, Inactive Badge @ Site_Widget", "Active AA, Inactive Badge @ Other Site_Widget"
                        ]
                        for setting_name in settings_to_process:
                            check_stop_event(stop_event)
                            boolean_value, Color = settings.get(setting_name, (False, None))
                            if boolean_value:
                                check_stop_event(stop_event)
                                if setting_name == "Active AA, Inactive Badge @ Site_Widget" and ProfileValues[7] != "Terminated" and ProfileValues[11] == Home_Site:
                                    check_stop_event(stop_event)
                                    Quip_Color_Cells(driver, Color, WorkingRow, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    check_stop_event(stop_event)
                                    pyautogui.press('esc')
                                elif setting_name == "Active AA, Inactive Badge @ Other Site_Widget" and ProfileValues[7] != "Terminated" and ProfileValues[11] != Home_Site:
                                    check_stop_event(stop_event)
                                    Quip_Color_Cells(driver, Color, WorkingRow, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    check_stop_event(stop_event)
                                    pyautogui.press('esc')

                    if Cardholder_Tab:
                        # Iterate over settings and perform actions
                        settings_to_process = [
                            "Active AA, Active Badge @ Site_Widget", "Active AA, Active Badge @ Other Site_Widget",
                            "Active AA, Inactive Badge @ Site_Widget", "Active AA, Inactive Badge @ Other Site_Widget"
                        ]
                        for setting_name in settings_to_process:
                            check_stop_event(stop_event)
                            boolean_value, Color = settings.get(setting_name, (False, None))
                            if boolean_value:
                                check_stop_event(stop_event)
                                if ProfileValues[7] != "Terminated":
                                    check_stop_event(stop_event)
                                    Quip_Color_Cells(driver, Color, WorkingRow, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    check_stop_event(stop_event)
                                    pyautogui.press('esc')
                                    break

                        settings_to_process = [
                            "Terminated AA @ Site_Widget", "Terminated AA @ Other Site_Widget",
                        ]
                        for setting_name in settings_to_process:
                            check_stop_event(stop_event)
                            boolean_value, Color = settings.get(setting_name, (False, None))
                            if boolean_value:
                                check_stop_event(stop_event)
                                if ProfileValues[7] == "Terminated":
                                    check_stop_event(stop_event)
                                    Quip_Color_Cells(driver, Color, WorkingRow, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    check_stop_event(stop_event)
                                    pyautogui.press('esc')
                                    break

                    check_stop_event(stop_event)

                    boolean_value, column_name, Color = settings.get("*Color a Column* Row Complete_Widget", (False, "A", None))
                    if boolean_value:
                        check_stop_event(stop_event)
                        try:
                            column_name = ord(column_name.upper()) - ord('A')
                        except TypeError:
                            column_name = 6
                        Quip_Color_Cells(driver, Color, WorkingRow, Row=False, Column=column_name, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                        pyautogui.press('esc')
            
            check_stop_event(stop_event)
            CommandLineResult = Quip_Check_CommandLine(driver, WorkingRow, CommandLineColumn, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
            check_stop_event(stop_event)
            if CommandLineResult == "skip":
                return True
            elif CommandLineResult != "stopall":
                check_stop_event(stop_event)
                if SearchBy_EID:
                    check_stop_event(stop_event)
                    Cardholder_Failsafe_GeneralError(driver)
                    EIDInfo = Quip_GetInfo_CellText(driver, WorkingRow, SearchByColumn, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                    if EIDInfo:
                        check_stop_event(stop_event)
                        time.sleep(gtime)
                        pyperclip.copy(EIDInfo)
                    else:
                        print(f"SearchBy_EID: {EIDInfo}")
                        return False
                elif SearchBy_Login:
                    check_stop_event(stop_event)
                    LoginInfo = Quip_GetInfo_CellText(driver, WorkingRow, SearchByColumn, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                    if LoginInfo:
                        check_stop_event(stop_event)
                        Cardholder_Failsafe_GeneralError(driver)
                        time.sleep(gtime)
                        pyperclip.copy(LoginInfo)
                    else:
                        print(f"SearchBy_Login: {LoginInfo}")
                        return False
                else:
                    print("Invalid SearchBy method, Failsafe Measure Ending Script")
                    return False
                time.sleep(gtime)
                Quip_ClickOn_Cell(driver, WorkingRow - 1, CommandLineColumn, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                check_stop_event(stop_event)
                pyautogui.press('down', presses=3)
                time.sleep(gtime)

                # Switch to Cardholder, and get info from AA profile
                SwithTo_Window(CardholderWindow=True)
                time.sleep(gtime)
                check_stop_event(stop_event)
                Cardholder_Failsafe_GeneralError(driver)

                # Get Search button Element
                SearchButton_Element = CardHolder_GetElement_SearchButton(driver, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                if SearchButton_Element is False:
                    print(f"SearchButton_Element: {SearchButton_Element}")
                    return False

                if SearchBy_EID:
                    check_stop_event(stop_event)
                    Cardholder_Failsafe_GeneralError(driver)
                    CardHolder_Paste_EID(driver, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                elif SearchBy_Login:
                    check_stop_event(stop_event)
                    Cardholder_Failsafe_GeneralError(driver)
                    CardHolder_Paste_Login(driver, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                else:
                    print("Invalid Paste method, Failsafe Measure Ending Script")
                    return False
                current_time = datetime.datetime.now()
                print(f"Cardholder_ProfileLoadedWithValues: Trigger1 @ {current_time}")
                
                check_stop_event(stop_event)
                Cardholder_Failsafe_GeneralError(driver)
                time.sleep(gtime)

                for LoadProfileAttempt in range(3):
                    ContinueStatus1, SearchBarResult = CardHolder_WaitFor_Loading(driver, MainProfile=True, Element=SearchButton_Element, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                    if ContinueStatus1:
                        if SearchBarResult:
                            ContinueStatus2, ProfileLoaded = Cardholder_Verify_ProfileLoaded(driver, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                            if ContinueStatus2:
                                if ProfileLoaded is False:
                                    # Retry
                                    print(f"Profile Load attempt Failed {LoadProfileAttempt}")
                                    TryAgain = Cardholder_TryAgain_LoadProfile(driver, settings=settings, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    if TryAgain is False:
                                        print(f"TryAgain: {TryAgain}")
                                        return False
                                    continue
                                else:
                                    # continue with script
                                    check_stop_event(stop_event)
                                    Cardholder_Failsafe_GeneralError(driver)
                                    
                                    # In Cardholder Management System, get AA Information
                                    CardHolder_ClickOn_BadgeTab(driver)  # Click on Badge Tab
                                    ProfileValues = CardHolder_GetInfo_ProfileInfo(driver, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                    print(ProfileValues)

                                    current_time = datetime.datetime.now()
                                    print(f"Cardholder_ProfileLoadedWithValues: Trigger2 @ {current_time}")

                                    if ProfileValues:
                                        if ProfileValues[7] == "Terminated":
                                            check_stop_event(stop_event)
                                            Cardholder_Failsafe_GeneralError(driver)
                                            time.sleep(gtime)

                                            # Switch to Quip, and write info to Quip Database
                                            SwithTo_Window(QuipWindow=True)
                                            check_stop_event(stop_event)

                                            Write_InfoTo_Quip(ProfileValues)
                                            Color_InfoTo_Quip(ProfileValues, TerminatedStatus=True)
                                            return True

                                        if ProfileValues[7] == "Suspended":
                                            check_stop_event(stop_event)
                                            Cardholder_Failsafe_GeneralError(driver)
                                            time.sleep(gtime)

                                            # Switch to Quip, and write info to Quip Database
                                            SwithTo_Window(QuipWindow=True)
                                            check_stop_event(stop_event)

                                            Write_InfoTo_Quip(ProfileValues)
                                            Color_InfoTo_Quip(ProfileValues, InActiveBadge=True)
                                            return True

                                        if settings.get("Badge_Tab_Info_Widget", False):
                                            check_stop_event(stop_event)
                                            Cardholder_Failsafe_GeneralError(driver)

                                            BadgeContinueStatus, BadgeValuesLoaded = CardHolder_WaitFor_Loading(driver, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)

                                            if BadgeContinueStatus:
                                                if BadgeValuesLoaded:
                                                    BadgeNumberElement = driver.find_element(By.CSS_SELECTOR, 'span[class*="awsui_counter_2qdw9"]')

                                                    if BadgeNumberElement.text == "(0)":
                                                        check_stop_event(stop_event)
                                                        Cardholder_Failsafe_GeneralError(driver)
                                                        check_stop_event(stop_event)
                                                        Cardholder_Failsafe_GeneralError(driver)
                                                        time.sleep(gtime)

                                                        # Switch to Quip, and write info to Quip Database
                                                        SwithTo_Window(QuipWindow=True)

                                                        Write_InfoTo_Quip(ProfileValues)
                                                        Color_InfoTo_Quip(ProfileValues, NoBadges=True)

                                                        check_stop_event(stop_event)
                                                        return True
                                                    else:
                                                        check_stop_event(stop_event)
                                                        Cardholder_Failsafe_GeneralError(driver)
                                                        time.sleep(gtime)

                                                        BadgeValues = CardHolder_GetInfo_BadgeInfo(driver, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                                        print(BadgeValues)

                                                        badge_number_text = BadgeNumberElement.text.strip().replace('(', '').replace(')', '')
                                                        BadgeValues.append(badge_number_text)

                                                        if BadgeValues:
                                                            if not BadgeValues[9]:
                                                                badge_actions = {
                                                                    "Returned": {"TerminatedStatus": True},
                                                                    "Terminated": {"TerminatedStatus": True},
                                                                    "Lost": {"InActiveBadge": True},
                                                                    "Broken": {"InActiveBadge": True},
                                                                    "Use/Lose (System)": {"InActiveBadge": True},
                                                                    "In the Mail": {"InActiveBadge": True},
                                                                    "IFMB Issued": {"InActiveBadge": True},
                                                                    "Suspended": {"InActiveBadge": True},
                                                                    "Expired (System)": {"InActiveBadge": True},
                                                                }
                                                                action = badge_actions.get(BadgeValues[1])
                                                                if action:
                                                                    check_stop_event(stop_event)
                                                                    Cardholder_Failsafe_GeneralError(driver)
                                                                    time.sleep(gtime)

                                                                    # Switch to Quip, and write info to Quip Database
                                                                    SwithTo_Window(QuipWindow=True)

                                                                    Write_InfoTo_Quip(ProfileValues, BadgeValues=BadgeValues)
                                                                    Color_InfoTo_Quip(ProfileValues, BadgeValues=BadgeValues, **action)
                                                                    return True
                                                                else:
                                                                    print("action", action)
                                                                    return False
                                                            else:
                                                                if settings.get("AccessLvl_Tab_Info_Widget", False):
                                                                    CardHolder_ClickOn_AccessLvlTab(driver)  # Click on AccessLvl Tab
                                                                    check_stop_event(stop_event)
                                                                    Cardholder_Failsafe_GeneralError(driver)

                                                                    AccessContinueStatus, AccessValuesLoaded = CardHolder_WaitFor_Loading(driver, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                                                    if AccessContinueStatus:
                                                                        if AccessValuesLoaded:
                                                                            check_stop_event(stop_event)
                                                                            Cardholder_Failsafe_GeneralError(driver)
                                                                            time.sleep(gtime)

                                                                            AccessValues = CardHolder_GetInfo_AccessLvlInfo(driver, settings=settings, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                                                            print(AccessValues)

                                                                            check_stop_event(stop_event)
                                                                            Cardholder_Failsafe_GeneralError(driver)
                                                                            CardHolder_ClickOn_BadgeTab(driver)  # Click on Badge Tab
                                                                            time.sleep(gtime)

                                                                            # Add DOB from Skyline and NATA here

                                                                            # Switch to Quip, and write info to Quip Database
                                                                            SwithTo_Window(QuipWindow=True)

                                                                            Write_InfoTo_Quip(ProfileValues, BadgeValues=BadgeValues, AccessValues=AccessValues)
                                                                            Color_InfoTo_Quip(ProfileValues, BadgeValues=BadgeValues, AllInfo=True)

                                                                            current_time = datetime.datetime.now()
                                                                            print(f"Cardholder_Verification_Script: Trigger2 @ {current_time}")
                                                                            return True
                                                                        else:
                                                                            print(f"AccessValuesLoaded: {AccessValuesLoaded}")
                                                                            AccessValuesNonLoadCount = AccessValuesNonLoadCount + 1
                                                                            if AccessValuesNonLoadCount <= 3:
                                                                                print(f"AccessValuesNonLoadCount: {AccessValuesNonLoadCount}")
                                                                                SearchBarResultCount = 0
                                                                                BadgeValuesNonLoadCount = 0
                                                                                AccessValuesNonLoadCount = 0
                                                                                return False
                                                                            SwitchBack_FailsafeColoring()
                                                                            return True
                                                                    else:
                                                                        print(f"AccessContinueStatus: {AccessContinueStatus}")
                                                                        return False
                                                                else:
                                                                    check_stop_event(stop_event)
                                                                    Cardholder_Failsafe_GeneralError(driver)
                                                                    time.sleep(gtime)

                                                                    # Switch to Quip, and write info to Quip Database
                                                                    SwithTo_Window(QuipWindow=True)

                                                                    Write_InfoTo_Quip(ProfileValues, BadgeValues=BadgeValues)
                                                                    Color_InfoTo_Quip(ProfileValues, BadgeValues=BadgeValues, AllInfo=True)
                                                                    return True
                                                        else:
                                                            print("BadgeValues: ", BadgeValues)
                                                            return False    
                                                else:
                                                    print(f"BadgeValuesLoaded: {BadgeValuesLoaded}")
                                                    BadgeValuesNonLoadCount = BadgeValuesNonLoadCount + 1
                                                    if BadgeValuesNonLoadCount <= 3:
                                                        print(f"BadgeValuesNonLoadCount: {BadgeValuesNonLoadCount}")
                                                        SearchBarResultCount = 0
                                                        BadgeValuesNonLoadCount = 0
                                                        AccessValuesNonLoadCount = 0
                                                        return False
                                                    SwitchBack_FailsafeColoring()
                                                    return True
                                            else:
                                                print(f"BadgeContinueStatus: {BadgeContinueStatus}")
                                                return False
                                        else:
                                            if settings.get("AccessLvl_Tab_Info_Widget", False):
                                                CardHolder_ClickOn_AccessLvlTab(driver)  # Click on AccessLvl Tab
                                                check_stop_event(stop_event)
                                                Cardholder_Failsafe_GeneralError(driver)
                                                time.sleep(gtime)

                                                ContinueStatus, _ = CardHolder_WaitFor_Loading(driver, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                                                if ContinueStatus:
                                                    check_stop_event(stop_event)
                                                    Cardholder_Failsafe_GeneralError(driver)
                                                    AccessValues = CardHolder_GetInfo_AccessLvlInfo(driver, settings=settings, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)

                                                    check_stop_event(stop_event)
                                                    CardHolder_ClickOn_BadgeTab(driver)  # Click on Badge Tab
                                                    time.sleep(gtime)

                                                    # Add DOB from Skyline and NATA here

                                                    # Switch to Quip, and write info to Quip Database
                                                    SwithTo_Window(QuipWindow=True)

                                                    Write_InfoTo_Quip(ProfileValues, AccessValues=AccessValues)
                                                    Color_InfoTo_Quip(ProfileValues, Cardholder_Tab=True)
                                                    return True
                                                else:
                                                    print("ContinueStatus: ", ContinueStatus)
                                                    return False
                                            else:
                                                # Switch to Quip, and write info to Quip Database
                                                SwithTo_Window(QuipWindow=True)

                                                Write_InfoTo_Quip(ProfileValues)
                                                Color_InfoTo_Quip(ProfileValues, Cardholder_Tab=True)
                                                return True
                                    else:
                                        print("ProfileValues: ", ProfileValues)
                                        return False
                            else:
                                print(f"ContinueStatus2: {ContinueStatus2}")
                                return False
                        else:
                            print(f"SearchBarResult: {SearchBarResult}")
                            SearchBarResultCount = SearchBarResultCount + 1
                            if SearchBarResultCount <= 3:
                                print(f"SearchBarResultCount: {SearchBarResultCount}")
                                SearchBarResultCount = 0
                                BadgeValuesNonLoadCount = 0
                                AccessValuesNonLoadCount = 0
                                return False
                            SwitchBack_FailsafeColoring()
                            return True
                    else:
                        print(f"ContinueStatus1: {ContinueStatus1}")
                        return False
                # Bad EID
                SwitchBack_FailsafeColoring()
                return True
            else:
                print("stop all")
                return False

        elif not Quip_Database and Excel_Database:
            print("THe Exceldata feature does not exsist, Work in Progress")
            return False
    except (StopFunctionException, ElementClickInterceptedException, StaleElementReferenceException, CardHolder_General_Failsafe):
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
    global EID_ID
    try:
        for attempt in range(2):
            try:
                if EID_ID is None:
                    # Get the EID_ID if not already obtained
                    EID_ID = CardHolder_GetID_EID(driver, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)

                check_stop_event(stop_event)
                Cardholder_Failsafe_GeneralError(driver)
            
                input_element = driver.find_element(By.ID, EID_ID)
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
                EID_ID = None
                continue

    except (StopFunctionException, ElementClickInterceptedException, StaleElementReferenceException, CardHolder_General_Failsafe):
        return False

def CardHolder_Paste_Login(driver, StopFunctionException=None, check_stop_event=None, stop_event=None):
    global Login_ID
    try:
        for attempt in range(2):
            try:
                if Login_ID:
                    # Get the EID_ID if not already obtained
                    Login_ID = CardHolder_GetID_Login(driver, StopFunctionException=StopFunctionException, check_stop_event=check_stop_event, stop_event=stop_event)
                
                check_stop_event(stop_event)
                Cardholder_Failsafe_GeneralError(driver)

                input_element = driver.find_element(By.ID, Login_ID)
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
                Login_ID = None
                continue

    except (StopFunctionException, ElementClickInterceptedException, StaleElementReferenceException, CardHolder_General_Failsafe):
        return False

def Cardholder_Verify_ProfileLoaded(driver, StopFunctionException=None, check_stop_event=None, stop_event=None):
    try:
        current_time = datetime.datetime.now()
        print(f"Cardholder_Verify_ProfileLoaded: Trigger1 @ {current_time}")
        time.sleep(gtime)
        ParentElements = driver.find_elements(By.CSS_SELECTOR, 'div[class*="awsui_small_"]')

        # Iterate through the elements
        for element in ParentElements:
            check_stop_event(stop_event)
            Cardholder_Failsafe_GeneralError(driver)
            if "awsui_breakpoint" in element.get_attribute('class'): 
                check_stop_event(stop_event)
                Cardholder_Failsafe_GeneralError(driver)
                current_time = datetime.datetime.now()
                print(f"Cardholder_Verify_ProfileLoaded: Trigger2 @ {current_time}")
                return True, False  # Profile not loaded, return False

        # If the loop completes, meaning the profile loaded, return True
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
