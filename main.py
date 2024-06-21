import re
import time
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.facebook.com/")
    time.sleep(2)

    page.get_by_test_id("royal_email").click()
    time.sleep(2)

    page.get_by_test_id("royal_email").fill("0688109956")
    time.sleep(2)

    page.get_by_test_id("royal_pass").click()
    time.sleep(2)

    page.get_by_test_id("royal_pass").fill("facebookskhon")
    time.sleep(2)

    page.get_by_test_id("royal_login_button").click()
    time.sleep(2)

    time.sleep(120)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
