import csv
from time import sleep
import pandas as pd
from selenium import webdriver
from .links_scapper import YoutubeLinks
from .video import Video

options = webdriver.ChromeOptions()
options.add_argument("--headless")


class VideoData(Video):
    """
    This class will iterate through the links stored in the
    json files created from the LinkScrapper class. It also inherits attributes
    functions from both of the Video and LinkScrapper class.

    Attributes:
        channel (str): this holds the value of the youtube channel video links will be scrapped from
        height (int): this specifies how far to scroll down the youtube page to grab links.
        driver_path (str): the path to Chrome Driver on system.
        driver (str): contains the specified Chrome Driver path
    """

    def __init__(self, channel: str, height: int, driver_path: str):
        self.driver = webdriver.Chrome(executable_path=driver_path, options=options)
        self.links = YoutubeLinks(channel, height, driver_path)
        self.channel = channel
        self.height = height
        self.yt_data = []

    def write_data_to_csv(self):
        df = pd.DataFrame.from_dict(self.yt_data, orient='columns')

        csv_file = open(
            './youtube_data.csv', 'w', encoding="UTF-8", newline="")
        writer = csv.writer(csv_file)
        writer.writerow(['title', 'description', 'hash_tags', 'views', 'comments'])
        df.to_csv('./youtube_data.csv')
        csv_file.close()

    def get_yt_data(self):
        """
        This function takes the json files containing links scrapped from the LinkScrapper,
        iterates over each link in the file, grabs the information described in the Video class
        and and stores them into a csv file.
        """
        count = 0
        for i, link in enumerate(self.links.extract_links()):
            print(f'I am collecting information for video {i} ')

            self.driver.get(link)
            data = {"title": [], "description": [], "loc_tags": [], "views": [], "comments": []}

            title = self.get_video_title()
            data['title'].append(title)

            desc = self.get_video_description()
            data['description'].append(desc)

            tags = self.get_hash_tag()
            data['loc_tags'].append(tags)

            views = self.get_no_views()
            data['views'].append(views)

            comm = self.get_video_comments()
            data['comments'].append([my_elem.text for my_elem in comm])

            self.yt_data.append(data)
            count += 1
            sleep(3)

        self.write_data_to_csv()
        self.driver.close()


if __name__ == '__main__':
    ls = VideoData('SkyNews', 4000, r'C:\Users\Victor\Downloads\chromedriver_win32\chromedriver')
    ls.get_yt_data()
