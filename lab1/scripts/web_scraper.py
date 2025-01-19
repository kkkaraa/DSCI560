import os
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO)

output_path = '../data/raw_data/web_data.html'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

driver_path = "/usr/local/bin/chromedriver"
service = Service(driver_path)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=service, options=options)

url = "https://www.cnbc.com/world/?region=world"

try:
    logging.info("Fetching the webpage using Selenium...")
    driver.get(url)

    logging.info("Waiting for the Market Cards rows to be populated...")
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "MarketCard-row"))
    )

    logging.info("Parsing the HTML content with BeautifulSoup...")
    soup = BeautifulSoup(driver.page_source, "html.parser")

    logging.info("Extracting the latest news panel...")
    latest_news = soup.find("ul", class_="LatestNews-list")
    latest_news_html = latest_news.prettify() if latest_news else "Latest news panel not found."

    logging.info("Extracting the market banner HTML tags...")
    market_banner = soup.find("div", class_="MarketsBanner-marketData")
    market_banner_html = market_banner.prettify() if market_banner else "Market banner not found."

    logging.info("Saving the extracted content to an HTML file...")
    with open(output_path, "w", encoding="utf-8") as file:
        if market_banner_html:
            file.write(market_banner_html)
            file.write("\n\n")
        if latest_news_html:
            file.write(latest_news_html)

    logging.info("Printing the first ten lines of the saved HTML file...")
    with open(output_path, "r", encoding="utf-8") as file:
        for _ in range(10):
            print(file.readline().strip())

except Exception as e:
    logging.error("An unexpected error occurred: %s", e)
finally:
    driver.quit()