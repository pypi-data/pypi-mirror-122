from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as ec
import json
import re
import sys
from time import sleep

options = webdriver.ChromeOptions()
options.add_argument("--headless")


class YoutubeLinks:
    """
    This class is used to scrape links for youtube videos and save them in a json file

    class attributes:
        channel (str): this holds the value of the youtube channel video links will be scrapped from
        height (int): this specifies how far to scroll down the youtube page to grab links.
        driver_path (str): the path to Chrome Driver on system.
        driver (str): contains the specified Chrome Driver path
    """

    def __init__(self, channel: str, height: int, driver_path: str):
        self.links = []
        self.channel = channel
        self.height = height
        self.driver_path = driver_path
        self.driver = webdriver.Chrome(executable_path=driver_path, options=options)

    @staticmethod
    def _is_channel_valid(x):
        x = x.lower()
        x = x.replace(' ', '')
        return x

    @property
    def channel(self):
        return self.__channel

    @channel.setter
    def channel(self, channel):
        if re.fullmatch('[a-zA-Z\s]+', channel):
            self.__channel = self._is_channel_valid(channel)
        else:
            sys.stderr.write('Not a valid channel')
            raise ValueError('Not a valid channel')

    def accept_cookies(self) -> None:
        try:
            cookies = self.driver.find_element_by_xpath(
                '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div[1]/div/button/span')
            cookies.click()
        except:
            pass

    def page_scroll(self) -> None:
        while True:
            scroll_height = 200
            document_height_before = self.driver.execute_script("return document.documentElement.scrollHeight")
            self.driver.execute_script(f"window.scrollTo(0, {document_height_before + scroll_height});")
            sleep(3)
            document_height_after = self.driver.execute_script("return document.documentElement.scrollHeight")
            if document_height_after > self.height:
                break

    def extract_links(self):
        """
        This function performs the links scrapping using the methods above
        """
        url = f'https://www.youtube.com/c/{self.channel}/videos'
        self.driver.get(url)
        self.accept_cookies()
        sleep(2)
        self.page_scroll()
        videos_list = Wait(self.driver, 30).until(
            ec.presence_of_all_elements_located((By.XPATH, "//*[@id='video-title']")))
        self.links = []
        for item in videos_list:
            self.links.append(item.get_attribute('href'))
        print(f' I found {len(self.links)} videos')
        self.write_to_json()
        self.driver.close()
        return self.links

    def write_to_json(self):
        with open('./links.json', 'w') as f:
            json.dump(self.links, f, indent=2)


if __name__ == '__main__':
    ls = YoutubeLinks('imaginetunez', 4000, r'C:\Users\Victor\Downloads\chromedriver_win32\chromedriver')
    ls.extract_links()
