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
- [ ] Backend Endpunkte definieren
- [ ] Backend implementieren
    - [ ] Add Contact by ID
    - [ ] Get Contact by ID
    - [ ] Update Contact by ID
    - [ ] Delete Contact by ID
    - [ ] Search Contacts by Name -> Return IDs
- [ ] Frontend implementieren
    - [ ] Upload Button
    - [ ] Tabellarische Übersicht
    - [ ] Kontaktfenster bauen (Name, Nachname, Telefon, E-Mail, Adresse (ggf. darstellung mit OpenStreetMap))
    - [ ] Suchfeld
    - [ ] Button zum Hinzufügen eines Kontaktes
    - [ ] Button zum Bearbeiten eines Kontaktes
    - [ ] Button zum Löschen eines Kontaktes
- [ ] Docker implementieren
- [ ] Docker Compose implementieren
- [x] GitHub Repository erstellen
- [ ] GitHub Repository verlinken


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