# python
# File: TA_1/signup.py
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

DRIVER_PATH = r'D:\browserdrivers\chromedriver.exe'

def _save_screenshot(driver, prefix, success):
    try:
        screenshots_dir = os.path.join(os.getcwd(), "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        status = "success" if success else "failure"
        filename = f"{prefix}_{status}_{ts}.png"
        path = os.path.join(screenshots_dir, filename)
        driver.save_screenshot(path)
    except Exception:
        pass

def run_signup(data, timeout=15, driver=None, driver_path=DRIVER_PATH):
    """
    Minimal signup helper.
    Returns: (success: bool, message: str)
    If `driver` is provided it will not be quit by this function.
    """
    local_driver = None
    if driver is None:
        s = Service(driver_path)
        local_driver = webdriver.Chrome(service=s)
        driver = local_driver

    success = False
    try:
        driver.maximize_window()
        driver.get("https://www.facebook.com/")
        wait = WebDriverWait(driver, timeout)

        # try a few common ways to open the registration form
        tried = False
        for locator in [
            (By.CSS_SELECTOR, "a[data-testid='open-registration-form-button']"),
            (By.XPATH, "//*[text()='Create New Account']"),
            (By.XPATH, "//a[contains(., 'Create New Account')]")
        ]:
            try:
                btn = wait.until(EC.element_to_be_clickable(locator))
                btn.click()
                tried = True
                break
            except TimeoutException:
                continue
        if not tried:
            raise NoSuchElementException("Create account button not found")

        wait.until(EC.visibility_of_element_located((By.NAME, "firstname")))
        driver.find_element(By.NAME, "firstname").send_keys(data.get("firstname", ""))
        driver.find_element(By.NAME, "lastname").send_keys(data.get("lastname", ""))
        driver.find_element(By.NAME, "reg_email__").send_keys(data.get("email", ""))
        # optional confirmation field
        try:
            driver.find_element(By.NAME, "reg_email_confirmation__").send_keys(data.get("email", ""))
        except Exception:
            pass
        if data.get("password"):
            driver.find_element(By.ID, "password_step_input").send_keys(data.get("password", ""))

        Select(wait.until(EC.presence_of_element_located((By.ID, "day")))).select_by_visible_text(data.get("day", "1"))
        Select(wait.until(EC.presence_of_element_located((By.ID, "month")))).select_by_visible_text(data.get("month", "Jan"))
        Select(wait.until(EC.presence_of_element_located((By.ID, "year")))).select_by_visible_text(data.get("year", "1990"))

        # try to pick gender
        try:
            gender = wait.until(EC.element_to_be_clickable((By.XPATH, f"//input[@name='sex' and @value='{data.get('gender_value','1')}']")))
            gender.click()
        except Exception:
            try:
                g = driver.find_elements(By.XPATH, "//input[@name='sex']")
                if g:
                    g[0].click()
            except Exception:
                pass

        submit = wait.until(EC.element_to_be_clickable((By.NAME, "websubmit")))
        submit.click()

        try:
            # wait for either the form to hide or a confirmation indicator
            cond1 = EC.invisibility_of_element_located((By.NAME, "firstname"))
            cond2 = EC.presence_of_element_located((By.XPATH, "//*[contains(., 'Enter the code') or contains(., 'confirmation')]"))
            WebDriverWait(driver, 8).until(EC.any_of(cond1, cond2))
            success = True
        except TimeoutException:
            # inspect URL for common confirmation tokens
            current_url = driver.current_url.lower()
            if any(tok in current_url for tok in ("confirm", "checkpoint", "verify", "confirm_code")):
                success = True
            else:
                success = False

    except Exception:
        success = False
    finally:
        if driver:
            _save_screenshot(driver, "signup", success)
        if local_driver:
            try:
                local_driver.quit()
            except Exception:
                pass

    return success, ("TEST PASSED" if success else "TEST FAILED")