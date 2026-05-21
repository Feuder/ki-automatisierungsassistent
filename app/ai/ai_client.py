from config.settings import get_api_key, get_model
import logging
from openai import OpenAI

client = None
gptmodel = None

def get_client():
    global client 

    if client is None:
        client = OpenAI(api_key = get_api_key())

    return client

def get_model_env():
    global gptmodel

    if gptmodel is None:
        gptmodel = get_model()

    return gptmodel

def KI_anfrage(inhalt):
    try:
        client = get_client()

        response = client.responses.create(
            model=get_model_env(),
            instructions="Du sollst den Inhalt zusammenfassen. Erfinde dabei nichts sondern halte alles bei, was auch in der gegeben Datei steht. Wichtig ist das du nichts dazu schreiben darf. Schreibe die zusammenfassung immer Sätzen, die unterinenander geschrieben werden sollen. Für jede zeile soll es ein minus als Zeilenstart geben",
            input=inhalt
        )

        return response.output_text
    
    except Exception as f:
        print("Es gab ein Fehler bei dem OpenAI API Aufruf:\n")
        logging.error("Es gab ein Fehler bei dem OpenAI-API Aufruf\n")
        print(f)
        logging.error(f)
        raise SystemExit
    
def ki_task_erstellen():
    try:
        client = get_client()

        response = client.responses.create(
            model=get_model_env(),
            instructions="Du bekommst einen Text, oder eine unsortierte Aufgabenliste. Diese sollst du sortieren und sortiert als Aufgabenliste ausgeben. Hierbei sollst du zu jedem Punkt ein Priotät vorschlagen. Nehme entweder: 1.niedrig, 2.mittel, oder 3. hoch. Erfinde nichts dazu und halte dich an den Text den du bekommst. Mache nichts auser diese Liste zu erstellen. Gebe auch nur diese Aufgabenliste aus, nichts anderes!"
            reasoning={"effort": "low"},
            input=inhalt
        )
    except Exception as f:  
        print("Es gab ein Fehler bei dem OpenAI API Aufruf:\n")
        logging.error("Es gab ein Fehler bei dem OpenAI-API Aufruf\n")
        print(f)
        logging.error(f)
        raise SystemExit