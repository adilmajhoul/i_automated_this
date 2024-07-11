import pyautogui as pg
from time import sleep

# import os

# You may also need the webbrowser library to open Chrome tabs initially
# import webbrowser

from sqlalchemy import table


class Bot:
    def __init__(self):

        self.adress_bar = (187, 96)

        self.snaptik_url_field = (460, 464)
        self.snaptik_first_download = (972, 453)
        self.snaptik_second_download = (1079, 266)
        self.snaptik_home_logo = (142, 177)

    def switch_to_tab(self, tab_number):
        pg.hotkey("ctrl", str(tab_number))
        sleep(1.5)

    # def wait_for_download(download_folder, timeout=300):
    #     start_time = time.time()
    #     while time.time() - start_time < timeout:
    #         if any(file.endswith(".mp4") for file in os.listdir(download_folder)):
    #             return True
    #         sleep(5)
    #     return False

    def wait_for_image(self, image_path, timeout=5):

        while True:
            image = pg.locateCenterOnScreen(image_path)

            if image:
                return image

            sleep(timeout)

    def run(self, tiktok_videos=[]):

        # run chrome

        # open three tabs tiktok,meta suite, and snaptik

        # click chrome to focus
        pg.click(1032, 53)

        self.switch_to_tab(3)
        sleep(1.5)

        for url in tiktok_videos:

            # self.switch_to_tab(1.5)
            # sleep(1.5)

            # pg.click(self.adress_bar)
            # sleep(1.5)

            # # write url to adress bar
            # pg.typewrite(url)
            # sleep(1.5)

            # pg.hotkey("enter")
            # sleep(1.5)

            # pg.hotkey("ctrl", "a")
            # sleep(1.5)

            # pg.hotkey("ctrl", "c")
            # sleep(1.5)

            # self.switch_to_tab(3)
            # sleep(1.5)

            pg.click(self.snaptik_url_field)
            sleep(1.5)

            # pg.hotkey("ctrl", "v")
            # sleep(1.5)

            pg.typewrite(url)
            sleep(1.5)

            pg.click(self.snaptik_first_download)
            sleep(1.5)

            pg.click(self.snaptik_second_download)
            sleep(1.5)

            pg.click(self.snaptik_home_logo)
            sleep(1.5)

            # switch to meta business suite tab

            # click upload reel

            # choose video

            # image = self.wait_for_image("images/reel_upload_100%.png")

            # click next
            # schedual or upload
