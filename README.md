# **Web Scraper für Google Suchergebnisse**

Ein Python-Projekt für die **LB1 "Web Scraping mit Python"**

## **Übersicht**
Dieses Projekt ermöglicht das automatische Scraping von Webseiteninhalten und speichert die Ergebnisse sowohl in einer **Datenbank** als auch als **HTML-Report**. 
Es wurde für die **LB1** entwickelt und kombiniert **Selenium mit SQLite** für eine robuste Datenspeicherung.

## **Inhaltsverzeichnis**
1. [Ziele](#ziele)
2. [Hauptfunktionen](#hauptfunktionen)
3. [Installation](#installation)
   - [Voraussetzungen](#voraussetzungen)
   - [Schritte](#schritte)
4. [Konfiguration](#konfiguration)
5. [Erklärung des Programmes](#erklärung-des-programmes)
   - [Startvorbereitung](#startvorbereitung)
   - [Datenbank-Setup](#datenbank-setup)
   - [Browser starten](#browser-starten)
   - [Webseite laden](#webseite-laden)
   - [Warten auf Seitenladung](#warten-auf-seitenladung)
   - [HTML-Code erfassen](#html-code-erfassen)
   - [Dateiname generieren](#dateiname-generieren)
   - [Datenbankspeicherung](#datenbankspeicherung)
   - [HTML-Report erstellen](#html-report-erstellen)
   - [Fehlerbehandlung](#fehlerbehandlung)
6. [Reflexion](#reflexion)


---

## **Ziele**
- Ein Python-Scraper in Python erstellen der funktioniert
- Es sollte die Werte in einem externen File speichern
- Es sollte gutes Problem-handling haben
- Allgemeine wie die Uhrzeit des Scrapes Daten des Scrapes sollen gespeichert werden
- Die Daten des Scrapes sollen in einer Datenbank gespeichert werden
- Eventuell soll ein GUI existieren

---

## **Hauptfunktionen**
- Automatisiertes Scraping von Webseiteninhalten  
- Datenbankintegration (**SQLite**) mit Zeitstempel  
- HTML-Report-Generierung mit Volltextanzeige  
- **Headless-Browser** für unsichtbares Scraping  
- Fehlerbehandlung mit **automatischen Screenshots**  

---

## **Installation**

### **Voraussetzungen**
- [Python 3.11+ herunterladen](https://www.python.org/downloads/)
- [Google Chrome herunterladen](https://www.google.com/chrome/)
- [ChromeDriver herunterladen](https://sites.google.com/chromium.org/driver/)

### **Schritte**

1. **Repository klonen:**  
   ```bash
   git clone https://github.com/Nicolas10101010/Python-Scraping.git
   ```
2. **Benötigte Bibliotheken installieren:**  
   ```bash
   pip install selenium beautifulsoup4
   ```
3. **ChromeDriver vorbereiten:**
   - Passende Version für deinen Chrome-Browser wählen
   - `chromedriver.exe` im Projektordner speichern
   - Pfad in `CHROMEDRIVER_PATH` anpassen

---

## **Konfiguration**
Anpassungen im **config-Abschnitt** des Codes:

```python
CHROMEDRIVER_PATH = r"pfad/zum/chromedriver.exe"  #anpassen!
OUTPUT_DIR = "scraped_pages"                      #Ausgabeordner
DB_NAME = "portfolio.db"                          #Datenbankname
HEADLESS = True                                   #Headless-Modus
```

---

## **Erklärung des Programmes**

### **Startvorbereitung**
**Was passiert?**  
Beim Start wird der Ordner **scraped_pages** erstellt (falls nicht vorhanden).

**Warum?**  
Damit alle HTML-Reports später gespeichert werden können.

**Code-Snippet:**
```python
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
```

---

### **Datenbank-Setup**
**Was passiert?**  
Eine **SQLite-Datenbank** (`portfolio.db`) wird mit einer Tabelle angelegt.

**Tabelle enthält:**  
- URL der gescrapten Seite  
- Dateiname des HTML-Reports  
- Kompletter HTML-Code  
- Zeitstempel der Erfassung  

**Warum wichtig?**  
Alles wird strukturiert gespeichert, damit man später leicht darauf zugreifen kann.

---

### **Browser starten**
**Was passiert?**  
Ein **unsichtbarer Chrome-Browser** wird im Hintergrund gestartet.

**Besonderheit:**  
Läuft im **Headless-Modus** (kein sichtbares Fenster).

**Code:**
```python
options.add_argument("--headless=new")  #Unsichtbarer Modus
```

---

### **Webseite laden**
**Ablauf:**  
Beispiel: `https://thomas.stern.ch`
- Du gibst eine **URL** ein (z. B. `https://thomas.stern.ch`).
- Das Programm überprüft, ob die URL mit `http://` oder `https://` beginnt.
- Falls nicht, wird **automatisch `https://` vorangestellt**.

---

### **Warten auf Seitenladung**
**Was passiert?**  
Das Programm wartet **maximal 15 Sekunden**, bis die Seite vollständig geladen ist.

**Überprüfung:**  
Es checkt, ob das `<body>`-Tag vorhanden ist.

**Code:**
```python
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.TAG_NAME, "body"))
)
```

---

### **HTML-Code erfassen**
**Technik:**  
Der komplette Seitenquelltext wird kopiert.

**Beispiel:**
```html
<html>
  <head>
    <title>Thomas Stern | TBZ Zürich</title>
  </head>
  <body>...</body>
</html>
```

---

### **Dateiname generieren**
**Regeln:**  
- `https://` wird entfernt.
- Sonderzeichen werden durch **Unterstriche** ersetzt.
- Maximale Länge: **50 Zeichen**.

**Beispiel:**
```
https://thomas.stern.ch/ → thomas_stern_ch.html
```

---

### **Datenbankspeicherung**
**Prozess:**  
1. Verbindung zur **Datenbank** herstellen.
2. Neuer Eintrag mit **URL, Dateiname und HTML-Code**.
3. **Automatischer Zeitstempel** wird hinzugefügt.

---

### **HTML-Report erstellen**
**Inhalt des Reports:**  
- **Eingesetzte URL**  
- **Erstellungsdatum**  

---

### **Fehlerbehandlung**
**Bei Crash:**  
- Fehlermeldung wird angezeigt.
- **Screenshot `error.png`** wird gespeichert.
- Browser wird sicher beendet.

**Typische Fehler:**  
- **Falsche ChromeDriver-Version**  
- **Ungültige URL**  
- **Netzwerkprobleme**  

---

## **Reflexion**
Ich finde ich habe meine Projektziele erstaunlich gut erreicht, manchmal sind grosse Probleme aufgekommen wie zum Beispiel beim importieren der Daten in eine Datenbank oder beim hinzufügen eines GUI. Vorallem beim GUI hatte ich riesige Probleme, vorher ging das Programm noch, aber mit dem implementieren des GUI funktionierte nichts mehr. Hätte ich mehr Zeit würde ich definitiv noch mehr mit dem GUI herumprobieren, sodass es schlussendlich auch funktionieren würde. Ich finde es gleichzeitig schade und toll, dass dieses Projekt nicht wirklich eine Partnerarbeit ist, mit einer Partnerarbeit hätte man die Aufgaben besser verteilen können, aber gleichzeitig verstehe ich nun den Python Scraper besser als wenn ich es als Partnerprojekt gemacht hätte.
Würde ich dieses Projekt nochmals durchführen, würde ich definitiv die Unterrichtszeit besser einteilen und dann auch mehr aufpassen, da ich beim Start der LB1 ziemlich ins kalte Wasser geworfen wurde.

--- 

**Version:** 2.1  
**Autor:** Nicolas Manser

