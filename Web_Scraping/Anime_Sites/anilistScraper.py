from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time, openpyxl

'''
Python Script that uses Selenium and BeautifulSoup to scrape an Anilist profile
Will grab the completed shows and take the score and episode count as well, and
put all that into an excel spreadsheet with the labels of Name, Score, Episodes
'''

# create a xl file
excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = 'My Completed Shows'
sheet.append(['Name', 'Score', 'Episodes'])

# driver = webdriver.ChromeOptions()
# driver.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome()
driver.get("https://anilist.co/user/(username here)/animelist")
time.sleep(3)
# scroll to the bottom of the page
# driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

start = time.time()
# Scrolls to the end of the page for us
# will be used in the while loop
initialScroll = 0
finalScroll = 1000
 
while True:
    driver.execute_script(f"window.scrollTo({initialScroll}, {finalScroll})")
    # this command scrolls the window starting from
    # the pixel value stored in the initialScroll
    # variable to the pixel value stored at the
    # finalScroll variable
    initialScroll = finalScroll
    finalScroll += 1000
 
    # we will stop the script for 3 seconds so that
    # the data can load
    time.sleep(3)
    # You can change it as per your needs and internet speed
 
    end = time.time()
 
    # We will scroll for 45 seconds.
    # You can change it as per your needs and internet speed
    if round(end - start) > 45:
        break

src = driver.page_source
 
# Now using beautiful soup
# soup = BeautifulSoup(src, 'lxml')
soup = BeautifulSoup(src, 'html.parser')

# gets the completed section and all the shows
group = soup.find_all('div', class_="list-wrap")[1]
shows = group.find('div', class_="list-entries").find_all('div', class_="entry row")
# print(len(shows))

for show in shows:
        # finds the title tage and a tag to extract the title 
        # .a only returns the a tag of the div and gets the text from it
        name = show.find('div', class_="title").a.text
        # gets the score attribute
        score = show.find('div', class_="score").text
        prog = show.find('div', class_="progress").text
        # print(name, score, prog)
        # loads into the excel sheet
        sheet.append([name, score, prog])

# saves the excel sheet
excel.save('AnilistShows.xlsx')