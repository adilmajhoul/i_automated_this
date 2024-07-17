import pyautogui as pg
from time import sleep
import os
import cv2
import numpy as np

# import os

# You may also need the webbrowser library to open Chrome tabs initially
import webbrowser


class Download_IG:
    def __init__(self):
        self.adress_bar = (1648, 61)


        

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

    def download_publer(self,reel_urls=[]):

        self.goto_site('https://snapsave.app/')
        
        for url in reel_urls:        
            # click url field
            pg.click(1928,451)
            # write url
            pg.typewrite(url)
            # click enter
            pg.hotkey('enter')
            # click download video
            pg.click(1607,837)
            # click close ad
            # click download more



    def run(self, tiktok_videos=[]):

        pg.click(1032, 53)

        # open empty chrome tab
        # os.system("xdg-open https://google.com")
        webbrowser.open("https://google.com")

        # sleep(10)
        image = self.wait_for_image("images/google_logo.png")

        # click chrome to focus
        # pg.click(1032, 53)

        # open two more tabs
        # for _ in range(2):

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

        # get videos names
        videos = [video for video in os.listdir("/home/x/0-videos_to_upload") if video.endswith(".mp4")]
        sleep(1.5)

        print("videos: ", videos)  # videos:  ['video3.mp4', 'video1.mp4', 'video2.mp4']

        # open new tab
        pg.hotkey("ctrl", "t")
        sleep(1.5)

        for video in videos:

            # goto bsuit site
            self.goto_site(self.bsuit["reel_upload_link"])
            sleep(1.5)

            # wait page to load
            self.wait_for_image("images/bsuit/add_video_button.png")
            sleep(1.5)

            # click add video
            pg.click(self.bsuit["add_video_button"])

            # -------------
            # folder navigation part

            sleep(7)

            # click home
            pg.click(86, 136)
            sleep(2)

            # click enter
            pg.hotkey("enter")
            sleep(2)

            # ctrl + f to search needed video
            pg.hotkey("ctrl", "f")
            sleep(2)

            pg.typewrite(video)
            sleep(1.5)

            # click enter
            pg.hotkey("enter")
            sleep(1.5)
            # -------------

            # wait for load 100%
            self.wait_for_image("images/bsuit/upload_progress_100%.png")
            sleep(1.5)

            # click next
            pg.click(self.bsuit["next_button"])
            sleep(2)

            # click next
            pg.click(self.bsuit["next_button"])
            sleep(2)

            # click share
            pg.click(self.bsuit["next_button"])
            sleep(2)

            # wait for reel published image
            self.wait_for_image("images/bsuit/reel_published.png")
            sleep(1.5)

  