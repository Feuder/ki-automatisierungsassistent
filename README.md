# KI-Automatisierungsassistent

# Ziel:
Am Ende existiert ein lokaler Assistent, der:

Ordner und Dateien analysieren kann.
Berichte erzeugt.
Texte mit KI zusammenfasst.
Aufgaben aus Texten extrahiert.
strukturierte JSON-Ergebnisse speichert.
sichere Automatisierungsaktionen vorbereitet.
später definierte lokale Tools über KI ansteuern kann.

# Projektstruktur

# Aktuelle Stand
Phase 1 ist abgeschlossen
Phase 2 abgeschlossen: Das Projekt kann einen lokalen Eingabeordner prüfen, Dateien erkennen, Dateiendungen und Dateigrößen auslesen und einen einfachen Ordnerbericht im Terminal ausgeben.
Phase 3 abgeschlossen: Zentrale Konfiguration, Ausgabeordner, einfacher Logordner, Fehlerbehandlung und eine einheitliche Terminal-Ausgabe wurden umgesetzt.
Phase 4 abgeschlossen: Hier habe ich die OpenAI anbindung gemacht
Phase 5 abgeschlossen.
Phase 6 abgeschlossen: Das Projekt kann aus einer lokalen Notizdatei per KI Aufgaben extrahieren, Prioritäten und Status vergeben, die Aufgaben als JSON speichern und im Terminal strukturiert anzeigen.
Phase 7 zusatz: Ich habe zusätzlich einen JSON Validiere mit eingebaut, damit die KI ausgabe immer noch überprüft wurde. Wenn dies nicht der Fall ist, wird die Anfrage bis zu 3 mal wiederholt.
Phase 7 abgeschlossen: Das Projekt kann KI-Ausgaben als strukturiertes JSON erzeugen, gegen ein Schema validieren, ungültige Ergebnisse erkennen, JSON speichern und wieder einlesen.
Phase 8 abgeschlossen: Das Projekt kann einen lokalen Eingabeordner analysieren, daraus einen technischen Bericht erzeugen, diesen per KI verständlich zusammenfassen, Handlungsempfehlungen erstellen und das Ergebnis als Markdown-Report speichern.
Phase 9 abgeschlossen: Das Projekt kann einen frei gewählten Ordner analysieren, optional Unterordner einbeziehen, Dateiablage-Vorschläge per KI erzeugen, diese als JSON validieren, als Trockenlauf anzeigen und speichern. Es werden keine Dateien automatisch verändert.

# Geplante Phasen
Phase 10 – Kontrollierte Dateiaktionen

# Projekt einrichten
1. Die .env .example kopieren und mit der API von OPENAI verbinden

## Venv einrichten:
1. Im Projekt Ordner: "python -m venv .venv" ausführen
2. Aktiviere sie mit folgendem Befehl: ".\.venv\Scripts\Activate.ps1"

## Abhängikkeiten Installieren
1. Im Terminal folgenden Befehl ausführen 'pip install -r requirements.txt'
2. PIP Updateten, sofern nicht aktuell 'python.exe -m pip install --upgrade pip'

## Projekt starten
Führe um das Projekt zu starten folgenden Befehl aus: 'Python app\main.py'

## Projekt Bereinigen
1. Um das Projekt zu bereinigen deinstalliere zu erst die Venv: "deactivate; Remove-Item -Recurse -Force .\venv"