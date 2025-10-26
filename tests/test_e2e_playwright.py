import pytest
from playwright.sync_api import sync_playwright

@pytest.mark.skip(reason="Skipping E2E test in CI (requires running FastAPI server)")
def test_homepage_loads():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://127.0.0.1:8000/docs")
        assert "Swagger UI" in page.title()
        browser.close()
