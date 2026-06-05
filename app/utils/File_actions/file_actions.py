import shutil
from pathlib import Path
import logging

def move_file(datei_name, alter_pfad, neuer_pfad):

    try:
        shutil.move(alter_pfad, neuer_pfad)
        
        logging.info(
        "-" * 50 + "\n" +
        f"Die Datei {datei_name} wurde erfolgreich verschoben:\n" \
        f"Alter Speicherort: {alter_pfad}\n" \
        f"Neuer Pfad: {neuer_pfad}"
        "-" * 50
        )
    except Exception as f:
        print("Es gab einen Fehler bei dem versuch folgende Datei zu verschieben:\n" \
        "-" * 50 + "\n" \
        f"Dateiname: {datei_name}")
        f"Fehlermeldung: {f}"

        logging.error("Es gab einen Fehler bei dem versuch folgende Datei zu verschieben:\n" \
        f"Dateiname: {datei_name}")
        f"Fehlermeldung: {f}"


def rename_file(datei_name, neuer_name, alter_pfad):

    try:
        neuer_name = alter_pfad.with_stem(neuer_name)

        alter_pfad.rename(neuer_name)

    except Exception as f:
        print("Es gab einen Fehler bei dem versuch folgende Datei zu verschieben:\n" \
        "-" * 50 + "\n " \
        f"Dateiname: {datei_name}")
        f"Fehlermeldung: {f}"
        
        logging.error("Es gab einen Fehler bei dem versuch folgende Datei zu verschieben:\n" \
        f"Dateiname: {datei_name}")
        f"Fehlermeldung: {f}"
