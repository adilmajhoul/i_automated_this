import pyautogui as pg
from time import sleep
import os

# import os

# You may also need the webbrowser library to open Chrome tabs initially
import webbrowser


class Bot:
    def __init__(self):

        self.adress_bar = (187, 96)

        self.snaptik_url_field = (592, 425)
        self.snaptik_first_download = (991, 422)
        self.snaptik_second_download = (1101, 233)
        self.snaptik_home_logo = (147, 141)

        self.browser_path = "/usr/bin/google-chrome-stable"

        self.snaptik_url = "https://snaptik.app/en1"

        self.reel_upload_link = "https://business.facebook.com/latest/reels_composer"

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
            try:
                image = pg.locateCenterOnScreen(image_path)
            except:
                image = None

            if image:
                print(f"FOUND {image_path} !")
                return image

            print(f"Waiting for {image_path} ...")

            sleep(timeout)

    def run(self, tiktok_videos=[]):

        pg.click(1032, 53)

        # run chrome
        # open empty chrome tab
        # os.system("xdg-open https://google.com")
        webbrowser.open("https://google.com")

        # sleep(10)
        image = self.wait_for_image("images/google_logo.png")

        # click chrome to focus
        # pg.click(1032, 53)

        # open two more tabs
        for _ in range(2):
            pg.hotkey("ctrl", "t")
            sleep(1.5)

        # switch to 3rd tab and go to snaptik
        self.switch_to_tab(3)
        sleep(1.5)
        pg.click(self.adress_bar)
        sleep(1.5)
        pg.hotkey("ctrl", "a")
        sleep(1.5)
        pg.typewrite(self.snaptik_url)
        sleep(1.5)
        pg.hotkey("enter")

        image = self.wait_for_image("images/snaptik_logo.png", timeout=2)

        for url in tiktok_videos:

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

        # get videos names
        videos = [video for video in os.listdir("videos_to_upload/") if video.endswith(".mp4")]

        print("videos: ", videos)  # videos:  ['video3.mp4', 'video1.mp4', 'video2.mp4']

        for _ in range(len(videos)):
            pg.hotkey("ctrl", "t")
            sleep(1.5)

            # TODO: coonvert this to fnuction called goto_site(self,url)
            pg.click(self.adress_bar)
            sleep(1.5)
            pg.hotkey("ctrl", "a")
            sleep(1.5)
            pg.typewrite(self.reel_upload_link)
            sleep(1.5)
            pg.hotkey("enter")
