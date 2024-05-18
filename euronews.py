from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from db.postgres import PostgreSQL
from db.elastic import ElasticSearch
import os
import time

db = ElasticSearch()

# Start Firefox WebDriver
driver = webdriver.Firefox()

# Navigate to the website
driver.get("https://www.euronews.ro/")

nav_bar = driver.find_element(By.TAG_NAME, "nav")
nav_li = nav_bar.find_elements(By.TAG_NAME, "li")

# Iterate through each BreakingNews section
nav_links = []

for btn in nav_li:
    # Find all news posts within the current BreakingNews section
    button_element = btn.find_element(By.TAG_NAME, "a")
    
    link = button_element.get_attribute("href")

    if link:
        nav_links.append(link)

for page in nav_links:
    try:
        driver.get(page)

        wait = WebDriverWait(driver, 10)
        articles_links = []

        try:
            while True:
                # Wait until the "Load more" button is clickable
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.5)

                parent_div = driver.find_element(By.XPATH, '/html/body/main/section[2]/div/div/footer')
                if 'hidden' in parent_div.get_attribute('class'):
                    break

                load_more_button = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/main/section[2]/div/div/footer/button')))

                driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)

                # Scroll the "Load more" button into view

                wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section[2]/div/div/footer/button')))


                driver.execute_script("arguments[0].click();", load_more_button)

        except Exception as e:
            print(f"Eroare scroll {page}: {e}")

        articles_container = driver.find_element(By.XPATH, "/html/body/main/section[2]/div/div")
        articles_divs = articles_container.find_elements(By.TAG_NAME, "article")
        try:
            for art in articles_divs: 
                try:
                    #article = art.find_element(By.TAG_NAME, "article")
                                                            
                    link_a = art.find_element(By.TAG_NAME, 'a').get_attribute("href")
                    articles_links.append(link_a)

                except Exception as e:
                    print(f"An error occurred: {e}")

        except Exception as e:
            print(f"Eroare extragere link: {e}")

        news_data = []

        for news_link in articles_links:
            try:
                driver.get(news_link)
                _article = driver.find_element(By.XPATH, '/html/body/main/div/div/section/div[1]/article/div[1]/div/section/div/div[2]')
                _text = _article.text

                post_data = {"link": news_link, "text": _text, "site":"https://www.euronews.ro/"}
                news_data.append(post_data)
            except Exception as e:
                print(f"Eroare link in article {news_link}: {e}")

        if(len(news_data) > 0):
            try:
                db.insert_multiple_data(news_data)
            except Exception as e:
                print(f"Eroare insert bd: {e}")
    except Exception as e:
            print(f"Eroare page {page}: {e}")
driver.quit()

# print(news_data)
# Close the WebDriver
# driver.close()


