from curses import meta
import scrapy


class UsersSpider(scrapy.Spider):
    base_url = "https://theworldwatch.com"
    name = "usersspider"
    start_urls = [
        "https://theworldwatch.com/latest-updates/1/",
    ]

    # Custom settings for this spider
    custom_settings = {
        "DOWNLOAD_DELAY": 2,  # Delay of 2 seconds between requests
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,  # Limit concurrent requests per domain
        "DOWNLOAD_TIMEOUT": 15,  # Timeout for downloads (in seconds)
        "RETRY_TIMES": 3,  # Number of times to retry failed requests
        # "ITEM_PIPELINES": {
        #     "scrapy_theworldwatch.pipelines.UsersPipeline": 1,
        # },
    }

    def __init__(self, *args, **kwargs):
        super(UsersSpider, self).__init__(*args, **kwargs)
        self.last_video_url = self.read_last_video_url()
        print("__________self.last_video_url: ", self.last_video_url)
        self.last_video_reached = False
        self.current_page = 1
        self.first_video_url = None
        self.videos_scraped = 1

    def read_last_video_url(self):
        try:
            with open("last_video.txt", "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            return None

    def write_last_video_url(self, url):
        with open("last_video.txt", "w") as file:
            file.write(url)

    def get_video_users(self, response):
        video_url = response.meta["video_url"]

        for user in response.css(".username"):
            yield {
                "+++++++++++++username": user.css("::text").get(),
                "profile_link": user.attrib.get("href", "None"),
                "video_url": video_url,
            }

    def parse(self, response):
        print(f">>>>>>>>>>> PAGE {self.current_page} <<<<<<<<<<<<<")

        if self.videos_scraped == 0:
            self.first_video_url = response.css(".item > a").attrib["href"]
            print("______ self.first_video_url: ", self.first_video_url)

        for video in response.css(".item"):
            print(f">>>>>>>>>>> VIDEO {self.videos_scraped} <<<<<<<<<<<<<")

            video_url = video.css(".item > a").attrib["href"]

            # Check if the current video URL is the last video URL
            if video_url == self.last_video_url or (
                self.last_video_url is None and self.videos_scraped >= 8
            ):
                print("___________Last video reached!")

                if self.first_video_url:
                    self.write_last_video_url(self.first_video_url)

                self.last_video_reached = True
                return

            yield response.follow(
                video_url, self.get_video_users, meta={"video_url": video_url}
            )
            self.videos_scraped += 1
            # yield {
            #     "+++++++++++++ title": video.css(".title::text").get(),
            #     "poster": video.css(".video-uploader::text").get(),
            #     "views": video.css(".amount-views::text").get(),
            #     "comments": video.css(".tme::text").get(),
            #     "length": video.css(".drtn::text").get(),
            #     "link": video.css(".item > a").attrib["href"],
            # }

        if self.last_video_url is None and self.videos_scraped >= 8:
            if self.first_video_url:
                self.write_last_video_url(self.first_video_url)
            return

        next_page = response.css(".pagination-holder .next > a").attrib["href"]
        self.current_page += 1

        if next_page is not None and not self.last_video_reached:
            yield response.follow(next_page, self.parse)
        else:
            # Write the first video URL to the file if we are stopping
            if self.first_video_url:
                self.write_last_video_url(self.first_video_url)
