import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from src.TextTransformer import TextProcessor

text_processor = TextProcessor()

class EuronewsScraper:
    def __init__(self, db):
        self.driver = None
        self.db = db

    def start_scrapping(self, limit=None):
        # Start Firefox WebDriver
        self.driver = webdriver.Firefox()

        news_data = [] 

        try:
            # Navigate to the website
            self.driver.get("https://www.euronews.ro/")

            nav_bar = self.driver.find_element(By.TAG_NAME, "nav")
            nav_li = nav_bar.find_elements(By.TAG_NAME, "li")

            # Iterate through each BreakingNews section
            nav_links = []

            for btn in nav_li:
                # Find all news posts within the current BreakingNews section
                button_element = btn.find_element(By.TAG_NAME, "a")
                
                link = button_element.get_attribute("href")

                if link:
                    nav_links.append(link)
                    
                if limit and len(nav_links) >= limit:
                    break

            for page in nav_links:
                try:
                    self.driver.get(page)

                    wait = WebDriverWait(self.driver, 10)
                    articles_links = []

                    try:
                        while True:
                            # Wait until the "Load more" button is clickable
                            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                            time.sleep(0.5)

                            parent_div = self.driver.find_element(By.XPATH, '/html/body/main/section[2]/div/div/footer')
                            if 'hidden' in parent_div.get_attribute('class'):
                                break

                            load_more_button = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/main/section[2]/div/div/footer/button')))
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
                            wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section[2]/div/div/footer/button')))
                            self.driver.execute_script("arguments[0].click();", load_more_button)

                    except Exception as e:
                        print(f"Eroare scroll {page}: {e}")

                    articles_container = self.driver.find_element(By.XPATH, "/html/body/main/section[2]/div/div")
                    articles_divs = articles_container.find_elements(By.TAG_NAME, "article")

                    for art in articles_divs: 
                        try:
                            link_a = art.find_element(By.TAG_NAME, 'a').get_attribute("href")
                            articles_links.append(link_a)
                        except NoSuchElementException as e:
                            print(f"An error occurred: {e}")

                    for news_link in articles_links:
                        try:
                            self.driver.get(news_link)
                            _article = self.driver.find_element(By.XPATH, '/html/body/main/div/div/section/div[1]/article/div[1]/div/section/div/div[2]')
                            _text = _article.text

                            summarized_text = text_processor.summarize(_text)
                            tokenized_result = text_processor.tokenize(summarized_text)
                            marked_entities_text = text_processor.mark_entities(summarized_text, tokenized_result)
                                                                                
                            post_data = {"link": news_link, "text": _text, "site":"https://www.euronews.ro/", "summary": summarized_text, "tokenized": tokenized_result, "marked_entities_text": marked_entities_text}
                            news_data.append(post_data)
                        except NoSuchElementException as e:
                            print(f"Eroare link in article {news_link}: {e}")

                        if limit and len(news_data) >= limit:
                            break
                        
                except Exception as e:
                    print(f"Eroare page {page}: {e}")

            if len(news_data) > 0:
                try:
                    self.db.insert_multiple_data(news_data)
                except Exception as e:
                    print(f"Eroare insert bd: {e}")

        finally:
            if self.driver:
                self.driver.quit()
            return news_data

class MediafaxScraper:
    def __init__(self, db):
        self.driver = webdriver.Firefox()
        self.db = db

    def start_scrapping(self, limit=None):
        # Navigate to the website
        self.driver.get("https://www.mediafax.ro/")

        breaking_news_sections = self.driver.find_elements(By.CLASS_NAME, "BreakingNews")

        href_links = []

        for section in breaking_news_sections:
            news_posts = section.find_elements(By.TAG_NAME, "a")
            for post in news_posts:
                link = post.get_attribute("href")
                if link:
                    href_links.append(link)
                if limit and len(href_links) >= limit:
                    break

        news_data = []
        for link in href_links:
            self.driver.get(link)
            text = ""
            try:
                article = self.driver.find_elements(By.CLASS_NAME, "just-article-content")
                for elem in article:
                    try:
                        article_text = elem.find_elements(By.TAG_NAME, "p")
                        for p in article_text:
                            text = text + " " + p.text

                    except NoSuchElementException:
                        print("No p element here")
                if text == "":
                    continue

                summarized_text = text_processor.summarize(text)
                tokenized_result = text_processor.tokenize(summarized_text)
                marked_entities_text = text_processor.mark_entities(summarized_text, tokenized_result)
                                                     
                post_data = {"link": link, "text": text, "site":"https://www.mediafax.ro/", "summary": summarized_text, "tokenized": tokenized_result, "marked_entities_text": marked_entities_text}    
                news_data.append(post_data)
            except NoSuchElementException:
                print("Article text content not found for this post.")

            if limit and len(news_data) >= limit:
                break
            
        if len(news_data) > 0:
            try:
                self.db.insert_multiple_data(news_data)
            except Exception as e:
                print(f"Eroare insert bd: {e}")

        self.driver.quit()

        return news_data
