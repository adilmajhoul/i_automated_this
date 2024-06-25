from enum import Enum
import time
from playwright.sync_api import sync_playwright


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


# def comment_US(page, post, comment):

#     page.goto(post)
#     time.sleep(10)

#     page.get_by_role("paragraph").click()
#     time.sleep(3)

#     page.get_by_label("Write a public comment…").fill(comment)
#     time.sleep(3)

#     page.get_by_label("Comment", exact=True).click()
#     time.sleep(3)


# def like(page, post):
#     page.goto(post)
#     time.sleep(10)

#     page.get_by_label("Like").first.click()
#     time.sleep(3)


# def love(page, post):
#     page.goto(post)
#     time.sleep(10)

#     page.get_by_label("Like").first.hover()
#     time.sleep(5)

#     page.get_by_label("Love").click(position={"x": 17, "y": 21})
#     time.sleep(3)


# def care(page, post):
#     page.goto(post)
#     time.sleep(10)

#     page.get_by_label("Like").first.hover()
#     time.sleep(5)

#     page.get_by_label("Care").click(position={"x": 17, "y": 19})
#     time.sleep(3)


# def haha(page, post):
#     page.goto(post)
#     time.sleep(10)

#     page.get_by_label("Like").first.hover()
#     time.sleep(5)

#     page.get_by_label("Haha", exact=True).click(position={"x": 16, "y": 21})
#     time.sleep(3)


def comment(page, post, comment, additional_actions=[]):
    # Navigate to the post page only if it wasn't loaded before
    page.goto(post)
    time.sleep(10)

    page.get_by_label("Leave a comment").click()
    time.sleep(5)

    page.get_by_role("paragraph").fill(comment)
    time.sleep(3)

    page.keyboard.press("Enter")
    time.sleep(3)

    for action in additional_actions:
        if isinstance(action, tuple):
            func, *args = action
            func(page, post, skip_navigation=True, *args)
            time.sleep(5)

        else:
            action(page, post, skip_navigation=True)
            time.sleep(5)


class Reaction(Enum):
    LIKE = "Like"
    LOVE = "Love"
    CARE = "Care"
    HAHA = "Haha"
    WOW = "Wow"
    SAD = "Sad"
    ANGRY = "Angry"


def react(page, post, reaction: Reaction, skip_navigation=False):
    if not skip_navigation:
        page.goto(post)
        time.sleep(10)

    page.get_by_label("Like").first.hover()
    time.sleep(5)

    page.get_by_label(reaction.value).click(position={"x": 17, "y": 21})
    time.sleep(3)


def share(page, post, skip_navigation=False):
    if not skip_navigation:
        page.goto(post)
        time.sleep(10)

    page.get_by_label("Send this to friends or post").click()
    time.sleep(3)

    page.get_by_label("Share now").click()
    time.sleep(3)


def main(playwright, email="", password=""):

    # page.get_by_label("Wow").click(position={"x":16,"y":22})
    # page.get_by_label("Sad").click(position={"x":19,"y":20})
    # page.get_by_label("Angry").click(position={"x":17,"y":21})
    # page.get_by_label("Leave a comment").click()
    # page.get_by_label("Comment as Adil Ahmed").fill("wtf hhhhh")

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

    posts = ["https://www.facebook.com/groups/412570174716840/posts/487007983939725/"]

    for index, post in enumerate(posts):

        match index:
            case 0:
                comment(
                    page,
                    post,
                    "so true",
                    additional_actions=[(react, Reaction.LIKE), share],
                )

                # get users from post
                # send friend requests

                time.sleep(100)

            # case 2:
            # react(page, post, Reaction.HAHA)
            # comment share
            # time.sleep(10)
            # case 3:
            # react(page, post, Reaction.HAHA)
            # comment
            # share
            # add 5 friends from post
            # time.sleep(10)

            case _:
                pass

    time.sleep(120)

    # for group in groups:
    #     posts = get_last_posts(page, group)
    #     time.sleep(10)

    #     for post in posts:

    #         comment(page, post, "hello")
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
