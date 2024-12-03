import time, pyautogui, pyperclip, json, os, sys

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from Resources.Utilities.Utilities_File import StopFunctionException, check_stop_event
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException
# ------------------------------------------- #

gtime = 0.25

# Setup code to get the IDs
EID_ID = None
First_Name_ID = None
Last_Name_ID = None
Login_ID = None
SearchButton_Element = None

class CardHolder_General_Failsafe(Exception):
    pass

def Cardholder_Failsafe_GeneralError(driver):
    Element_List = driver.find_elements(By.CSS_SELECTOR, "[class*='awsui_large']")

    for Element in Element_List:
        class_name = Element.get_attribute('class')
        if 'awsui_breakpoint' in class_name:
                time.sleep(gtime)
                raise CardHolder_General_Failsafe

# ---------------------------------------- #

def CardHolder_GetID_First_Last_Name(driver, stop_event=None):
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

def CardHolder_GetID_EID(driver, stop_event=None):
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

def CardHolder_GetID_Login(driver, stop_event=None):
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

def CardHolder_GetElement_SearchButton(driver, stop_event=None):
    global SearchButton_Element
    try:
        check_stop_event(stop_event)
        Cardholder_Failsafe_GeneralError(driver)
        if SearchButton_Element is None:
            Button_Elements = driver.find_elements(By.CSS_SELECTOR, "[class*='awsui_button_vjswe']")
            SearchButton_Element = Button_Elements[1]

        check_stop_event(stop_event)
        Cardholder_Failsafe_GeneralError(driver)
        return SearchButton_Element
    except (StopFunctionException, ElementClickInterceptedException, StaleElementReferenceException, CardHolder_General_Failsafe):
        return False

def CardHolder_Paste_EID(driver, stop_event=None):
    try:
        for attempt in range(2):
            # Get the EID_ID if not already obtained
            ReturnID = CardHolder_GetID_EID(driver, stop_event=stop_event)
            check_stop_event(stop_event)
            Cardholder_Failsafe_GeneralError(driver)
            time.sleep(gtime)
            try:
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

def CardHolder_Paste_Login(driver, stop_event=None):
    try:
        for attempt in range(2):
            try:
                # Get the EID_ID if not already obtained
                ReturnID = CardHolder_GetID_Login(driver, stop_event=stop_event)
                check_stop_event(stop_event)
                Cardholder_Failsafe_GeneralError(driver)
                time.sleep(gtime)

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

def CardHolder_FailSafe_LoadProfile(driver, stop_event=None):
    try:
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
                return True, True  # Found the desired text, return True

        # If the loop completes without finding the desired text, return False
        check_stop_event(stop_event)
        Cardholder_Failsafe_GeneralError(driver)
        return True, False
    except (StopFunctionException, ElementClickInterceptedException, StaleElementReferenceException, CardHolder_General_Failsafe):
        return False, False

# ----------------------------------------------------------------------------------- #

