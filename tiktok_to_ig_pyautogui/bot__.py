import pyautogui as pg
from time import sleep
import time
import os
import webbrowser
import cv2
from SimpleCV import Image as SimpleCVImage

# import pytesseract
# from PIL import Image
# from skimage import io, color, feature
# import dlib
import numpy as np

# from SimpleCV import Image as SimpleCVImage, Template


class Bot:
    def __init__(self):
        self.adress_bar = (187, 96)
        self.snaptik_url_field = (592, 425)
        self.snaptik_first_download = (991, 422)
        self.snaptik_second_download = (1101, 233)
        self.snaptik_home_logo = (147, 141)
        self.browser_path = "/usr/bin/google-chrome-stable"
        self.snaptik_url = "https://snaptik.app/en1"
        self.bsuit_reel_upload_link = "https://business.facebook.com/latest/reels_composer"

    def switch_to_tab(self, tab_number):
        pg.hotkey("alt", str(tab_number))

    def wait_for_image(self, image_path, timeout=2, method="opencv"):
        start_time = time.time()

        while True:
            if method == "opencv":
                image = self.locate_image_opencv(image_path)
            # elif method == 'tesseract':
            #     image = self.locate_image_tesseract(image_path)
            # elif method == 'pillow':
            #     image = self.locate_image_pillow(image_path)
            # elif method == 'scikit_image':
            #     image = self.locate_image_scikit(image_path)
            # elif method == 'dlib':
            #     image = self.locate_image_dlib(image_path)
            # elif method == 'simplecv':
            #     image = self.locate_image_simplecv(image_path)
            # else:
            #     raise ValueError("Invalid method specified.")

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

        threshold = 0.8
        if max_val >= threshold:
            return max_loc
        return None

    def locate_image_simplecv(self, image_path):
        screenshot = pg.screenshot()

        screenshot_np = np.array(screenshot)

        screen = SimpleCVImage(screenshot_np)

        template = SimpleCVImage(image_path)

        match = screen.findTemplate(template, threshold=0.8)

        print("simple cv match: ", match)

        if match:
            return match[0].x, match[0].y
        return None

    def goto_site(self, url):
        pg.click(self.adress_bar)
        sleep(1.5)
        pg.hotkey("ctrl", "a")
        sleep(1.5)
        pg.typewrite(url)
        sleep(1.5)
        pg.hotkey("enter")

    def click_image(self, image_path, method="opencv"):
        image = self.wait_for_image(image_path, method=method)
        if image:
            pg.click(image)

    def run(self, tiktok_videos=[]):
        pg.click(1032, 53)
        webbrowser.open("https://google.com")
        image = self.wait_for_image("images/google_logo.png", method="opencv")
        pg.hotkey("ctrl", "t")
        sleep(1.5)
        self.switch_to_tab(2)
        sleep(1.5)
        self.goto_site(self.snaptik_url)
        image = self.wait_for_image("images/snaptik_logo.png", timeout=2, method="opencv")

        for url in tiktok_videos:
            pg.click(self.snaptik_url_field)
            sleep(1.5)

        videos = [video for video in os.listdir("/home/x/0-videos_to_upload") if video.endswith(".mp4")]
        sleep(1.5)
        print("videos: ", videos)

        for _ in range(len(videos)):
            pg.hotkey("ctrl", "t")
            sleep(1.5)
            self.goto_site(self.bsuit_reel_upload_link)
            sleep(1.5)

        current_bsuit_tab = 3
        for index, video in enumerate(videos):
            self.switch_to_tab(current_bsuit_tab)
            sleep(1.5)
            if index == 0:
                self.wait_for_image("images/bsuit/create_reel.png", method="opencv")
            pg.click(151, 438)
            sleep(6)
            pg.click(86, 136)
            sleep(1.5)
            pg.hotkey("enter")
            sleep(1.5)
            pg.hotkey("ctrl", "f")
            sleep(1.5)
            pg.typewrite(video)
            sleep(1.5)
            pg.hotkey("enter")
            sleep(1.5)
            current_bsuit_tab += 1

        current_bsuit_tab = 3
        for _ in range(len(videos)):
            self.switch_to_tab(current_bsuit_tab)
            sleep(1.5)
            self.wait_for_image("images/bsuit/upload_progress_100%.png", method="opencv")
            sleep(1.5)
            self.click_image("images/bsuit/next_button.png", method="opencv")
            sleep(2)
            self.click_image("images/bsuit/next_button.png", method="opencv")
            sleep(2)
            self.click_image("images/bsuit/share_button.png", method="opencv")
            sleep(2)
            self.wait_for_image("images/bsuit/reel_published.png", method="opencv")
            sleep(1.5)
            current_bsuit_tab += 1


# Initialize and run the bot
bot = Bot()
bot.run(["https://www.tiktok.com/@example1/video/1234567890", "https://www.tiktok.com/@example2/video/0987654321"])
