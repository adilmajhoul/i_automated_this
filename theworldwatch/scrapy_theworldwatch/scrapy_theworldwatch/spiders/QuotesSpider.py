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
setup db pip

        # Follow pagination link and repeat the process
        next_sublink = response.css(".pagination-holder .next > a").attrib["href"]
        page = int(next_sublink.split("/")[-2])
        next_page = self.base_url + next_sublink

        if next_page is not None and page < 5:
            print("page -->", page)
            yield response.follow(next_page, self.parse)
