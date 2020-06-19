# Rating-Crawler
A python and scrapy based rating crawler, which takes a Movie or TV Series name as input and fetches movie details, Imdb rating,and number of user reviews rated <=5 and the number of reviews rated >=5, rotten tomatoes ratings and number of user reviews rated <=3 and those rated >=3. The program thereafter generates an excel file Movie.xlsx with the details and respective URL's to the pages. The cap size for reviews is 1500, ie it fetches recent reviews upto 1500 reviews.

# Make sure you have the latest version of Python > 3 installed in your machine
Get the latest version from :  http://www.python.org/getit/

# If python is not added to the system PATH, add it :
https://geek-university.com/python/add-python-to-the-windows-path/

# Installing Scrapy and openpyxl
How to Install Scrapy ?
Open a command prompt from the RatingCrawler folder or navigate to the path from command prompt and execute:
pip install scrapy

//If it throws an error Microsoft Visual C++ 14.0 is required

Don't bother installing entire visual studio, download the appropriate whl file from the below link:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted

ie if python version is 3.8 you should be downloading the file with name cp38-cp38

Place it in the RatingCrawler folder(I have placed my version of the file in the folder) and execute 

pip install [that file] for eg: pip install Twisted-20.3.0-cp38-cp38-win32.whl

Now execute pip install scrapy

How to install openpyxl ?
Open a command prompt from the RatingCrawler folder or navigate to the path from command prompt and execute:
pip install openpyxl

# Starting the Rating Crawler:
Double click on start-ratingCrawler.vbs file and wait for the Movie.xlsx file to be generated.

# Stopping the Rating Crawler:
Double click on kill-crawler.bat file
