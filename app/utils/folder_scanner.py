import logging
from collections import Counter

from config.settings import MAX_TIEFE

max_unterordner = MAX_TIEFE

def ordnerinhaltunteror(wahlpfad):
    tiefe = 0

    for pfad in wahlpfad.rglob("*"):
        tiefe = len(pfad.relative_to(wahlpfad).parts)
        
    dateien = [pfad for pfad in wahlpfad.rglob("*") if pfad.is_file()]
    metadaten = []
    dateiendungen = Counter()

    print(tiefe)
    if tiefe <= max_unterordner:
        logging.info("Es werden alle existierenden Unterordner mit einbezogen!")
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

                if f.suffix:
                    endung = f.suffix.lower()
                    dateiendungen[endung] += 1
                    dateipfad = f.relative_to(wahlpfad)

        
                    metadaten.append(f"{f.name} | {endung} | {dateipfad} | {grösse} Bytes")
                else:
                    metadaten.append(f"{f.name} | Keine Endung | {dateipfad} | {grösse} Bytes")
                    metadaten.append("")

                metadaten.append("Dateiendungen:")

            for endung, anzahl in dateiendungen.items():
                metadaten.append(f"- {endung}: {anzahl}")
                print(f"- {endung}: {anzahl}")
        
        print("")    
    else:
        logging.error("Es werden nicht alle existierenden Unterordner mit ein bezogen!")


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
        logging.error("Es werden nicht alle existierenden Unterordner mit ein bezogen!")


    return ordnerstat, metadaten