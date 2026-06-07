import shutil
from pathlib import Path
import logging

def move_file(datei_name, alter_pfad, neuer_pfad):

    try:
        shutil.move(alter_pfad, neuer_pfad)
        
        logging.info(
        "--------------------------------------------------\n" +
        f"Die Datei {datei_name} wurde erfolgreich verschoben:\n" \
        f"Alter Speicherort: {alter_pfad}\n" \
        f"Neuer Pfad: {neuer_pfad}"
        "--------------------------------------------------"
        )
    except Exception as f:
        print("Es gab einen Fehler bei dem versuch folgende Datei zu verschieben:\n" \
        "--------------------------------------------------\n" +
        f"Dateiname: {datei_name}")
        f"Fehlermeldung: {f}"

        logging.error("Es gab einen Fehler bei dem versuch folgende Datei zu verschieben:\n" \
        f"Dateiname: {datei_name}")
        f"Fehlermeldung: {f}"
    
    logging.info("Dateu wurde erfolgreich verschoben")


def rename_file(datei_name, neuer_name, alter_pfad):

    try:
        neuer_pfad = alter_pfad.with_name(neuer_name)
        alter_pfad.rename(neuer_pfad)
        
    except Exception as f:
        print("Es gab einen Fehler bei dem versuch folgende Datei zu verschieben:\n" \
        "--------------------------------------------------\n" +
        f"Dateiname: {datei_name}")
        f"Fehlermeldung: {f}"
        
        logging.error("Es gab einen Fehler bei dem versuch folgende Datei zu verschieben:\n" \
        f"Dateiname: {datei_name}")
        f"Fehlermeldung: {f}"
    
    logging.info("Dateiname wurde erfolgreich umbenannt")
