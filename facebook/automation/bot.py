import re
import time
from playwright.sync_api import Playwright, sync_playwright, expect


def initialize(playwright):

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    return browser, context


def login(page):

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

    time.sleep(10)

    # ---------------------


def get_last_posts(page, group_url, number_of_posts=1):
    page.goto(group_url)
    time.sleep(5)  # Wait for page to load
    posts = page.query_selector_all(
        "div.html-div > span.x4k7w5x.x1h91t0o > a.x1i10hfl.xjbqb8w"
    )
    return [post.href for post in posts[:number_of_posts]]


def get_groups(
    page,
    groups_url="https://www.facebook.com/groups/joins/?nav_source=tab",
    number_of_groups=3,
):
    page.goto(groups_url)
    time.sleep(5)  # Wait for page to load

    groups = page.query_selector_all('div.x8gbvx8.x78zum5 > div[role="listitem"]')
    return [group.href for group in groups[:number_of_groups]]


def main(playwright):

    browser, context = initialize(playwright)
    page = context.new_page()

    login(page)

    # get_groups(page,groups_url='https://www.facebook.com/groups/feed/')

    # get_last_posts(page,group_url,number_of_posts=5)

    {
        # comment on posts
        # like posts
        # share posts
        # add friends who comment on posts
        # like comments
        {
            # get the post context
            # feed it to ai api
            # post the comment
        }
    }

    context.close()
    browser.close()


with sync_playwright() as playwright:
    main(playwright)
