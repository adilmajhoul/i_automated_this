import pyautogui as pg
from time import sleep


class Indeed_Apply_Bot:
    def __init__(self, jobs_amount):

        self.adress_bar = (181, 96)

        self.choose_resume = (383, 489)
        self.continue_button = (594, 546)

        self.jobs_amount = jobs_amount

    def switch_to_tab(self, tab_number):
        pg.hotkey("alt", str(tab_number))

    def run(self):

        pg.click(self.adress_bar)
        sleep(1.5)

        current_tab = 1
        for _ in range(self.jobs_amount):

            pg.click(self.choose_resume)
            sleep(1.5)

            while True:
                pg.hotkey("end")
                sleep(1.5)

                pg.click(self.continue_button)
                sleep(2)

                # for _ in range(2):
                try:
                    image = pg.locateOnScreen("images/application_submitted.png")
                except:
                    image = None

                if image:
                    print(f"application submitted!")

                    current_tab += 1

                    self.switch_to_tab(current_tab)
                    sleep(1.5)

                    break
