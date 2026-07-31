import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def validere_Pfad(i, basis_pfad):
    basis_pfad = Path(basis_pfad).resolve()
    pfad = Path(i["suggested_folder"])

    if pfad.is_absolute():
        logging.warning("Der Pfad darf nicht absolut sein!")
        return False

    if ".." in pfad.parts:
        logging.warning("Der vorgeschlagene Ordner darf kein '..' enthalten.")
        return False

    komp_pfad = (basis_pfad / pfad).resolve()

    if not komp_pfad.is_relative_to(basis_pfad):
        logging.warning("Der Zielpfad liegt außerhalb des angegebenen Ordners.")
        return False

    return True