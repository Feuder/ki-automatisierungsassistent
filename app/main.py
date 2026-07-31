import logging
import json
from config.settings import PRJ_PFAD, EINGABE_ORDNER, AUSGABE_ORDNER, LOG_ORDNER, SUMMARY_ORDNER, TASK_ORDNER, REPORT_ORDNER, MAX_TIEFE
from ai.ai_client import ordnerbericht
from choices.Metadata import call_metadata
from choices.filestructure.main_phase5 import phase_5
from choices.summerize_tasks_Content import extract_content
from pathlib import Path

logger = logging.getLogger(__name__)

#-------Hier wird überprüft ob die Pfade alle in Ordnung sind-------
LOG_ORDNER.mkdir(parents=True, exist_ok=True)
AUSGABE_ORDNER.mkdir(parents=True, exist_ok=True)
SUMMARY_ORDNER.mkdir(parents=True, exist_ok=True)
TASK_ORDNER.mkdir(parents=True, exist_ok=True)
REPORT_ORDNER.mkdir(parents=True, exist_ok=True)

LOG_DATEI = LOG_ORDNER / "logs.log"

projekt_pfad = PRJ_PFAD
pfad = EINGABE_ORDNER
zusammenfassung_ordner = SUMMARY_ORDNER
aufgaben_ordner = TASK_ORDNER
report_ordner = REPORT_ORDNER
ki_response = None
max_unterordner = MAX_TIEFE

logging.basicConfig(filename=LOG_DATEI, level=logging.INFO, encoding="utf-8")
logger.info("Programm startet")
logger.info("Ordnerstrukturen und Ausgabepfade geprüft")
#---------------------------------------------

#-------Start des Programmes-------
#Hier wird der Relevante Pfad für dennen die Aktionen gemacht werden sollen aufgerufen
print("Gebe den Pfad ein, mit dem du Arbeiten möchtest:\n")
pfad = Path(input()).resolve()

if not pfad.exists() or not pfad.is_dir():
    print("Es gibt ein Problem mit dem Pfad der input Dateien.")
    logger.error("Ungültiger Input-Pfad: %s", pfad)
    raise SystemExit

dateien = [f for f in pfad.iterdir() if f.is_file()]
dateianzahl = []

if not dateien:
    print("Es wurden keine Dateien im Eingabeordner gefunden.")
    logger.info("Keine Dateien im Eingabeordner gefunden: %s", pfad)
    raise SystemExit


relevantes_Objekt = {
    "pfad": pfad,
    "dateien": dateien,
}

relevantes_Objekt["Metadaten"] = call_metadata(relevantes_Objekt)

#Hier wird ausgewählt, was der User machen möchte
print("Was möchtest du machen?:\n" \
"1. Metadaten aller Dateien anzeigen\n" \
"2. Den Inhalt einer Datei zusammenfassen\n" \
"3. Aufgaben erstellen\n" \
"4. Einen Report erzeugen\n" \
"5. Ordnerstrukur Optimieren")

print("Gebe eine Zahl von 1 bis 5 ein:\n")

auswahlzahlen = ["1", "2", "3", "4", "5"]

while True:
    userstartwahl = input()

    if userstartwahl in auswahlzahlen:
        break
    else:
        print("Bitte gebe eine gültige Zahl ein!")


if userstartwahl == "1":
    #Hier werden nur die Metadaten abgerufen und ausgegeben
    for i in relevantes_Objekt["bericht"]:
        print(i)

elif userstartwahl == "2" or userstartwahl == "3":

    ki_response = extract_content(userstartwahl, relevantes_Objekt)

elif userstartwahl == "4":

    metadaten = relevantes_Objekt["Metadaten"]

    for i in metadaten:
        print(i)

    #Den Inhalt und die Daten in die ausgabedatei schreiben
    try:
        inhalt = "\n".join(metadaten)

        ki_response = ordnerbericht(inhalt)

        anzahl_dateien = [1 for datei in report_ordner.iterdir() if datei.is_file()]

        with open(report_ordner / f"Report des durchlauf {len(anzahl_dateien) + 1}.md", "w", encoding="utf-8") as antwortdatei:
            antwortdatei.write("# Automatisierter Ordnerbericht\n\n")
            antwortdatei.write("## Technischer Bericht\n\n")
            antwortdatei.write(f"{inhalt}\n\n")
            antwortdatei.write("## KI-Auswertung\n\n")
            antwortdatei.write(f"{ki_response}\n")

    except Exception as fehler:
        print("Es gab einen Fehler bei der Erstellung des Reports.")
        print(fehler)
        logger.error("Report-Erstellung fehlgeschlagen für: %s", report_ordner)
        logger.error(fehler)
        raise SystemExit

elif userstartwahl == "5":
    try:
        phase_5(pfad, report_ordner)
    except Exception as f:
        print(f)

#----Ab hier werden die ausgaben der Antworten getätigt.----

if ki_response is not None:

    if userstartwahl == "2":

        anzahl_dateien = [1 for f in zusammenfassung_ordner.iterdir() if f.is_file()]

        try:

            with open(zusammenfassung_ordner / f"summary des durchlauf {len(anzahl_dateien) +1}.md", "a", encoding="utf-8") as antwortdatei:
                antwortdatei.write("-----------------------------\n")
                antwortdatei.write("KI Antwort:\n")
                antwortdatei.write(f"{ki_response}\n")
                antwortdatei.write("-----------------------------\n")

        except Exception as fehler:
            print("")
            print("Es gab ein Fehler bei der Antwort-Datei erstellung:\n")
            logger.error("Fehler bei der Zusammenfassungs-Datei: %s", zusammenfassung_ordner)
            print(fehler)
            logger.error(fehler)
            raise SystemExit
    
    elif userstartwahl == "3":

        anzahl_dateien = [1 for f in aufgaben_ordner.iterdir() if f.is_file()]

        try:

            with open(aufgaben_ordner / f"Aufgaben des durchlauf {len(anzahl_dateien) +1}.json", "w", encoding="utf-8") as antwortdatei:
                antwortdatei.write(f"{ki_response}\n")

            aufgaben_daten = json.loads(ki_response)

            print("\n-----------------------------------------------------")

            for aufgabe in aufgaben_daten["aufgaben"]:
                print()
                print(f"Titel: {aufgabe['titel']}")
                print(f"Beschreibung: {aufgabe['beschreibung']}")
                print(f"Priorität: {aufgabe['priorität']}")
                print(f"Status: {aufgabe['status']}")
                print(f"Kategorie: {aufgabe['kategorie']}")
                print(f"Quelle: {aufgabe['quelle']}")
                print(f"Erstellungsdatum: {aufgabe['erstellungsdatum']}")
                print()
                print("-----------------------------------------------------")

            print()

        except Exception as fehler:
            print("")
            print("Es gab ein Fehler bei der Task-erstellungsdatei erstellung:\n")
            logger.error("Fehler bei der Aufgaben-Datei: %s", aufgaben_ordner)
            print(fehler)
            logger.error(fehler)
            raise SystemExit
        
        print()

    if not userstartwahl == "3" and not userstartwahl =="5":
        print("")
        print("------------------------------------------")
        print(ki_response)
        print("------------------------------------------")

logging.info("Programm endet")
logging.info("-" * 100)
logging.info("")
