from .video_data import VideoData

print('This is a Web_scrapper package for Youtube')
print('Input the information required and let me do the rest :)')
channel = (input('Youtube channel: '))
scroll_range = int(input('Number of scrolls: '))
driver_path = (input('Path to chromedriver: '))
scraper = VideoData(channel, scroll_range, driver_path)
data = scraper.get_yt_data()
print(f"Scrapping completed\nSee csv file for data.\nThanks for using YouTube scrapper")