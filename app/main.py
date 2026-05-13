import logging
from config.settings import EINGABE_ORDNER, AUSGABE_ORDNER, LOG_ORDNER

LOG_ORDNER.mkdir(parents=True, exist_ok=True)
LOG_DATEI = LOG_ORDNER / "logs.log"

logging.basicConfig(filename=LOG_DATEI, level=logging.INFO, encoding="utf-8")
logging.info("Programm startet")

pfad = EINGABE_ORDNER
AUSGABE_ORDNER.mkdir(parents=True, exist_ok=True)

logging.info("Ausgabe wurde geprüft, oder erstellt")

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

logging.info("Programm endet")