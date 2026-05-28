import logging
from collections import Counter

from config.settings import MAX_TIEFE

max_unterordner = MAX_TIEFE

def ordnerinhaltunteror(wahlpfad):
    tiefe = 0

    for pfad in wahlpfad.rglob("*"):
        temp_tiefe = len(pfad.relative_to(wahlpfad).parts)
        if temp_tiefe > tiefe:
            tiefe = temp_tiefe

    if tiefe <= max_unterordner:
        dateien = [pfad for pfad in wahlpfad.rglob("*") if pfad.is_file()]
        logging.info("Es werden alle existierenden Unterordner mit einbezogen!")
    else:
        dateien = [pfad for pfad in wahlpfad.rglob("*") if pfad.is_file() and len(pfad.relative_to(wahlpfad).parts) <= max_unterordner]
        logging.warning("Es werden nicht alle existierenden Unterordner mit einbezogen!")
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

        raise SystemExit

    print("")   


    return ordnerstat, metadaten

def ordnerinhaltohne(wahlpfad):

    dateien = [pfad for pfad in wahlpfad.iterdir() if pfad.is_file()]
    metadaten = []
    dateiendungen = Counter()

    logging.info("Es werden nur der angebenene Ordner Analyisert")

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

        raise SystemExit


    return ordnerstat, metadaten