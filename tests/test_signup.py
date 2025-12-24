# python
# File: tests/test_signup.py
import os
import glob
import pytest
import allure
from TA_1.signup import run_signup

def _attach_latest(prefix: str) -> None:
    pattern = os.path.join(os.getcwd(), "screenshots", f"{prefix}_*.png")
    files = glob.glob(pattern)
    if not files:
        return
    latest = max(files, key=os.path.getmtime)
    allure.attach.file(latest, name=os.path.basename(latest), attachment_type=allure.attachment_type.PNG)

def test_signup_success():
    data_pass = {
        "firstname": "Alice",
        "lastname": "Bob",
        "email": "bob.alice069@gmail.com",
        "password": "Secret@123",
        "day": "10",
        "month": "Jan",
        "year": "1990",
        "gender_value": "1"
    }
    ok, _msg = run_signup(data_pass, timeout=20)
    _attach_latest("signup")
    assert ok

def test_signup_failure():
    data_fail = {
        "firstname": "Bad",
        "lastname": "User",
        "email": "bad@example.com",
        "password": "Secret@123",
        "day": "1",
        "month": "Jan",
        "year": "1990",
        "gender_value": "1"
    }
    ok, _msg = run_signup(data_fail, timeout=20)
    _attach_latest("signup")
    assert not ok