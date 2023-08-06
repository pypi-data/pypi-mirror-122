from .video_data import VideoData

print('This is a Web_scrapper package for Youtube')
print('Input the information required and let me do the rest :)')
channel = (input('Youtube channel: '))
height = int(input('Number of videos: '))
driver_path = (input('Path to chromedriver: '))
scraper = VideoData(channel, height, driver_path)
data = scraper.get_yt_data()
print("Data scrapping completed /n See csv file for data. /n Thank you for using YouTube scrapper")
