import logging
from config.settings import EINGABE_ORDNER, AUSGABE_ORDNER, LOG_ORDNER
from ai.ai_client import einfache_anfrage

#-------Hier wird überprüft ob die Pfade alle in Ordnung sind-------
LOG_ORDNER.mkdir(parents=True, exist_ok=True)
LOG_DATEI = LOG_ORDNER / "logs.log"
AUSGABE_ORDNER.mkdir(parents=True, exist_ok=True)

pfad = EINGABE_ORDNER

logging.basicConfig(filename=LOG_DATEI, level=logging.INFO, encoding="utf-8")
logging.info("Programm startet")
logging.info("Ausgabe wurde geprüft, oder erstellt")
#---------------------------------------------

#Ab hier wird geguckt was es für Dateien gibt und wie diese heißen.
bericht = []
fehlerbericht = []

if not pfad.is_dir():
    print("Der Zielpfad existiert nicht oder ist kein Ordner.")
    logging.error("Der Eingabe Ordner existiert nicht")
    fehlerbericht.append("Der Eingabe Ordner existiert nicht")
    raise SystemExit

dateien = [f for f in pfad.iterdir() if f.is_file()]

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


#Ab hier wird die KI Anfrage aufgerufen und ausgegeben
ki_response = einfache_anfrage()

ausgabe_pfad = AUSGABE_ORDNER

try:
    with open(ausgabe_pfad / "AI-Antwort.txt", "a", encoding="utf-8") as antwortdatei:
        antwortdatei.write("-----------------------------\n")
        antwortdatei.write("KI Antwort:\n")
        antwortdatei.write(f"{ki_response}\n")
        antwortdatei.write("-----------------------------\n")

except Exception as fehler:
    print("Es gab ein Fehler bei der Antwort-Datei erstellung:\n")
    logging.error("Es gab ein Fehler bei der Antwort-Datei erstellung:\n")
    print(fehler)
    logging.error(fehler)
    raise SystemExit


print(ki_response)

logging.info("Programm endet")