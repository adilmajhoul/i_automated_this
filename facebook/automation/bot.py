import re
import time
from turtle import goto
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

    page.get_by_test_id("royal_email").fill("oliagems@proton.me")
    time.sleep(2)

    page.get_by_test_id("royal_pass").click()
    time.sleep(2)

    page.get_by_test_id("royal_pass").fill("facebookskhon1-")
    time.sleep(2)

    page.get_by_test_id("royal_login_button").click()
    time.sleep(2)

    # ---------------------


def get_groups(
    page,
    groups_url="https://www.facebook.com/groups/joins/?nav_source=tab",
    number_of_groups=3,
):
    page.goto(groups_url)
    time.sleep(5)

    groups = page.query_selector_all(
        "div:nth-child(2) > div.x8gbvx8.x78zum5.x1q0g3np.x1a02dak.x1nhvcw1.x1rdy4ex.xcud41i.x4vbgl9.x139jcc6 > div > div > div.x6s0dn4.x78zum5.x1q0g3np.x1qughib > div.x1cy8zhl.x78zum5.xdt5ytf.x1iyjqo2.x1a02dak.x1sy10c2.x1pi30zi > div > div > span > span > div > a"
    )

    return [group.get_attribute("href") for group in groups[:number_of_groups]]


# def get_last_posts(page, group_url, number_of_posts=1):
#     page.goto(group_url)
#     time.sleep(5)  # Wait for page to load
#     posts = page.query_selector_all(
#         "div.html-div > span.x4k7w5x.x1h91t0o > a.x1i10hfl.xjbqb8w"
#     )
#     return [post.href for post in posts[:number_of_posts]]


# # -----------------------
# def generate_comment(post_content):
#     openai.api_key = "YOUR_OPENAI_API_KEY"
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=f"Generate a thoughtful comment for the following Facebook post:\n\n{post_content}",
#         max_tokens=50,
#     )
#     return response.choices[0].text.strip()


# def post_comment(page, post, comment):

#     page.goto(post)

#     post_content = page.query_selector("div[aria-label='Write a comment']").text_content

#     generate_comment(post_content)

#     post.click()  # Click to expand the post
#     time.sleep(2)
#     page.fill("div[aria-label='Write a comment']", comment)
#     page.press("div[aria-label='Write a comment']", "Enter")
#     time.sleep(2)  # Wait for comment to post


def main(playwright, email="", password=""):

    browser, context = initialize(playwright)

    page = context.new_page()

    login(page)
    time.sleep(10)

    groups = get_groups(page)
    print("groups: ", groups)

    time.sleep(120)

    # for group in groups:
    #     posts = get_last_posts(page, group)
    #     time.sleep(10)

    #     for post in posts:

    #         post_comment(page, post, "hello")
    #         time.sleep(10)

    # get_groups(page,groups_url='https://www.facebook.com/groups/feed/')

    # get_last_posts(page,group_url,number_of_posts=5)

    # {
    # comment on posts
    # like posts
    # share posts
    # add friends who comment on posts
    # like comments
    # {
    # get the post context
    # feed it to ai api
    # post the comment
    # }
    # }

    context.close()
    browser.close()


with sync_playwright() as playwright:
    main(playwright)
