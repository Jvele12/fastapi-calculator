from playwright.sync_api import sync_playwright

BASE_URL = "http://fastapi_app:8000"


def _wait_for_message(page):
    # Wait until #message has non-empty text
    page.wait_for_function(
        """
        () => {
            const el = document.querySelector('#message');
            if (!el) return false;
            const txt = el.textContent.trim();
            return txt.length > 0;
        }
        """,
        timeout=30000,
    )
    msg = page.text_content("#message") or ""
    return msg.strip()


def test_register_success():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(f"{BASE_URL}/register")

        page.fill("#email", "e2e_user@example.com")
        page.fill("#password", "password123")
        page.fill("#confirm-password", "password123")

        # Either of these is fine, but keep ONE:
        # page.click("text=Register")
        page.click("#register-btn")

        msg = _wait_for_message(page)
        assert "successful" in msg.lower()

        browser.close()


def test_register_short_password():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(f"{BASE_URL}/register")

        page.fill("#email", "shortpass@example.com")
        page.fill("#password", "123")
        page.fill("#confirm-password", "123")

        page.click("#register-btn")

        msg = _wait_for_message(page)
        assert "password must be at least" in msg.lower()

        browser.close()


def test_login_success():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # First register the user (in case DB is empty)
        page.goto(f"{BASE_URL}/register")
        page.fill("#email", "e2e_user@example.com")
        page.fill("#password", "password123")
        page.fill("#confirm-password", "password123")
        page.click("#register-btn")
        _ = _wait_for_message(page)  # ignore content

        # Now go to login
        page.goto(f"{BASE_URL}/login")

        page.fill("#email", "e2e_user@example.com")
        page.fill("#password", "password123")

        page.click("#login-btn")

        msg = _wait_for_message(page)
        assert "login successful" in msg.lower()

        browser.close()


def test_login_wrong_password():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Ensure user exists
        page.goto(f"{BASE_URL}/register")
        page.fill("#email", "e2e_user@example.com")
        page.fill("#password", "password123")
        page.fill("#confirm-password", "password123")
        page.click("#register-btn")
        _ = _wait_for_message(page)

        # Wrong password
        page.goto(f"{BASE_URL}/login")

        page.fill("#email", "e2e_user@example.com")
        page.fill("#password", "wrongpass")

        page.click("#login-btn")

        msg = _wait_for_message(page)
        assert "invalid" in msg.lower()

        browser.close()
