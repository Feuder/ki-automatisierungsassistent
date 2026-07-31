import logging
from collections import Counter

from config.settings import MAX_TIEFE

max_unterordner = MAX_TIEFE
logger = logging.getLogger(__name__)

def ordnerinhaltunteror(wahlpfad):
    logger.info("Funktion ordnerinhaltunteror() gestartet | Pfad: %s", wahlpfad)

    log = []
    tiefe = 0

    for pfad in wahlpfad.rglob("*"):
        temp_tiefe = len(pfad.relative_to(wahlpfad).parts)
        if temp_tiefe > tiefe:
            tiefe = temp_tiefe

    if tiefe <= max_unterordner:
        dateien = [pfad for pfad in wahlpfad.rglob("*") if pfad.is_file()]
        logger.info("Ordneranalyse: Alle Unterordner werden berücksichtigt | Pfad: %s | MaxTiefe: %s | AktiveTiefe: %s", wahlpfad, max_unterordner, tiefe)
        log.append("Es werden alle existierenden Unterordner mit einbezogen!")
    else:
        dateien = [pfad for pfad in wahlpfad.rglob("*") if pfad.is_file() and len(pfad.relative_to(wahlpfad).parts) <= max_unterordner]
        logging.warning("Es werden nicht alle existierenden Unterordner mit einbezogen!")
        logger.info("Ordneranalyse: Nur Dateien bis Tiefe %s werden berücksichtigt | Pfad: %s | Erreichte Tiefe: %s", max_unterordner, wahlpfad, tiefe)
        print("Die Ordnerstruktur ist tiefer als erlaubt.")
        print("Es werden nur Dateien bis zur erlaubten Tiefe analysiert.")

    metadaten = []
    dateiendungen = Counter()

    if dateien:

        ordnerstat = (
            "\n"
            "----------------Ordnerstruktur---------------\n\n"
            f"Angegebener Pfad: {wahlpfad}\n"
            "Unterordner werden mit einbezogen:\n\n"
            f"Tiefe der Unterordner: {tiefe}\n"
            f"Anzahl der Dateien: {len(dateien)}"
        )

        logger.info("Ordnerstatistik aufgebaut | Pfad: %s | Dateien: %s | Tiefe: %s", wahlpfad, len(dateien), tiefe)
        print(ordnerstat)

        for f in dateien:
            grösse = f.stat().st_size
            dateipfad = f.relative_to(wahlpfad)

            if f.suffix:
                endung = f.suffix.lower()
                dateiendungen[endung] += 1

    
                metadaten.append(f"{f.name} | {endung} | {dateipfad} | {grösse} Bytes")
            else:
                dateiendungen["Ohne Endung"] += 1

                metadaten.append(f"{f.name} | Keine Endung | {dateipfad} | {grösse} Bytes")
                metadaten.append("")

        metadaten.append("Dateiendungen:")

        for endung, anzahl in dateiendungen.items():
            metadaten.append(f"- {endung}: {anzahl}")
            print(f"- {endung}: {anzahl}")
    else:
        logging.error("Es gab einen Fehler bei der Ordnerstrukur erkennung!")
        logging.error(dateien)
        logger.error("Ordnerinhaltunteror() abgebrochen | Pfad: %s | Dateien: %s", wahlpfad, dateien)

        raise SystemExit

    print("")
    logger.info("Ordnerinhaltunteror() beendet | Pfad: %s", wahlpfad)

    return ordnerstat, metadaten

def ordnerinhaltohne(wahlpfad):
    logger.info("Funktion ordnerinhaltohne() gestartet | Pfad: %s", wahlpfad)

    dateien = [pfad for pfad in wahlpfad.iterdir() if pfad.is_file()]
    metadaten = []
    dateiendungen = Counter()

    logger.info("Ordneranalyse ohne Unterordner gestartet | Pfad: %s | Dateien im Ordner: %s", wahlpfad, len(dateien))

    if dateien:

        ordnerstat = (
            "\n"
            "----------------Ordnerstruktur---------------\n\n"
            f"Angegebener Pfad: {wahlpfad}\n"
            f"Anzahl der Dateien: {len(dateien)}"
        )

        print(ordnerstat)

        for f in dateien:
            grösse = f.stat().st_size

            if f.suffix:
                endung = f.suffix.lower()
                dateiendungen[endung] += 1

    
                metadaten.append(f"{f.name} | {endung} | {grösse} Bytes")
            else:
                metadaten.append(f"{f.name} | Keine Endung | {grösse} Bytes")
                metadaten.append("")

        metadaten.append("Dateiendungen:")

        for endung, anzahl in dateiendungen.items():
            metadaten.append(f"- {endung}: {anzahl}")
            print(f"- {endung}: {anzahl}")
    
        print("")    
    else:
        logging.error("Es gab einen Fehler bei der Ordnerstrukur erkennung!")
        logging.error(dateien)
        logger.error("ordnerinhaltohne() abgebrochen | Pfad: %s | Dateien: %s", wahlpfad, dateien)

        raise SystemExit

    logger.info("ordnerinhaltohne() beendet | Pfad: %s", wahlpfad)

    return ordnerstat, metadaten