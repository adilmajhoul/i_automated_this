import pyautogui as pg
from time import sleep
import cv2
import numpy as np

import argparse


# You may also need the webbrowser library to open Chrome tabs initially
import webbrowser


class Bot:
    def __init__(self):

        self.adress_bar = (334, 97)

        self.snaptik_url_field = (592, 425)
        self.snaptik_first_download = (991, 422)
        self.snaptik_second_download = (1101, 233)
        self.snaptik_home_logo = (147, 141)

        self.browser_path = "/usr/bin/google-chrome-stable"

        self.snaptik_url = "https://snaptik.app/en1"

        self.bsuit = {
            "reel_upload_link": "https://business.facebook.com/latest/reels_composer",
            "add_video_button": (155, 440),
            "next_button": (1295, 708),
        }

    def switch_to_tab(self, tab_number):
        pg.hotkey("alt", str(tab_number))

    def wait_for_image(self, image_path, timeout=1.5):

        while True:
            image = self.locate_image_opencv(image_path)

            if image:
                print(f"FOUND {image_path}!")
                return image

            print(f"Waiting for {image_path} ...")
            sleep(timeout)

    def locate_image_opencv(self, image_path):
        screenshot = pg.screenshot()

        # Convert Screenshot to BGR
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Load the Template Image
        template = cv2.imread(image_path)

        # Perform Template Matching:
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)

        # Locate the Best Match
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        threshold = 0.99
        if max_val >= threshold:
            return max_loc
        return None

    def goto_site(self, url):
        pg.click(self.adress_bar)
        sleep(1.5)
        pg.hotkey("ctrl", "a")
        sleep(1.5)
        pg.typewrite(url)
        sleep(1.5)
        pg.hotkey("enter")

    def click_image(self, image_path):
        image = self.wait_for_image(image_path)
        pg.click(image)

    def run(self, tiktok_videos=[]):

        pg.click(1032, 53)

        # open empty chrome tab
        # os.system("xdg-open https://google.com")
        webbrowser.open("https://google.com")

        # sleep(10)
        image = self.wait_for_image("images/google_logo.png")

        pg.hotkey("ctrl", "t")
        sleep(1.5)

        # switch to 3rd tab and go to snaptik
        self.switch_to_tab(2)
        sleep(1.5)

        self.goto_site(self.snaptik_url)

        image = self.wait_for_image("images/snaptik_logo.png")

        for url in tiktok_videos:
            pg.click(self.snaptik_url_field)
            sleep(1.5)

            pg.typewrite(url)
            sleep(1.5)

            pg.click(self.snaptik_first_download)
            sleep(2)

            pg.click(self.snaptik_second_download)
            sleep(1.5)

            pg.click(self.snaptik_home_logo)
            sleep(1.5)


def main():
    parser = argparse.ArgumentParser(description="Automate TikTok and Instagram tasks using PyAutoGUI.")

    parser.add_argument("--urls", type=str, nargs="+", required=True, help="A list of URLs.")

    args = parser.parse_args()

    videos = [
        "https://www.tiktok.com/@topbanat/video/7225186705127607558",
        "https://www.tiktok.com/@topbanat/video/7224816030290431259",
        "https://www.tiktok.com/@topbanat/video/7180113065533328646",
        "https://www.tiktok.com/@topbanat/video/7170064269105515782",
        "https://www.tiktok.com/@topbanat/video/7128913256722353413",
        "https://www.tiktok.com/@topbanat/video/7128911419336084741",
        "https://www.tiktok.com/@topbanat/video/7128761683803131141",
        "https://www.tiktok.com/@topbanat/video/7128538273126845702",
        "https://www.tiktok.com/@topbanat/video/7128524457735359749",
        "https://www.tiktok.com/@topbanat/video/7079473736193248517",
        "https://www.tiktok.com/@topbanat/video/7079499964493155590",
        "https://www.tiktok.com/@topbanat/video/7102497703673842949",
        "https://www.tiktok.com/@topbanat/video/7047278719857184001",
        "https://www.tiktok.com/@topbanat/video/7073128613809343745",
        "https://www.tiktok.com/@topbanat/video/6948872782616857857",
        "https://www.tiktok.com/@topbanat/video/6948119460297428226",
        "https://www.tiktok.com/@buuuz.tiktok/video/7184160347287194886",
        "https://www.tiktok.com/@buuuz.tiktok/video/7183014621123546374",
        "https://www.tiktok.com/@lfroj_2.0/video/7361190127399341317",
        "https://www.tiktok.com/@lfroj_2.0/video/7327051907946630406",
        "https://www.tiktok.com/@lfroj_2.0/video/7327052049802169605",
        "https://www.tiktok.com/@lfroj_2.0/video/7288459442608164101",
        "https://www.tiktok.com/@lfroj_2.0/video/7285130523138116870",
        "https://www.tiktok.com/@lfroj_2.0/video/7285129709829197062",
        "https://www.tiktok.com/@lfroj_2.0/video/7282912507235241221",
        "https://www.tiktok.com/@lfroj_2.0/video/7275872744267468037",
        "https://www.tiktok.com/@lfroj_2.0/video/7274398898662149382",
    ]
    bot = Bot()
    bot.run(videos)


if __name__ == "__main__":
    main()
