import scrapy


class TheworldwatchSpider(scrapy.Spider):
    base_url = "https://theworldwatch.com"
    name = "theworldwatch"
    start_urls = [
        "https://theworldwatch.com/latest-updates/1/",
    ]

    # Custom settings for this spider
    custom_settings = {
        "DOWNLOAD_DELAY": 2,  # Delay of 2 seconds between requests
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,  # Limit concurrent requests per domain
        "DOWNLOAD_TIMEOUT": 15,  # Timeout for downloads (in seconds)
        "RETRY_TIMES": 3,  # Number of times to retry failed requests
    }

    def parse(self, response):
        for video in response.css(".item"):
            video_data = {
                "text": video.css(".title::text").get(),
                "poster": video.css(".video-uploader::text").get(),
                "views": video.css(".amount-views::text").get(),
                "comments": video.css(".tme::text").get(),
                "length": video.css(".drtn::text").get(),
                "link": video.css(".item > a").attrib["href"],
            }
            video_url = video_data["link"]
            yield response.follow(
                video_url, self.parse_video, meta={"video_data": video_data}
            )

        next_sublink = response.css(".pagination-holder .next > a").attrib["href"]
        page = int(next_sublink.split("/")[-2])
        next_page = self.base_url + next_sublink

        if next_page is not None and page < 5:
            yield response.follow(next_page, self.parse)

    def parse_video(self, response):
        video_data = response.meta["video_data"]
        users = {}
        for user in response.css(".username"):
            username = user.css("::text").get()
            profile_link = user.attrib.get("href", "No link available")
            users[username] = profile_link

        video_data["users"] = users
        yield video_data


# # Importing necessary modules
# import scrapy


# # Define the Spider class
# class TheworldwatchSpider(scrapy.Spider):
#     base_url = "https://theworldwatch.com"

#     name = "theworldwatch"
#     start_urls = [
#         "https://theworldwatch.com/latest-updates/1/",
#     ]

#     def parse(self, response):
#         # Loop through all videos on each page
#         for video in response.css(".item"):
#             yield {
#                 "text": video.css(".title::text").get(),
#                 "poster": video.css(".video-uploader::text").get(),
#                 "views": video.css(".amount-views::text").get(),
#                 "comments": video.css(".tme::text").get(),
#                 "length": video.css(".drtn::text").get(),
#                 "link": video.css(".item > a").attrib["href"],
#             }

#         # Follow pagination link and repeat the process
#         next_sublink = response.css(".pagination-holder .next > a").attrib["href"]
#         page = int(next_sublink.split("/")[-2])
#         next_page = self.base_url + next_sublink

#         if next_page is not None and page < 5:
#             print("page -->", page)
#             yield response.follow(next_page, self.parse)
