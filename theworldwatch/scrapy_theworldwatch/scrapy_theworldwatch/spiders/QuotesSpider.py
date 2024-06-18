# Importing necessary modules
import scrapy


# Define the Spider class
class TheworldwatchSpider(scrapy.Spider):
    base_url = "https://theworldwatch.com"

    name = "theworldwatch"
    start_urls = [
        "https://theworldwatch.com/latest-updates/1/",
    ]

    def parse(self, response):
        # Loop through all videos on each page
        for video in response.css(".item"):
            yield {
                "text": video.css(".title::text").get(),
                "poster": video.css(".video-uploader::text").get(),
                "views": video.css(".amount-views::text").get(),
                "comments": video.css(".tme::text").get(),
                "length": video.css(".drtn::text").get(),
                "link": video.css(".item > a").attrib["href"],
            }

        # Follow pagination link and repeat the process
        next_sublink = response.css(".pagination-holder .next > a").attrib["href"]
        page = int(next_sublink.split("/")[-2])
        next_page = self.base_url + next_sublink

        if next_page is not None and page < 5:
            print("page -->", page)
            yield response.follow(next_page, self.parse)
