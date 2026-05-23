import logging
import json
from config.settings import EINGABE_ORDNER, AUSGABE_ORDNER, LOG_ORDNER, SUMMARY_ORDNER, TASK_ORDNER
from ai.ai_client import KI_anfrage, ki_task_erstellen
from utils.text_reader import datei_inhalt



#-------Hier wird überprüft ob die Pfade alle in Ordnung sind-------
LOG_ORDNER.mkdir(parents=True, exist_ok=True)
AUSGABE_ORDNER.mkdir(parents=True, exist_ok=True)
SUMMARY_ORDNER.mkdir(parents=True, exist_ok=True)
TASK_ORDNER.mkdir(parents=True, exist_ok=True)

LOG_DATEI = LOG_ORDNER / "logs.log"

pfad = EINGABE_ORDNER
zusammenfassung_ordner = SUMMARY_ORDNER
aufgaben_ordner = TASK_ORDNER
ki_response = None

logging.basicConfig(filename=LOG_DATEI, level=logging.INFO, encoding="utf-8")
logging.info("Programm startet")
logging.info("Ausgabe wurde geprüft, oder erstellt")

if not pfad.exists() or not pfad.is_dir():
    print("Es gibt ein Problem mit dem Pfad der input Dateien.")
    logging.error("Der Input Pfad wurde nicht gefunden")
    raise SystemExit
#---------------------------------------------

print("Was möchtest du machen?:\n" \
"1. Metadaten aller Dateien anzeigen\n" \
"2. Den Inhalt einer Datei zusammenfassen\n" \
"3. Aufgaben erstellen")

print("Gebe eine Zahl von 1 bis 3 ein:\n")

while True:
    userstartwahl = input()

    if userstartwahl == "1" or userstartwahl == "2" or userstartwahl == "3":
        break
    else:
        print("Bitte gebe eine gültige Zahl ein!")

dateien = [f for f in pfad.iterdir() if f.is_file()]
dateianzahl = []

if userstartwahl == "1":
    #Ab hier wird geguckt was es für Dateien gibt und wie diese heißen.
    bericht = []

    logging.info(f"Anzahl Gefundener Dateien: {len(dateien)}")

    bericht.append("============= Ordnerbericht =============")
    bericht.append("")
    bericht.append(f"Analysierter Pfad: {pfad}")
    bericht.append(f"Anzahl der Dateien: {len(dateien)}")
    bericht.append("")
    bericht.append("Dateien:")

    #Hier werden die Dateien ausgeben
    if dateien:
        for f in dateien:
            if f.suffix:
                bericht.append(f"{f.name} | {f.suffix} | {f.stat().st_size} Bytes")
            else:
                bericht.append(f"{f.name} | Keine Endung | {f.stat().st_size} Bytes")
    else:
        bericht.append("Es wurden keine Dateien gefunden.")
        logging.info("Es wurden keine Dateien gefunden")

    for b in bericht:
        print(b)

elif userstartwahl == "2" or userstartwahl == "3":

    if not dateien:
        print("Es wurden keine Dateien im Eingabeordner gefunden.")
        logging.info("Keine Dateien im Eingabeordner gefunden.")
        raise SystemExit

    for i in range(1, len(dateien) +1):
        dateianzahl.append(i)

    print("")
    print("------------------------------------------")
    for i, f in enumerate(dateien, start=1):
        print(f"{i}. {f.name}")
    print("------------------------------------------")
    print("")
    
    while True:
        try:
            userinput = int(input(f"Wähle eine Zahl zwischen 1 und {len(dateien)} aus\n"))
            
            if userinput in dateianzahl:
                break
            else:
                print("Gebe nur gültige Zahlen an!")

        except ValueError:
            print("Gebe nur gültige Zahlen an!")
            pass
        except Exception:
            print("Es gab einen Fehler bei der Dateiaussuche")
            logging.error("Es gab einen Fehler bei der Dateiaussuche")
            raise SystemExit

    print()

    ausgedatei = dateien[userinput -1]

    inhalt = datei_inhalt(ausgedatei)

    if userstartwahl == "2":
        ki_response = KI_anfrage(inhalt)
    elif userstartwahl == "3":
        ki_response = ki_task_erstellen(inhalt)
    

if ki_response is not None:
    #Ab hier wird die KI Anfrage aufgerufen und ausgegeben

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
            logging.error("Es gab ein Fehler bei der Antwort-Datei erstellung:\n")
            print(fehler)
            logging.error(fehler)
            raise SystemExit
    
    elif userstartwahl == "3":

        anzahl_dateien = [1 for f in aufgaben_ordner.iterdir() if f.is_file()]

        try:

            with open(aufgaben_ordner / f"Aufgaben des durchlauf {len(anzahl_dateien) +1}.json", "a", encoding="utf-8") as antwortdatei:
                antwortdatei.write(f"{ki_response}\n")


            aufgaben = json.loads(ki_response)

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
            logging.error("Es gab ein Fehler bei der Task-erstellungsdatei erstellung:\n")
            print(fehler)
            logging.error(fehler)
            raise SystemExit

    if not userstartwahl == "3":
        print("")
        print("------------------------------------------")
        print(ki_response)
        print("------------------------------------------")


logging.info("Programm endet")