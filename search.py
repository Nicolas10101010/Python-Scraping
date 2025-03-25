from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

# Set path to ChromeDriver (Replace this with the correct path)
CHROMEDRIVER_PATH = r"C:/Users/nicol/Desktop/TBZ/M122/chromedriver-win64/chromedriver.exe"  # Change this to match your file location

# Initialize WebDriver with Service
service = Service(CHROMEDRIVER_PATH)
options = webdriver.ChromeOptions()


options.add_argument("--window-size=1920,1080")  # Set window size


driver = webdriver.Chrome(service=service, options=options)

# Open Google Search URL
search_url = "https://thomas.stern.ch/"

driver.get(search_url)

# Wait for the page to load
time.sleep(2)

page_html = driver.page_source
print(page_html)