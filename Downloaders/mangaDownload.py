import os
import requests
from bs4 import BeautifulSoup
import time

#Base URL for the manga is the series you want to download so here it would be Black Clover
BASE_URL = "https://ww1.mangafreak.me/Manga/Black_Clover"

# Creates a directory if it doesnt exist can give it the directory name below
# Creates the directory wherever this script is located if no directory exists
def create_directory(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

# Goes and fetches the html of the corresponding page
def fetch_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch {url}. Status code: {response.status_code}")
        return None

# Extracts chapter links from the main manga page
def extract_chapter_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    chapter_tags = soup.select('a.manga_series_list')  # Adjust based on site structure
    chapters = {tag.text.strip(): tag['href'] for tag in chapter_tags if 'href' in tag.attrs}
    return chapters

# Extracts image URLs from the chapter page
def extract_image_urls(html):
    soup = BeautifulSoup(html, 'html.parser')
    image_tags = soup.select('img.img-responsive')  # Adjust based on site structure
    image_urls = [tag['src'] for tag in image_tags if 'src' in tag.attrs]
    return image_urls

# Downloads the images
def download_images(image_urls, chapter_name, base_directory):
    chapter_directory = os.path.join(base_directory, chapter_name)
    create_directory(chapter_directory)

    for index, url in enumerate(image_urls):
        try:
            print(f"Downloading image {index + 1}/{len(image_urls)}: {url}")
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                image_path = os.path.join(chapter_directory, f"page-{index + 1}.jpg")
                with open(image_path, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
            else:
                print(f"Failed to download {url}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")

# Main function
def main():
    base_directory = "Black_Clover_Manga"
    create_directory(base_directory)

    main_page_html = fetch_html(BASE_URL)
    if main_page_html:
        chapters = extract_chapter_links(main_page_html)
        print(f"Found {len(chapters)} chapters.")

        for chapter_name, chapter_url in chapters.items():
            print(f"Processing chapter: {chapter_name}")
            chapter_html = fetch_html(chapter_url)
            if chapter_html:
                image_urls = extract_image_urls(chapter_html)
                if image_urls:
                    download_images(image_urls, chapter_name, base_directory)
                else:
                    print(f"No images found for chapter: {chapter_name}")
                time.sleep(1)  # Be polite and avoid hammering the server
            else:
                print(f"Failed to fetch chapter: {chapter_name}")

if __name__ == "__main__":
    main()
