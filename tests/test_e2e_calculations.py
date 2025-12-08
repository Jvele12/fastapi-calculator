import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "http://fastapi_app:8000"


def login_and_get_page(p, email="bread_user@example.com", password="password123"):
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(f"{BASE_URL}/register")
    page.fill("#email", email)
    page.fill("#password", password)
    page.fill("#confirm-password", password)
    page.click("#register-btn")

    page.wait_for_function(
        "document.querySelector('#message') && "
        "document.querySelector('#message').textContent.trim().length > 0"
    )

    page.goto(f"{BASE_URL}/login")
    page.fill("#email", email)
    page.fill("#password", password)
    page.click("#login-btn")

    page.wait_for_function(
        "document.querySelector('#message') && "
        "document.querySelector('#message').textContent.toLowerCase().includes('login successful')"
    )

    return browser, page


def test_bread_calculations_positive():
    with sync_playwright() as p:
        browser, page = login_and_get_page(p)

        page.goto(f"{BASE_URL}/calculations-ui")

        # --- Add ---
        page.fill("#calc-a", "10")
        page.fill("#calc-b", "5")
        page.select_option("#calc-type", "divide")
        page.click("#add-calc-btn")

        page.wait_for_selector(".calc-row")
        text = page.text_content(".calc-row")
        assert "10" in text and "5" in text and "divide" in text

        # --- Edit ---
        page.click(".edit-btn")
        page.fill("#calc-a", "12")
        page.click("#save-edit-btn")

        page.wait_for_timeout(500)  # small wait
        text = page.text_content(".calc-row")
        assert "12" in text

        # --- Delete ---
        page.click(".delete-btn")
        page.wait_for_timeout(500)
        assert page.query_selector(".calc-row") is None

        browser.close()


def test_bread_calculations_negative_divide_by_zero():
    with sync_playwright() as p:
        browser, page = login_and_get_page(
            p, email="bread_negative@example.com", password="password123"
        )

        page.goto(f"{BASE_URL}/calculations-ui")

        page.fill("#calc-a", "1")
        page.fill("#calc-b", "0")
        page.select_option("#calc-type", "divide")
        page.click("#add-calc-btn")

        page.wait_for_function(
            "document.querySelector('#error') && "
            "document.querySelector('#error').textContent.toLowerCase().includes('zero')"
        )
        msg = page.text_content("#error").lower()
        assert "zero" in msg

        browser.close()
