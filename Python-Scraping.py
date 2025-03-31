from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import sqlite3
import os
import re
from datetime import datetime

# Konfiguration
CHROMEDRIVER_PATH = r"C:\Users\nicol\Desktop\TBZ\M122\chromedriver-win64\chromedriver.exe"
OUTPUT_DIR = "scraped_pages"
DB_NAME = "portfolio.db"
HEADLESS = True

def sanitize_filename(url):
    """Erzeugt einen sicheren Dateinamen aus der URL"""
    filename = re.sub(r"https?://", "", url)
    filename = re.sub(r"[^\w\-_\.]", "_", filename)
    return filename[:50] + ".html"

def setup_environment():
    """Erstellt benötigte Verzeichnisse"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def init_driver():
    options = webdriver.ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)

def create_html_report(soup, url, filename):
    """Erstellt eine strukturierte HTML-Datei"""
    report_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Scraped: {url}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 2em; }}
            .meta {{ color: #666; margin-bottom: 2em; }}
            iframe {{ width: 100%; height: 600px; border: 1px solid #ddd; }}
        </style>
    </head>
    <body>
        <h1>Scraping Report</h1>
        <div class="meta">
            <p>URL: <a href="{url}">{url}</a></p>
            <p>Erstellt am: {datetime.now().strftime("%d.%m.%Y %H:%M")}</p>
        </div>
        <h2>Vorschau</h2>
        <iframe srcdoc='{soup.prettify().replace("'", "&#39;")}'></iframe>
        <h2>Rohdaten</h2>
        <pre>{soup.prettify()}</pre>
    </body>
    </html>
    """
    
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report_html)
    return filepath

def main():
    setup_environment()
    
    url = input("Bitte URL eingeben: ").strip()
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"

    driver = init_driver()
    try:
        print(f"\nScrape: {url}")
        driver.get(url)
        
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        filename = sanitize_filename(url)
        
        # Datenbank speichern
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS scraped_pages (
                    id INTEGER PRIMARY KEY,
                    url TEXT UNIQUE,
                    filename TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.execute('''
                INSERT INTO scraped_pages (url, filename)
                VALUES (?, ?)
            ''', (url, filename))
        
        # HTML-Report erstellen
        saved_path = create_html_report(soup, url, filename)
        
        print("\nErfolgreich gespeichert!")
        print(f"- Datenbankeintrag: {DB_NAME}")
        print(f"- HTML-Report: {saved_path}")
        print(f"- Titel der Seite: {soup.title.string}")

    except Exception as e:
        print(f"\nFehler: {str(e)}")
        driver.save_screenshot("error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()