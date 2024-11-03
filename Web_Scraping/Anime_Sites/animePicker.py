from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time, random

'''
Python Script that uses Selenium and BeautifulSoup to scrape an Anilist profile
Will grab the Planning to Watch shows and take the title and episode count as well, and
run a random selector to find what show you should watch next.
'''

# driver = webdriver.ChromeOptions()
driver = webdriver.Chrome()
# https://anilist.co/user/(username here)/animelist
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
 
    # We will scroll for 40 seconds.
    # You can change it as per your needs and internet speed
    if round(time.time() - start) > 40:
        break

src = driver.page_source
 
# Now using beautiful soup
soup = BeautifulSoup(src, 'html.parser')
# gets the Planning section and all the shows
# [0 = Watching, 1 = Completed, 2 = Dropped, 3 = Planning]
group = soup.find_all('div', class_="list-wrap")[3]
shows = group.find('div', class_="list-entries").find_all('div', class_="entry row")

# HashMap to store the shows and variables within
shows_list = []

for show in shows:
        # finds the title tage and a tag to extract the title 
        # .a only returns the a tag of the div and gets the text from it
        name = show.find('div', class_="title").a.text
        # gets the type attribute
        type = show.find('div', class_="format").text
        episode = show.find('div', class_="progress").text
        
        # Extract  the release status from the class attribute
        status_tag = show.find('span', class_='release-status')
        status = status_tag["class"][-1] if status_tag else "Unkown"

        # Append data to list
        shows_list.append({'Name': name, 'Type': type, 'Episodes': episode, 'Release Status': status})

# Function to pick a random show from the list
def pick_random_show(shows_list):
    available_shows = [show for show in shows_list if show['Release Status'] != "NOT_YET_RELEASED"]
    if not available_shows:
         print("No shows are available to Binge! Go touch Grass")
         return

    random_show = random.choice(available_shows)
    print("Random Show Recommendation:")
    print(f"Name: {random_show['Name']}")
    print(f"Type: {random_show['Type']}")
    print(f"Episodes: {random_show['Episodes']}")
    print(f"Release Status: {random_show['Release Status']}")

# Pick a random show
pick_random_show(shows_list)

# Close the WebDriver
driver.quit()


# <span class="release-status FINISHED"></span> Gets recommended
# <span class="release-status RELEASING"></span> Gets recommended
# <span class="release-status NOT_YET_RELEASED"></span> Doesnt get recommended