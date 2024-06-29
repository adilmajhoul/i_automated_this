import json
from enum import Enum
import random
import time
from playwright.sync_api import sync_playwright
from multiprocessing import Process


class Reaction(Enum):
    LIKE = "Like"
    LOVE = "Love"
    CARE = "Care"
    HAHA = "Haha"
    WOW = "Wow"
    SAD = "Sad"
    ANGRY = "Angry"


class FacebookBot:
    def __init__(self, config):
        self.email = config["email"]
        self.password = config["password"]
        self.number_of_accounts_to_add = config["number_of_accounts_to_add"]
        self.number_of_posts_to_scrape = config["number_of_posts_to_scrape"]

    def initialize(self, playwright):
        self.browser = playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page.set_default_timeout(60000)

    def login(self):
        self.page.goto("https://www.facebook.com/")
        time.sleep(2)
        self.page.get_by_test_id("royal_email").click()
        self.page.get_by_test_id("royal_email").fill(self.email)
        self.page.get_by_test_id("royal_pass").click()
        self.page.get_by_test_id("royal_pass").fill(self.password)
        self.page.get_by_test_id("royal_login_button").click()
        time.sleep(5)

    def get_groups(
        self,
        groups_url="https://www.facebook.com/groups/joins/?nav_source=tab",
        number_of_groups=3,
    ):
        self.page.goto(groups_url)
        time.sleep(5)
        groups = self.page.query_selector_all(
            "div:nth-child(2) > div.x8gbvx8.x78zum5.x1q0g3np.x1a02dak.x1nhvcw1.x1rdy4ex.xcud41i.x4vbgl9.x139jcc6 > div > div > div.x6s0dn4.x78zum5.x1q0g3np.x1qughib > div.x1cy8zhl.x78zum5.xdt5ytf.x1iyjqo2.x1a02dak.x1sy10c2.x1pi30zi > div > div > span > span > div > a"
        )
        return [group.get_attribute("href") for group in groups[:number_of_groups]]

    def get_last_posts(self, group_url, number_of_posts=3):
        self.page.goto(group_url)
        time.sleep(5)
        self.page.keyboard.press("End")
        time.sleep(10)
        selectors = self.page.query_selector_all(
            'span[class="x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1tu3fi x3x7a5m x1nxh6w3 x1sibtaa xo1l8bm xi81zsa x1yc453h"] > span[class="html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs"] > span:nth-child(4) > span[class="x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j"] > a'
        )
        links = [selector.get_attribute("href") for selector in selectors]
        return links[:number_of_posts]

    def comment(self, post, comment, skip_navigation=False, additional_actions=[]):

        if not skip_navigation:
            self.page.goto(post)
            time.sleep(10)

        self.page.get_by_label("Leave a comment").click()
        self.page.get_by_role("paragraph").fill(comment)
        self.page.keyboard.press("Enter")
        time.sleep(3)

        for action in additional_actions:
            if isinstance(action, tuple):
                func, *args = action
                func(self.page, post, skip_navigation=True, *args)
                time.sleep(5)
            else:
                action(self.page, post, skip_navigation=True)
                time.sleep(5)

    def react(self, post, reaction: Reaction, skip_navigation=False):
        if not skip_navigation:
            self.page.goto(post)
            time.sleep(10)
        self.page.get_by_label("Like", exact=True).first.hover()
        time.sleep(5)
        self.page.get_by_label(reaction.value, exact=True).first.click(position={"x": 17, "y": 21})
        time.sleep(3)

    def share(self, post, skip_navigation=False):
        if not skip_navigation:
            self.page.goto(post)
            time.sleep(10)
        self.page.get_by_label("Send this to friends or post").click()
        time.sleep(3)
        self.page.get_by_label("Share now").click()
        time.sleep(3)

    def add_friends_who_commented(self, post, skip_navigation=False, number_of_accounts=random.randint(5, 10)):
        if not skip_navigation:
            self.page.goto(post)
            time.sleep(10)

        # how many times to scrol
        if number_of_accounts <= 5:
            scroll_times = number_of_accounts
        elif number_of_accounts <= 15:
            scroll_times = number_of_accounts / 2
        else:
            scroll_times = number_of_accounts / 3

        for i in range(int(scroll_times)):
            print(f"scrolled {i + 1} times")
            self.page.mouse.wheel(0, 1000)
            time.sleep(10)

        accounts = self.page.query_selector_all(
            "div.xv55zj0.x1vvkbs.x1rg5ohu.xxymvpz > div > div > span > span > a"
        )
        for account in accounts[:number_of_accounts]:
            account.hover()
            time.sleep(5)
            if self.page.get_by_label("Add friend").is_visible():
                self.page.get_by_label("Add friend").click()
                time.sleep(5)

                if self.page.get_by_text("Can't send request").is_visible():
                    self.page.get_by_label("OK", exact=True).click()

    def add_accounts_who_shared(self, post, skip_navigation=False, number_of_accounts=10):
        if not skip_navigation:
            self.page.goto(post)
            time.sleep(10)
        self.page.get_by_role("button", name="shares").click()
        time.sleep(5)

        # how many times to scrol
        if number_of_accounts <= 5:
            scroll_times = number_of_accounts
        elif number_of_accounts <= 15:
            scroll_times = number_of_accounts / 2
        else:
            scroll_times = number_of_accounts / 3

        for i in range(int(scroll_times)):
            print(f"scrolled {i + 1} times")
            self.page.mouse.wheel(0, 200)
            time.sleep(10)

        accounts = self.page.query_selector_all("div.xu06os2.x1ok221b > span > h3 > span > a > strong > span")
        for account in accounts[:number_of_accounts]:
            account.hover()
            time.sleep(5)
            if self.page.get_by_label("Add friend").is_visible():
                self.page.get_by_label("Add friend").click()
                time.sleep(5)
                if self.page.get_by_text("Can't send request").is_visible():
                    self.page.get_by_label("OK", exact=True).click()

        self.page.get_by_label("Close").click()

    def run(self):
        with sync_playwright() as playwright:
            self.initialize(playwright)
            self.login()
            posts = [
                "https://www.facebook.com/groups/207220915184146/posts/387147647191471",
                "https://www.facebook.com/groups/python.developers.group/posts/390021837383874/"
                "https://www.facebook.com/groups/207220915184146/posts/386865363886366/",
            ]
            for index, post in enumerate(posts):
                # match index:
                #     case 0:
                #         self.comment(
                #             post,
                #             "not all of them about coding",
                #             additional_actions=[
                #                 (self.react, Reaction.LOVE),
                #                 self.share,
                #             ],
                #         )
                #         self.add_friends_who_commented(post, number_of_accounts=self.number_of_accounts_to_add)
                #         self.add_accounts_who_shared(post, number_of_accounts=self.number_of_accounts_to_add)
                #     case _:
                #         pass

                self.react(post, Reaction.LOVE)

                self.add_friends_who_commented(
                    post, number_of_accounts=self.number_of_accounts_to_add, skip_navigation=True
                )
                self.add_accounts_who_shared(
                    post, number_of_accounts=self.number_of_accounts_to_add, skip_navigation=True
                )

                self.share(post, skip_navigation=True)

            time.sleep(120)
            self.context.close()
            self.browser.close()


def run_bot(config):
    bot = FacebookBot(config)
    bot.run()


if __name__ == "__main__":
    with open("config.json", "r") as file:
        configs = json.load(file)["bots"]

    for config in configs:
        run_bot(config)
