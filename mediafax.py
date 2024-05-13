from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from db.database import PostgreSQL
import os

db = PostgreSQL(os.path.join(os.path.dirname(__file__), 'db', 'config.ini'))

# Start Firefox WebDriver
driver = webdriver.Firefox()

# Navigate to the website
driver.get("https://www.mediafax.ro/")

breaking_news_sections = driver.find_elements(By.CLASS_NAME, "BreakingNews")

# Iterate through each BreakingNews section
href_links = []
news_data = []

for section in breaking_news_sections:
    # Find all news posts within the current BreakingNews section
    news_posts = section.find_elements(By.TAG_NAME, "a")
    
    # Iterate through each news post within the current section
    for post in news_posts:
        # Find the link (href) within the news post if it exists
        link = post.get_attribute("href")
        if link:
            href_links.append(link)

for link in href_links:
    # Navigate to the news post's URL
    driver.get(link)
    
    try:
        # Find the first occurrence of article text content
        article = driver.find_elements(By.CLASS_NAME, "just-article-content")
        #article_text = article.find_element(By.TAG_NAME, "p")
        for elem in article:
        # Print the article text
            try:
                article_text = elem.find_elements(By.TAG_NAME, "p")
                for p in article_text:

                    post_data = {"link": link, "text": p.text, "site":"https://www.mediafax.ro/"}
                    news_data.append(post_data)

            except NoSuchElementException:
                print("No p element here")
    except NoSuchElementException:
        # If the element is not found, print an error message
        print("Article text content not found for this post.")

# Close the WebDriver
driver.close()

db.insert_multiple_data(news_data)
