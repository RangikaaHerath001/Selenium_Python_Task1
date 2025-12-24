# python
# File: tests/test_login.py
import os
import glob
import pytest
import allure
from TA_1.login import run_login

def _attach_latest(prefix: str) -> None:
    pattern = os.path.join(os.getcwd(), "screenshots", f"{prefix}_*.png")
    files = glob.glob(pattern)
    if not files:
        return
    latest = max(files, key=os.path.getmtime)
    allure.attach.file(latest, name=os.path.basename(latest), attachment_type=allure.attachment_type.PNG)

def test_login_valid():
    ok = run_login("bob.alice069@gmail.com", "Secret@123", timeout=15)
    _attach_latest("login")
    assert ok

def test_login_invalid():
    ok = run_login("invalid.user@example.com", "wrongpassword", timeout=15)
    _attach_latest("login")
    assert not ok