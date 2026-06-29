from pathlib import Path
import logging


def call_metadata(relevantes_Objekt):
    logging.info("Call_metadata wurde aufgerufen")

    pfad = Path(relevantes_Objekt["pfad"]).resolve()
    dateien = relevantes_Objekt["dateien"]

    bericht = []
    datei_metadaten = []
    gesamtgroesse = 0

    logging.info(f"Anzahl Gefundener Dateien: {len(dateien)}")

    # Metadaten der einzelnen Dateien sammeln
    for f in dateien:
        f = Path(f).resolve()

        groesse = f.stat().st_size
        gesamtgroesse += groesse

        datei_metadaten.append(
            {
                "name": f.name,
                "endung": f.suffix if f.suffix else "Keine Endung",
                "groesse_bytes": groesse,
                "ordnerpfad": pfad,
                "relativer_pfad": f.relative_to(pfad)
            }
        )

    # Ordner-Metadaten erstellen
    ordnermetadaten = {
        "pfad": pfad,
        "anzahl_dateien": len(dateien),
        "gesamtgroesse_bytes": gesamtgroesse,
        "dateien": datei_metadaten
    }

    # Metadaten in dein vorhandenes Dict schreiben
    relevantes_Objekt["metadata"] = ordnermetadaten

    # Bericht aus den Metadaten erstellen
    bericht.append("============= Ordnerbericht =============")
    bericht.append("")
    bericht.append(f"Analysierter Pfad: {relevantes_Objekt['metadata']['pfad']}")
    bericht.append(f"Anzahl der Dateien: {relevantes_Objekt['metadata']['anzahl_dateien']}")
    bericht.append(f"Gesamtgröße: {relevantes_Objekt['metadata']['gesamtgroesse_bytes']} Bytes")
    bericht.append("")
    bericht.append("Dateien:")

    if datei_metadaten:
        for datei in datei_metadaten:
            bericht.append(
                f"{datei['name']} | {datei['endung']} | {datei['groesse_bytes']} Bytes"
            )
    else:
        bericht.append("Es wurden keine Dateien gefunden.")
        logging.info("Es wurden keine Dateien gefunden")

    # Bericht ebenfalls in das Dict schreiben
    relevantes_Objekt["bericht"] = bericht

    return relevantes_Objekt