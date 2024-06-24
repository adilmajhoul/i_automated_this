import re
import time
from turtle import goto
from playwright.sync_api import Playwright, sync_playwright, expect


def initialize(playwright):

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    return browser, context


def login(page, email="", password=""):

    page.goto("https://www.facebook.com/")
    time.sleep(2)

    page.get_by_test_id("royal_email").click()
    time.sleep(2)

    page.get_by_test_id("royal_email").fill(email)
    time.sleep(2)

    page.get_by_test_id("royal_pass").click()
    time.sleep(2)

    page.get_by_test_id("royal_pass").fill(password)
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


def get_last_posts(page, group_url, number_of_posts=3):
    page.goto(group_url)
    time.sleep(5)
    # posts = page.query_selector_all(
    #     "div.html-div > span.x4k7w5x.x1h91t0o > a.x 1i10hfl.xjbqb8w"
    # )
    # return [post.href for post in posts[:number_of_posts]]

    # Get all the selectors

    page.keyboard.press("End")
    time.sleep(10)

    selectors = page.query_selector_all(
        'span[class="x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1tu3fi x3x7a5m x1nxh6w3 x1sibtaa xo1l8bm xi81zsa x1yc453h"] > span[class="html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs"] > span:nth-child(4) > span[class="x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j"] > a'
    )
    print("selectors: ", selectors)

    links = []
    for selector in selectors:
        # Hover over the selector
        selector.hover()
        time.sleep(5)

        # Now, get the link
        link = selector.get_attribute("href")
        links.append(link)

    return links


def comment(page, post, comment):
    pass


def like(page, post):
    pass


def share(page, post):
    pass


def love_comment(page, post):
    pass


def add_friend(page, post):
    pass

    page.get_by_label("Like").nth(1).click()
    page.get_by_label("Send this to friends or post").click()
    page.get_by_role("button", name="Share to Feed").click()
    page.get_by_role("button", name="Share").click()
    page.get_by_label("Love", exact=True).click(position={"x": 17, "y": 26})
    page.get_by_label("Care").click(position={"x": 12, "y": 19})


# def post_comment_US(page, post, comment):

#     page.goto(post)
#     time.sleep(10)

#     page.get_by_role("paragraph").click()
#     time.sleep(3)

#     page.get_by_label("Write a public comment…").fill(comment)
#     time.sleep(3)

#     page.get_by_label("Comment", exact=True).click()
#     time.sleep(3)


def post_comment(page, post, comment):

    page.goto(post)
    time.sleep(10)

    page.get_by_label("Answer as Adil Ahmed").click()
    time.sleep(3)

    page.get_by_label("Answer as Adil Ahmed").fill(comment)
    time.sleep(3)

    # page.get_by_label("Comment", exact=True).click()
    page.keyboard.press("Enter")
    time.sleep(3)


# # -----------------------
# def generate_comment(post_content):
#     openai.api_key = "YOUR_OPENAI_API_KEY"
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=f"Generate a thoughtful comment for the following Facebook post:\n\n{post_content}",
#         max_tokens=50,
#     )
#     return response.choices[0].text.strip()


def main(playwright, email="", password=""):

    browser, context = initialize(playwright)

    page = context.new_page()

    login(page, email, password)
    time.sleep(10)

    # groups = get_groups(page)
    # print("groups: ", groups)

    # posts = get_last_posts(
    # page,
    # "https://www.facebook.com/groups/378731377493517/?sorting_setting=RECENT_ACTIVITY",
    # )
    # print("posts: ", posts)

    posts = ["https://www.facebook.com/groups/6128462463877370/posts/7964976430225955/"]

    for post in posts:
        post_comment(page, post, "si mhdi t9wdat 3lih hhhhhh")
        time.sleep(10)

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
    main(playwright, "0688109956", "facebookskhon")
