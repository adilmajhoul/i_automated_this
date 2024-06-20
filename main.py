from requests_html import HTMLSession

# if last_video is empty run this seeder


def last_video_seeder(videos_back=7):
    session = HTMLSession()
    parser = session.get("https://theworldwatch.com/latest-updates/1/")

    return parser.html.find(".item > a")[videos_back].attrs["href"]


print(last_video_seeder(8))
