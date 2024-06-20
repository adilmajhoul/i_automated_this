import pandas as pd
import csv


class UsersPipeline(object):

    def __init__(self):
        self.csvwriter = None

    def open_spider(self, spider):
        self.csvfile = open("users.csv", "w", newline="")
        self.csvwriter = csv.DictWriter(
            self.csvfile,
            fieldnames=["username", "video_title", "profile_link", "video_url"],
        )
        self.csvwriter.writeheader()

    def close_spider(self, spider):
        self.csvfile.close()

        # Read the CSV file
        df = pd.read_csv("users.csv")

        # Drop duplicates based on the 'username' column
        df = df.drop_duplicates(subset="username")

        # Write the filtered data back to the CSV file
        df.to_csv("users.csv", index=False)

    def process_item(self, item, spider):
        if item["profile_link"] != "None":  # Skip items with None link
            self.csvwriter.writerow(item)
            self.csvfile.flush()  # Flush the buffer

        return item
