import re
import time
from playwright.sync_api import Playwright, sync_playwright, expect

import csv

users = [
    {
        "username": "Superb Nipple Man",
        "video_title": " You could Never Predict How this Guy is About to Die..(Slow Motion Added) ",
        "profile_link": "https://theworldwatch.com/members/1324276/",
        "video_url": "https://theworldwatch.com/videos/1619618/you-could-never-predict-how-this-guy-is-about-to-die-slow-motion-added/",
    },
    {
        "username": "LordTorquemada",
        "video_title": " You could Never Predict How this Guy is About to Die..(Slow Motion Added) ",
        "profile_link": "https://theworldwatch.com/members/1318226/",
        "video_url": "https://theworldwatch.com/videos/1619618/you-could-never-predict-how-this-guy-is-about-to-die-slow-motion-added/",
    },
]


def load_users():
    with open("users.csv", "r") as file:
        reader = csv.DictReader(file)

        return list(reader)


def login(page):

    page.goto("https://theworldwatch.com/")
    page.locator("#login").click()
    time.sleep(2)

    page.get_by_placeholder("please enter login here").click()
    time.sleep(2)

    page.get_by_placeholder("please enter login here").fill("__user__")
    time.sleep(2)

    page.get_by_label("Password").click()
    time.sleep(2)

    page.get_by_label("Password").fill("__password__")
    time.sleep(2)

    page.get_by_text("remember me").click()
    time.sleep(2)

    page.get_by_role("button", name="Log in").click()
    time.sleep(2)

    # ---------------------

    time.sleep(2)


def message(page, user):
    page.goto(user["profile_link"])

    page.get_by_role("link", name="Send Message...").click()
    time.sleep(2)

    page.locator("#send_message_message").nth(1).click()
    time.sleep(2)

    page.locator("#send_message_message").nth(1).fill(f"hi {user['username']} how are you bro ? ")
    time.sleep(2)

    page.get_by_role("img", name=":heart:").click()
    time.sleep(2)

    page.get_by_role("button", name="Send").click()
    time.sleep(5)


def run(playwright):
    users = load_users()

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    login(page)

    for user in users:
        message(page, user)
        time.sleep(5)

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