def CardHolder_WaitFor_Loading(driver, MainProfile=False, Element=None, settings=None, stop_event=None):
    try:
        Status1, LoadingComplete = False, False

        for attempt in range(30):
            check_stop_event(stop_event)
            Cardholder_Failsafe_GeneralError(driver)
            if MainProfile:
                class_name = Element.get_attribute('class')
                
                if 'awsui_disabled_vjswe' in class_name:
                    time.sleep(1)  # Short delay between attempts
                else:
                    Status1, LoadingComplete = True, True
                    time.sleep(0.25)
                    break  # Exit the loop if the element is not found
            else:
                try:
                    driver.find_element(By.CSS_SELECTOR, "[class*='awsui_icon_1cbgc']")
                    time.sleep(1)
                except NoSuchElementException:
                    Status1, LoadingComplete = True, True
                    time.sleep(0.25)
                    break  # Exit the loop if the element is not found

        # Final status if the loop completes without break
        if not (Status1 and LoadingComplete):
            Status1, LoadingComplete = True, False

        if Status1:
            if LoadingComplete:
                if MainProfile:
                    SearchBy_EID, SearchBy_Login, _ = settings.get("SearchBy_Column_Widget", [True, False, "A"])
                    for attempt in range(3):
                        check_stop_event(stop_event)
                        Cardholder_Failsafe_GeneralError(driver)
                        time.sleep(gtime)
                        Status2, Result = CardHolder_FailSafe_LoadProfile(driver, stop_event=stop_event)
                        if Status2:
                            if Result:
                                check_stop_event(stop_event)
                                Cardholder_Failsafe_GeneralError(driver)
                                print(f"Bad EID attempt {attempt}")
                                pyautogui.press('esc')
                                time.sleep(gtime)
                                if SearchBy_EID:
                                    CardHolder_Paste_EID(driver, stop_event=stop_event)
                                elif SearchBy_Login:
                                    CardHolder_Paste_Login(driver, stop_event=stop_event)
                                else:
                                    print("Invalid Paste method, Failsafe Measure Ending Script")
                                    return False, False

                                time.sleep(gtime)
                                check_stop_event(stop_event)
                                Cardholder_Failsafe_GeneralError(driver)
                            else:
                                time.sleep(2)
                                return True, True
                        else:
                            print("stop all")
                            return False, False
                    return True, False
                else:
                    return True, True
            else:
                print("CardHolder_WaitFor_Loading_LoadingComplete: ", LoadingComplete)
                return False, False
        else:
            print("CardHolder_WaitFor_Loading_Status1: ", Status1)
            return False, False
    except (StopFunctionException, ElementClickInterceptedException, CardHolder_General_Failsafe) as E:
        # StaleElementReferenceException
        print(E)
        return False, False

def CardHolder_ClickOn_BadgeTab(driver):
    for attempt in range(5):
        elements = driver.find_elements(By.CSS_SELECTOR, 'span[class*="awsui_tabs-tab-label_14rmt"]')
        for element in elements:
            if element.text == "Badge":
                element.click()
                return  # Break the loop after clicking the text "Badge"
        time.sleep(gtime)

def CardHolder_ClickOn_CardholderTab(driver):
    for attempt in range(5):
        elements = driver.find_elements(By.CSS_SELECTOR, 'span[class*="awsui_tabs-tab-label_14rmt"]')
        for element in elements:
            if element.text == "Cardholder":
                element.click()
                return  # Break the loop after clicking the text "Cardholder"
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

def CardHolder_GetInfo_ProfileInfo(driver, stop_event=None):
    try:
        check_stop_event(stop_event)
        Cardholder_Failsafe_GeneralError(driver)
        # Find all input elements with the specified class names
        input_elements = driver.find_elements(By.CSS_SELECTOR, 'input[class*="awsui_input_"]')
        values = []

        check_stop_event(stop_event)
        Cardholder_Failsafe_GeneralError(driver)

        # Iterate over the input elements from index 6 to 17
        for i in range(6, 18):
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
        return values
    except (StopFunctionException, ElementClickInterceptedException, StaleElementReferenceException, IndexError, CardHolder_General_Failsafe):
        return False

def CardHolder_GetInfo_BadgeInfo(driver, stop_event=None):
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

def CardHolder_GetInfo_AccessLvlInfo(driver, settings, stop_event=None):
    try:
        check_stop_event(stop_event)

        Class_Selector = (
            '.awsui_input_ '
            '.awsui_input-type-search '
            '.awsui_input-has-icon-left'
        )

        # Find the input element with the specified class name
        input_element = driver.find_element(By.CSS_SELECTOR, 'input[class*="awsui_input-type-search"]')
        input_element.click()

        Home_Site = settings.get("Home_Site", "KAFW")
        Home_Site_Access = f"{Home_Site}-1-GENERAL ACCESS"
        pyperclip.copy(Home_Site_Access)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)

        Values = []

        try:
            time.sleep(3)
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