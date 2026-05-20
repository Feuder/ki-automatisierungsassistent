import logging
from config.settings import EINGABE_ORDNER, AUSGABE_ORDNER, LOG_ORDNER, SUMMARIE_ORDNER
from ai.ai_client import KI_anfrage
from utils.text_reader import datei_inhalt

#-------Hier wird überprüft ob die Pfade alle in Ordnung sind-------
LOG_ORDNER.mkdir(parents=True, exist_ok=True)
AUSGABE_ORDNER.mkdir(parents=True, exist_ok=True)
SUMMARIE_ORDNER.mkdir(parents=True, exist_ok=True)

LOG_DATEI = LOG_ORDNER / "logs.log"

pfad = EINGABE_ORDNER
zusammenfassung_ordner = SUMMARIE_ORDNER
ki_response = None

logging.basicConfig(filename=LOG_DATEI, level=logging.INFO, encoding="utf-8")
logging.info("Programm startet")
logging.info("Ausgabe wurde geprüft, oder erstellt")
#---------------------------------------------

print("Was möchtest du machen?:\n" \
"1. Metadaten aller Dateien anzeigen\n" \
"2. Den Inhalt einer Datei zusammenfassen\n")

userstartwahl = int(input("Gebe eine Zahl von 1 bis 2 ein:\n"))

while True:
    if userstartwahl == 1 or userstartwahl == 2:
        break
    else:
        print("Bitte gebe eine gültige Zahl ein!")

dateien = [f for f in pfad.iterdir() if f.is_file()]
dateianzahl = []

if userstartwahl == 1:
    #Ab hier wird geguckt was es für Dateien gibt und wie diese heißen.
    bericht = []
    fehlerbericht = []

    if not pfad.is_dir():
        print("Der Zielpfad existiert nicht oder ist kein Ordner.")
        logging.error("Der Eingabe Ordner existiert nicht")
        fehlerbericht.append("Der Eingabe Ordner existiert nicht")
        raise SystemExit


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
elif userstartwahl == 2:

    for i in range(1, len(dateien) +1):
        dateianzahl.append(i)

    if dateien:
        print("")
        print("------------------------------------------")
        for i, f in enumerate(dateien, start=1):
            print(f"{i}. {f.name}")
        print("------------------------------------------")
        print("")
    
    while True:
        userinput = int(input(f"Wähle eine Zahl zwischen 1 und {len(dateien)} aus\n"))

        if userinput in dateianzahl:
            break
        else:
            print("Gebe nur gültige Zahlen an!")

    ausgedatei = dateien[userinput -1]

    inhalt = datei_inhalt(ausgedatei)

    ki_response = KI_anfrage(inhalt)

if ki_response is not None:
    #Ab hier wird die KI Anfrage aufgerufen und ausgegeben

    anzahl_dateien = [1 for f in zusammenfassung_ordner.iterdir() if f.is_file()]

    try:

        with open(zusammenfassung_ordner / f"summary des durchlauf {len(anzahl_dateien) +1}.txt", "a", encoding="utf-8") as antwortdatei:
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

    print("")
    print("------------------------------------------")
    print(ki_response)
    print("------------------------------------------")


logging.info("Programm endet")