# python
# File: TA_1/login.py
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

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

def run_login(email_value, password_value, timeout=10, driver=None, driver_path=DRIVER_PATH):
    """
    Minimal login helper.
    Returns: bool (success)
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

        email = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        password = wait.until(EC.presence_of_element_located((By.NAME, "pass")))
        login_btn = wait.until(EC.element_to_be_clickable((By.NAME, "login")))

        email.clear()
        email.send_keys(email_value)
        password.clear()
        password.send_keys(password_value)

        before_url = driver.current_url
        login_btn.click()

        try:
            # wait for a URL change or the email field to disappear
            WebDriverWait(driver, timeout).until(
                EC.any_of(
                    EC.url_changes(before_url),
                    EC.invisibility_of_element_located((By.NAME, "email"))
                )
            )
            success = True
        except TimeoutException:
            success = False

    except (TimeoutException, WebDriverException):
        success = False
    finally:
        if driver:
            _save_screenshot(driver, "login", success)
        if local_driver:
            try:
                local_driver.quit()
            except Exception:
                pass

    return success