import csv


class UsersPipeline(object):

    def __init__(self):
        self.csvwriter = None

    def open_spider(self, spider):
        self.csvfile = open("users.csv", "w", newline="")
        self.csvwriter = csv.DictWriter(
            self.csvfile, fieldnames=["username", "profile_link"]
        )
        self.csvwriter.writeheader()

    def close_spider(self, spider):
        self.csvfile.close()

    def process_item(self, item, spider):
        if item["profile_link"] != "None":  # Skip items with None link
            self.csvwriter.writerow(item)
            self.csvfile.flush()  # Flush the buffer

        return item
