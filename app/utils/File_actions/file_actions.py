import shutil
from pathlib import Path
import logging

def move_file(datei_name, alter_pfad, neuer_pfad):
    
    try:
        alter_pfad = Path(alter_pfad)
        ziel_ordner = Path(neuer_pfad)
        ziel_datei = ziel_ordner / datei_name

        if not alter_pfad.exists():
            logging.error(
                "Die Quelldatei wurde nicht gefunden:\n"
                f"Dateiname: {datei_name}\n"
                f"Alter Pfad: {alter_pfad}\n"
            )
            return False

        if not alter_pfad.is_file():
            logging.error(
                "Der alte Pfad ist keine Datei:\n"
                f"Dateiname: {datei_name}\n"
                f"Alter Pfad: {alter_pfad}\n"
            )
            return False

        ziel_ordner.mkdir(parents=True, exist_ok=True)

        if ziel_datei.exists():
            logging.error(
                "Die Zieldatei existiert bereits:\n"
                f"Dateiname: {datei_name}\n"
                f"Zieldatei: {ziel_datei}\n"
                f"Alter Pfad: {alter_pfad}\n"
            )
            return False

        shutil.move(str(alter_pfad), str(ziel_datei))

        logging.info(
            "--------------------------------------------------\n"
            f"Die Datei {datei_name} wurde erfolgreich verschoben:\n"
            f"Alter Speicherort: {alter_pfad}\n"
            f"Neuer Speicherort: {ziel_datei}\n"
            "--------------------------------------------------"
        )

        return True

    except Exception as f:
        print(
            "Es gab einen Fehler bei dem Versuch, folgende Datei zu verschieben:\n"
            "--------------------------------------------------\n"
            f"Dateiname: {datei_name}\n"
            f"Fehlermeldung: {f}"
        )

        logging.error(
            "Es gab einen Fehler bei dem Versuch, folgende Datei zu verschieben:\n"
            f"Dateiname: {datei_name}\n"
            f"Alter Pfad: {alter_pfad}\n"
            f"Neuer Pfad: {neuer_pfad}\n"
            f"Fehlermeldung: {f}"
        )

        return False

def rename_file(datei_name, neuer_name, alter_pfad):
    
    try:
        alter_pfad = Path(alter_pfad)

        if not alter_pfad.exists():
            logging.error(
                "Die Quelldatei wurde nicht gefunden:\n"
                f"Dateiname: {datei_name}\n"
                f"Pfad: {alter_pfad}\n"
            )
            return False

        if not alter_pfad.is_file():
            logging.error(
                "Der alte Pfad ist keine Datei:\n"
                f"Dateiname: {datei_name}\n"
                f"Pfad: {alter_pfad}\n"
            )
            return False

        if neuer_name is None or str(neuer_name).strip() == "":
            logging.error(
                "Der neue Dateiname ist leer:\n"
                f"Alter Dateiname: {datei_name}\n"
                f"Pfad: {alter_pfad}\n"
            )
            return False

        neuer_name = str(neuer_name).strip()

        if "/" in neuer_name or "\\" in neuer_name:
            logging.error(
                "Der neue Dateiname darf keinen Pfad enthalten:\n"
                f"Alter Dateiname: {datei_name}\n"
                f"Neuer Name: {neuer_name}\n"
            )
            return False

        neuer_pfad = alter_pfad.with_name(neuer_name)

        if neuer_pfad.exists():
            logging.error(
                "Die Zieldatei existiert bereits:\n"
                f"Alter Dateiname: {datei_name}\n"
                f"Neuer Name: {neuer_name}\n"
                f"Alter Pfad: {alter_pfad}\n"
                f"Neuer Pfad: {neuer_pfad}\n"
            )
            return False

        alter_pfad.rename(neuer_pfad)

        logging.info(
            "--------------------------------------------------\n"
            f"Die Datei {datei_name} wurde erfolgreich umbenannt:\n"
            f"Alter Pfad: {alter_pfad}\n"
            f"Neuer Pfad: {neuer_pfad}\n"
            "--------------------------------------------------"
        )

        return True

    except Exception as f:
        print(
            "Es gab einen Fehler bei dem Versuch, folgende Datei umzubenennen:\n"
            "--------------------------------------------------\n"
            f"Dateiname: {datei_name}\n"
            f"Neuer Name: {neuer_name}\n"
            f"Fehlermeldung: {f}"
        )

        logging.error(
            "Es gab einen Fehler bei dem Versuch, folgende Datei umzubenennen:\n"
            f"Dateiname: {datei_name}\n"
            f"Neuer Name: {neuer_name}\n"
            f"Alter Pfad: {alter_pfad}\n"
            f"Fehlermeldung: {f}"
        )

        return False
    
def move_and_rename_file(datei_name, alter_pfad, neuer_pfad, neuer_name):

    try:
        move_status = move_file(datei_name, alter_pfad, neuer_pfad)

    except Exception as f:
        print("Es gab einen Fehler bei der verschiebung der Datei:\n" \
                f"{f}")
        logging.error("Es gab einen Fehler bei der verschiebung der Datei:\n" \
                    f"{f}")

    try:
        rename_staus = rename_file(datei_name, neuer_name, alter_pfad)
    
    except Exception as f:
        print("Es gab einen Fehler bei der neu benneung der Datei:\n" \
            f"{f}")
        logging.error("Es gab einen Fehler bei der neu benneung der Datei:\n" \
            f"{f}")
        
    if move_status == True and rename_staus == True:
        return True
    else:
        return False

        