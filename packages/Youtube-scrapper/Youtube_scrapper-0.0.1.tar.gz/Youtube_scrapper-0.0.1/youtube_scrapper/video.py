from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from time import sleep


class Video:
    """
    This class is used to provide the video information that will be scrapped by
    Scrapper.

    class attributes:
        driver (str): contains the specified Chrome Driver path

    """

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=driver_path, options=options)

    def get_video_title(self):
        try:
            v_title = Wait(self.driver, 5).until(
                ec.presence_of_element_located((By.XPATH, '//*[@id="container"]/h1/yt-formatted-string'))).text
        except:
            v_title = ""
        return v_title

    def get_video_description(self):
        try:
            v_description = Wait(self.driver, 5).until(ec.presence_of_element_located(
                (By.CSS_SELECTOR, "#description > yt-formatted-string > span:nth-child(1)"))).text.split('\n')
        except:
            v_description = ""
        return v_description

    def get_hash_tag(self):
        try:
            v_hash_tags = Wait(self.driver, 5).until(
                ec.presence_of_element_located((By.XPATH, '//*[@id="container"]/yt-formatted-string/a'))).text
        except:
            v_hash_tags = ""
        return v_hash_tags

    def get_no_views(self):
        try:
            v_views = self.driver.find_element_by_xpath(
                '//span[@class="view-count style-scope ytd-video-view-count-renderer"]').text
        except:
            v_views = ""
        return v_views

    def get_video_comments(self):
        """
        This function is used to grab video comments
        """
        sleep(2)
        self.driver.execute_script('window.scrollTo(0,100);')
        sleep(2)
        for i in range(0, 4):
            self.driver.execute_script(
                "window.scrollTo(0,Math.max(document.documentElement.scrollHeight,document.body.scrollHeight,"
                "document.documentElement.clientHeight))")
            sleep(2)
        try:
            v_comments = Wait(self.driver, 15).until(
                ec.presence_of_all_elements_located((By.XPATH, '//*[@id="content-text"]')))
        except:
            v_comments = ""
        return v_comments
