from dotenv import load_dotenv
import os
from pathlib import Path
import logging

EINGABE_ORDNER = Path("data/input/")
AUSGABE_ORDNER = Path("data/output/")
LOG_ORDNER = Path("data/logs/")
SUMMARY_ORDNER = Path("data/output/summaries")
TASK_ORDNER = Path("data/output/tasks")
REPORT_ORDNER = Path("data/output/reports")


PRJ_PFAD = Path.cwd().parent.parent
BERICHT_DATEINAME = "ordnerbericht.txt"
BERICHT_DATEIPFAD = AUSGABE_ORDNER / BERICHT_DATEINAME

MAX_TIEFE = 5

def get_api_key():
    ENV_PFAD = Path(__file__).resolve().parent.parent.parent / ".env"
    load_dotenv(ENV_PFAD)

    API_KEY = os.getenv("OPENAI_API_KEY")

    if not API_KEY:
        print("Es konnte kein API-Key gefunden werden")
        logging.error("Es konnte kein API-KEY gefunden werden.")
        raise SystemExit
  
    
    return API_KEY

def get_model():
    ENV_PFAD = Path(__file__).resolve().parent.parent.parent / ".env"
    load_dotenv(ENV_PFAD)

    GPT_VERSION = os.getenv("OPENAI_MODEL")
                            
                                
    if not GPT_VERSION:
        print("Es konnte das GPT Modell nicht sauber aufgerufen werden!")
        logging.error("Es konnte das GPT Modell nicht sauber aufgerufen werden!")
        raise SystemExit
    
    return GPT_VERSION

def get_fehler_moodel():
    ENV_PFAD = Path(__file__).resolve().parent.parent.parent / ".env"
    load_dotenv(ENV_PFAD)

    GPT_VERSION = os.getenv("OPENAI_FEHLER_MODEL")
                            
                                
    if not GPT_VERSION:
        print("Es konnte das GPT Modell nicht sauber aufgerufen werden!")
        logging.error("Es konnte das GPT Modell nicht sauber aufgerufen werden!")
        raise SystemExit
    
    return GPT_VERSION