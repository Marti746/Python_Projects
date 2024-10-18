# First attempt at scraping Anilist final result is in AnilistScraper.py
from bs4 import BeautifulSoup
import requests, openpyxl

# create a xl file
excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = 'My Completed Shows'
sheet.append(['Name', 'Score', 'Episodes'])

try:
    # will get the html source of the webpage
    source = requests.get("anilist url here")
    source.raise_for_status() # will throw an error if the webpage is not reachable

    # 'html parser' is the default parser for the html webpage
    soup = BeautifulSoup(source.text, 'html.parser') # will return a beautifulsoup object
    
    # need to use selium because page doesnt load all entries
    group = soup.find_all('div', class_="list-wrap")[1]
    shows = group.find('div', class_="list-entries").find_all('div', class_="entry row")

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
    
    # print(len(shows))

except Exception as e:
    print(e)

# saves the excel sheet
excel.save('AnilistShows.xlsx')