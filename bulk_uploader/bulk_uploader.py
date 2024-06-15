from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

with sync_playwright() as p:
    for browser_type in [p.chromium, p.firefox, p.webkit]:
        browser = browser_type.launch()
        page = browser.new_page()
        stealth_sync(page)
        page.goto('http://whatsmyuseragent.org/')
        page.screenshot(path=f'example-{browser_type.name}.png')
        
        page.wait_for_timeout(15000)  # Wait for 60 seconds
        
        browser.close()

# import re
# from playwright.sync_api import Playwright, sync_playwright, expect

# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
#     context = browser.new_context()
#     page = context.new_page()
#     page.locator("body").click()

#     # Go to Instagram login page
#     page.goto("https://www.instagram.com/accounts/login/")
#     page.wait_for_load_state('load')  # Wait for the login page to fully load

#     # Enter login credentials
#     page.get_by_label("Phone number, username, or email").click()
#     page.get_by_label("Phone number, username, or email").fill("adilmajhoul")
#     page.get_by_label("Password").click()
#     page.get_by_label("Password").fill("instagramskhon1-")
    
#     # Click login button and wait for the main page to load
#     page.get_by_role("button", name="Log in", exact=True).click()
#     page.wait_for_load_state('load')  # Wait for the main page to fully load

#     # Navigate to the reels upload page and wait for it to load
#     page.goto("https://www.instagram.com/reels/upload/")
#     page.wait_for_load_state('load')  # Wait for the reels upload page to fully load

#     # Click the "Select from computer" button and upload the video
#     page.get_by_role("button", name="Select from computer").click()
#     page.get_by_role("button", name="Select from computer").set_input_files("I JUST Found Out About This Python Trick! #python #coding #programming.mp4")

#     # Wait for a while to ensure the video upload completes (this is a rough approximation; ideally, check for some confirmation)
#     page.wait_for_timeout(60000)  # Wait for 60 seconds

#     # Close context and browser
#     context.close()
#     browser.close()

# with sync_playwright() as playwright:
#     run(playwright)
