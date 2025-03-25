from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

# Set path to ChromeDriver (using raw string to handle backslashes)
CHROMEDRIVER_PATH = r"C:/Users/nicol/Desktop/TBZ/M122/chromedriver-win64/chromedriver.exe"  # Verify this matches your file location

# Initialize WebDriver with Service
service = Service(CHROMEDRIVER_PATH)
options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920,1080")  # Set window size

try:
    # Initialize the driver
    driver = webdriver.Chrome(service=service, options=options)

    # Open the specified URL
    search_url = "https://thomas.stern.ch/"
    file = "index.html"
    driver.get(search_url)

    # Wait for the page to load
    time.sleep(2)

    # Get the page source
    page_html = driver.page_source

    # Write to file (append mode)
    with open(file, "a", encoding="utf-8") as f:
        f.write(page_html)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()