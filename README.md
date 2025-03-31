Web Scraper für Google Suchergebnisse
Ein Python-Projekt für die LB1 "Web Scraping mit Python"

Übersicht
Dieses Projekt ermöglicht das automatische Scraping von Webseiteninhalten und speichert die Ergebnisse sowohl in einer Datenbank als auch als HTML-Report. 
Es wurde für die LB1 entwickelt und kombiniert Selenium mit SQLite für eine robuste Datenspeicherung.

Hauptfunktionen

- Automatisiertes Scraping von Webseiteninhalten
- Datenbankintegration (SQLite) mit Zeitstempel
- HTML-Report-Generierung mit Volltextanzeige
- Headless-Browser für unsichtbares Scraping
- Fehlerbehandlung mit automatischen Screenshots

Installation
Voraussetzungen
- Python 3.11+ Download
- Chrome Browser Download
- ChromeDriver Download

Schritte

1. Repository klonen:
git clone https://github.com/Nicolas10101010/Python-Scraping.git

Bibliotheken installieren:
pip install selenium beautifulsoup4
ChromeDriver vorbereiten:
Passende Version für deinen Chrome-Browser wählen
chromedriver.exe im Projektordner speichern
Pfad in CHROMEDRIVER_PATH anpassen

Konfiguration
Anpassungen in config-Abschnitt des Codes:

CHROMEDRIVER_PATH = r"pfad/zum/chromedriver.exe"  #anpassen!
OUTPUT_DIR = "scraped_pages"                      #Ausgabeordner
DB_NAME = "portfolio.db"                          #Datenbankname
HEADLESS = True                                   #Headless-Modus

Erklärung des Programmes:
1. Startvorbereitung
Was passiert: Beim Start wird zuerst der Ordner scraped_pages erstellt (falls nicht vorhanden).
Warum: Damit alle HTML-Reports später gespeichert werden können.

Code-Snippet:
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
2. Datenbank-Setup
Was passiert: Es wird eine SQLite-Datenbank portfolio.db mit einer Tabelle angelegt.

Tabelle enthält:
URL der gescrapten Seite
Dateiname des HTML-Reports
Kompletter HTML-Code
Zeitstempel der Erfassung
Warum wichtig: Alles wird strukturiert gespeichert, damit man später leicht darauf zugreifen kann.

3. Browser starten
Was passiert: Ein unsichtbarer Chrome-Browser wird im Hintergrund gestartet.
Besonderheit: Läuft im Headless-Modus (kein sichtbares Fenster).

Code-Erklärung:
options.add_argument("--headless=new")  # Unsichtbarer Modus

4. Webseite laden
Ablauf:
Du gibst eine URL ein (z.B. https://thomas.stern.ch)
Das Programm überprüft, ob die URL mit http:// oder https:// beginnt
Falls nicht, wird automatisch https:// vorangestellt

5. Warten auf Seitenladung
Was passiert: Das Programm wartet maximal 15 Sekunden, bis die Seite vollständig geladen ist.
Überprüfung: Es checkt, ob das <body>-Tag vorhanden ist.

Code:
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.TAG_NAME, "body"))
    
6. HTML-Code erfassen
Technik: Der komplette Seitenquelltext wird kopiert.

Beispiel: So sieht der gespeicherte HTML-Ausschnitt aus:
html
Copy
<html>
  <head>
    <title>Thomas Stern | TBZ Zürich</title>
  </head>
  <body>...</body>
</html>
Run HTML

7. Dateiname generieren
Regeln:
https:// wird entfernt Sonderzeichen werden durch Unterstriche ersetzt
Maximale Länge: 50 Zeichen
Beispiel:
https://thomas.stern.ch/ → thomas_stern_ch.html

8. Datenbankspeicherung
Prozess:
Verbindung zur Datenbank herstellen
Neuer Eintrag mit URL, Dateiname und HTML-Code
Automatischer Zeitstempel wird hinzugefügt

9. HTML-Report erstellen
Inhalt des Reports:
Eingesetzte URL
Erstellungsdatum

10. Fehlerbehandlung
Bei Crash:
Fehlermeldung wird angezeigt
Screenshot error.png gespeichert
Browser wird sicher beendet
Typische Fehler:
Falsche ChromeDriver-Version
Ungültige URL
Netzwerkprobleme
