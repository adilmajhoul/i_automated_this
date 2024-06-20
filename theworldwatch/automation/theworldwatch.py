import re
import time
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://theworldwatch.com/")
    page.locator("#login").click()
    page.get_by_placeholder("please enter login here").click()
    page.get_by_placeholder("please enter login here").click()
    page.get_by_placeholder("please enter login here").fill("narax38053")
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill("theworldwatch9lawi1-")
    page.get_by_text("remember me").click()
    page.get_by_role("button", name="Log in").click()

    # ---------------------

    time.sleep(20)

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
