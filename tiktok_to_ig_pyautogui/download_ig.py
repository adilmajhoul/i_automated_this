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
        self.adress_bar = (1679, 64)


        

    def switch_to_tab(self, tab_number):
        pg.hotkey("alt", str(tab_number))





    def wait_for_image(self, image_path, timeout=2):

        while True:
            image = self.locate_image_opencv(image_path)

            if image:
                print(f"FOUND {image_path}!")
                return image

            print(f"Waiting for {image_path} ...")
            sleep(timeout)

    def locate_image_opencv(self, image_path):
        screenshot = pg.screenshot(allScreens=True)

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

    def download_snapinsta(self,reel_urls=[]):

        self.goto_site('https://snapinsta.app/')
        
        self.wait_for_image('images/download_ig_reels/snapinsta_logo.png')

        for url in reel_urls:        
            # click url field
            pg.click(1885,349)
            sleep(1.5)
            # write url
            pg.typewrite(url)
            sleep(1.5)
            # click enter
            pg.hotkey('enter')
            sleep(2)

            self.wait_for_image('images/download_ig_reels/download_button_snapinsta.png')

            # click download video
            pg.click(1618,519)
            sleep(1.5)

            # click close ad
            pg.click(1991,666)
            sleep(1.5)

            # click download more
            pg.click(2010,633)
            sleep(2)





    def run(self, tiktok_videos=[]):

        pg.click(self.adress_bar)

        # open empty chrome tab
        # os.system("xdg-open https://google.com")
        webbrowser.open("https://google.com")

        image = self.wait_for_image("images/google_logo.png")

        # click chrome to focus
        # pg.click(1032, 53)

        # open two more tabs
        # for _ in range(2):

        pg.hotkey("ctrl", "t")
        sleep(1.5)

        # switch to 2nd tab and go to snaptik
        self.switch_to_tab(2)
        sleep(1.5)

        self.download_snapinsta(tiktok_videos)



def main():

    # add ig videos here 
    videos =[]

    bot = Download_IG()
    bot.run(videos)

if __name__ == "__main__":
    main()

     