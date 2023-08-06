# YouTube Scrapper
The YouTube scrapper is a data pipeline that allows you to extract data from videos posted on YouTube.
The scrapper will extract information such as; **_video titles_**, **_descriptions_**, **_the number 
of views_** the video has and all the users or viewers' **_comments_** per each video. Information extracted is 
dumped into a csv file which can then be uploaded to an Amazon RDS database.

## Getting Started
1. Make sure pip and Chromedriver is installed.
2. Download package by using _**pip install Youtube-scrapper**_ in console
3. Run '_python -m youtube_scrapper_' on your terminal
4. A prompt to enter the following information will pop up;
   1. channel - this takes the youtube channel you want to scrape data from
   2. scroll_range - this indicates how many video you want the scrapper to look and grab information from. 
   3. driver_path - this directs the package to the location where chromedriver is installed on your of system.
5. Once the information is passed in, the scrapper will start grabbing all information requested. 
6. Once finished, the data is returned in a csv file which can be found at the directory level the package was run.

## Note
+ When the scroll_range value is 0, 30 videos (The least amount of videos that will be scrapped) are returned from the channel specified. Each time the value goes up by 1, 30 more videos are returned.
+ Run time takes a while (approximately 30mins for 30 videos)

## Dependencies
+ Python 3.7.9
+ selenium 3.141.0
+ pandas 1.3.2