## Project MiniDrive

Idee:
- Einfache Dateiablage im Browser
- Upload, Download, Delete, Rename
- Ordnerstruktur
- Drag & Drop
- 

---

## Tech Stack

- Python
- Flask / FastAPI
- SQLite
- VueJS 3

- Anmerkungen
    - Docker
    - Docker Compose

## Notizen

Da die gesamte Anwendung eine Validierung der Dateitypen erfordert, ist es sinnvoll, die Anwendung nicht als Drive sondern als Verwaltung spezieller Dateitypen zu sehen. Beispiele wären Dokumente (PDF, Word, Excel) oder Bilder (JPG, PNG, GIF) oder Kontakte (VCF).

Entscheidung:
- Ich werde das ganze als Kontaktverwaltung umsetzen. Ist das für sie okay, Jonathan?

Aufgaben:
- [x] Dummy VCF-Dateien erstellen
- [x] Backend Endpunkte definieren
- [x] Backend implementieren
    - [x] Add Contact
    - [x] Get Contact by ID
    - [x] Update Contact by ID
    - [x] Delete Contact by ID
    - [x] Add Contacts from VCF
- [x] Frontend implementieren
    - [x] Upload Button
    - [x] Tabellarische Übersicht
    - [x] Kontaktfenster
- [x] Docker implementieren
- [x] Docker Compose implementieren
- [x] GitHub Repository erstellen
- [x] GitHub Repository verlinken


Server Side Pagination scheint am sinnvollsten, da die Anzahl der Kontakte potenziell sehr groß werden kann.

## Anforderungen:

```
Basics
-   Saubere Projektstruktur
-   Nachvollziehbare Architekturentscheidungen
-   README-Datei mit Setup- und Startanleitung
-   Freie Themenwahl im Bereich der Containerisierung
-   Abgabe: GitHub Repository (Public) mit Link an uns bis zum 25.02.2026

Backend

-   Python API mit Flask / FastAPI
-   Umsetzung einer CRUD-API mit vier CRUD-Operationen (Create, Read, Update, Delete)
-   OpenAPI Specification (z. B. via Swagger)
-   Authentifizierung der Endpunkte per API-Token (JWT oder statischer Token)
-   SQLite als Datastore
-   File-Upload mit Validierung erlaubter Dateitypen + Speicherung in Projektordner

Frontend

-   VueJS 3-Frontend
-   Mindestens 4 CRUD-Operationen (Create, Read, Update, Delete)
```