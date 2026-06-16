import logging
from pathlib import Path
from config.settings import PRJ_PFAD

def validere_Pfad(i):
    projekt_pfad = PRJ_PFAD

    pfad = i["suggested_folder"]

    komp_pfad = Path(projekt_pfad + pfad).resolve()

    if not komp_pfad.is_relative_to(projekt_pfad):
        logging.warning("Der Zielpfad liegt außerhalb des angegeben Ordner")

    if komp_pfad.is_absolute():
        logging.warning("Der Pfad darf nicht absolut sein!")

    if ".." in i["suggested_folder"]:
        logging.warning("Der Vorgeschlagende Ordner darf kein '..' enthalten")

    return True