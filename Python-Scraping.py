# Autor: Nicolas Manser
# Modul 122
# Technische Berufsschule Zürich

import csv
import time
import psycopg2
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Funktion zum Laden der Konfiguration aus einer CSV-Datei
def load_config(csv_file):
    config = {}
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        # Überschrift überspringen, falls vorhanden
        headers = next(reader, None)
        if headers and headers[0].lower().startswith("parameter"):
            pass  # Überschrift wurde gelesen und übersprungen
        else:
            # Falls keine Überschrift, Datei zurücksetzen
            csvfile.seek(0)
            reader = csv.reader(csvfile)
        # Jede Zeile in ein Dictionary einlesen
        for row in reader:
            if not row or row[0].strip().startswith('#'):
                continue  # Leere Zeilen oder Kommentare überspringen
            key = row[0].strip()
            value = row[1].strip() if len(row) > 1 else ""
            config[key] = value
    return config

# Konfiguration laden
config = load_config('config.csv')

# Suchbegriffe (als Liste; erwartet, dass mehrere Einträge durch Semikolon getrennt sind)
search_terms_str = config.get("search_terms", "")
search_terms = [term.strip() for term in search_terms_str.split(';') if term]

# Selenium-Optionen aus der CSV laden und konvertieren
headless = config.get("headless", "False").lower() in ("true", "1", "yes")
driver_path = config.get("driver_path")
if not driver_path:
    raise ValueError("Kein 'driver_path' in der Konfiguration gefunden.")

# Ziel-URL aus der Konfiguration laden
target_url = config.get("target_url", "https://www.google.com")

# Datenbankkonfiguration aus CSV
db_host = config.get("db_host")
db_port = int(config.get("db_port", "5432"))
db_user = config.get("db_user")
db_password = config.get("db_password")
db_name = config.get("db_name")
db_table = config.get("db_table", "search_results")

# Selenium WebDriver konfigurieren
chrome_options = Options()
if headless:
    chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1280,720")

# Service-Objekt mit dem Pfad zum ChromeDriver erstellen
service = Service(driver_path)

# WebDriver starten (Chrome)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Funktion: Tabelle in PostgreSQL erstellen, falls nicht vorhanden
def create_table(cursor, table_name):
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        query TEXT,
        rank INT,
        title TEXT,
        url TEXT,
        scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    cursor.execute(create_table_query)

# Funktion: Suchergebnisse von der Ziel-URL mit Selenium abrufen
def scrape_website(search_query):
    # Navigiere zur Ziel-URL (anstelle von Google)
    driver.get(target_url)
    
    # (Optional: Falls die Zielseite einen Cookie-Consent hat, hier ergänzen)
    try:
        consent_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//text()='Ich stimme zu' or .//text()='I agree']"))
        )
        consent_button.click()
    except Exception:
        pass  # Wenn kein Consent-Fenster erscheint, fortfahren

    # Hier wird angenommen, dass die Zielseite ein Suchfeld mit dem Namen "q" hat.
    # Falls die Struktur abweicht, muss der XPath bzw. Selector angepasst werden.
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.clear()
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)
    
    # Warten, bis Ergebnisse geladen sind (hier wird weiterhin die Google-typische Struktur angenommen)
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='g']"))
    )
    time.sleep(2)  # kurze zusätzliche Pause, um sicherzustellen, dass alles geladen ist

    # Ergebnisse extrahieren: Suche nach <div class="g">, in denen ein <a> mit <h3> enthalten ist
    result_links = driver.find_elements(By.XPATH, "//div[@class='g']//a[h3]")
    
    scraped_data = []
    for i, link in enumerate(result_links, start=1):
        try:
            title = link.find_element(By.TAG_NAME, "h3").text
        except Exception:
            continue
        url = link.get_attribute("href")
        scraped_data.append((title, url))
        print(f"{i}. {title} -> {url}")
    return scraped_data

# Funktion: Ergebnisse in PostgreSQL speichern
def save_results_to_db(connection, table_name, search_query, results):
    cursor = connection.cursor()
    # Tabelle erstellen, falls nicht vorhanden
    create_table(cursor, table_name)
    # Parameterisierte Query zum Einfügen der Ergebnisse
    insert_sql = f"INSERT INTO {table_name} (query, rank, title, url) VALUES (%s, %s, %s, %s);"
    for rank, (title, url) in enumerate(results, start=1):
        cursor.execute(insert_sql, (search_query, rank, title, url))
    connection.commit()
    print(f"Gespeichert: {len(results)} Ergebnisse für Suche '{search_query}'")
    cursor.close()

# Hauptprogramm: Für jeden Suchbegriff aus der CSV durchführen
def main():
    # Verbindung zur PostgreSQL-Datenbank herstellen
    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )
    except Exception as e:
        print("Fehler beim Verbinden mit der Datenbank:", e)
        driver.quit()
        return

    try:
        for term in search_terms:
            print(f"\nSuche nach: {term}")
            results = scrape_website(term)
            save_results_to_db(conn, db_table, term, results)
            # Kurze Pause zwischen den Suchanfragen, um Rate Limiting zu vermeiden
            time.sleep(3)
    finally:
        conn.close()
        driver.quit()
        print("Ressourcen freigegeben.")

if __name__ == "__main__":
    main()
