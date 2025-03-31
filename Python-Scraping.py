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
    """Erstellt benötigte Verzeichnisse und Datenbank"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    # Datenbank mit neuer Struktur initialisieren
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('DROP TABLE IF EXISTS scraped_pages')
        conn.execute('''
            CREATE TABLE scraped_pages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                filename TEXT,
                html_content TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

def init_driver():
    options = webdriver.ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)

def create_html_report(html_content, url, filename):
    """Erstellt eine vollständige HTML-Reportdatei"""
    report_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Scraped: {url}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2em; }}
        .meta {{ color: #666; margin-bottom: 2em; }}
        pre {{ 
            background: #f4f4f4;
            padding: 1em;
            border-radius: 5px;
            overflow-x: auto;
        }}
    </style>
</head>
<body>
    <h1>Scraping Report</h1>
    <div class="meta">
        <p>URL: <a href="{url}">{url}</a></p>
        <p>Erstellt am: {datetime.now().strftime("%d.%m.%Y %H:%M")}</p>
    </div>
    <h2>Vollständiger HTML-Code</h2>
    <pre>{html_content}</pre>
</body>
</html>"""
    
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
        
        html_content = driver.page_source
        filename = sanitize_filename(url)
        
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute('''
                INSERT INTO scraped_pages (url, filename, html_content)
                VALUES (?, ?, ?)
            ''', (url, filename, html_content))
        
        saved_path = create_html_report(html_content, url, filename)
        
        print("\nErfolgreich gespeichert!")
        print(f"- Datenbankeintrag: {DB_NAME}")
        print(f"- HTML-Report: {saved_path}")
        
        soup = BeautifulSoup(html_content, "html.parser")
        print(f"- Titel der Seite: {soup.title.string if soup.title else 'Kein Titel gefunden'}")

    except Exception as e:
        print(f"\nFehler: {str(e)}")
        driver.save_screenshot("error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()