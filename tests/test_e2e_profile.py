from playwright.sync_api import sync_playwright

BASE_URL = "http://fastapi_app:8000"

def register_and_login(page, email, password):
    # Register
    page.goto(f"{BASE_URL}/register")
    page.fill("#email", email)
    page.fill("#password", password)
    page.fill("#confirm-password", password)
    page.click("#register-btn")
    page.wait_for_timeout(400)

    # Login
    page.goto(f"{BASE_URL}/login")
    page.fill("#email", email)
    page.fill("#password", password)
    page.click("#login-btn")

    page.wait_for_function("() => localStorage.getItem('jwt') !== null")

def test_profile_password_change_and_relogin():
    email = "e2e_profile_unique@example.com"
    old_password = "password123"
    new_password = "newpass123"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        register_and_login(page, email, old_password)

        # Go to profile page
        page.goto(f"{BASE_URL}/profile-ui")

        # Ensure inputs exist
        page.wait_for_selector("#current-password")
        page.wait_for_selector("#new-password")
        page.wait_for_selector("#change-password-btn")

        # Change password
        page.fill("#current-password", old_password)
        page.fill("#new-password", new_password)
        page.click("#change-password-btn")

        # Verify UI message
        page.wait_for_function("() => document.querySelector('#password-message')?.textContent.includes('Password updated')")

        # Now re-login with new password 
        page.evaluate("() => localStorage.removeItem('jwt')")
        page.goto(f"{BASE_URL}/login")
        page.fill("#email", email)
        page.fill("#password", new_password)
        page.click("#login-btn")
        page.wait_for_function("() => localStorage.getItem('jwt') !== null")

        browser.close()
