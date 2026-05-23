from config.settings import get_api_key, get_model
from ai.prompts.prompt_reader import zusammenfassenprompt, task_erstellenpromt
from json_validierung.json_validierung import aufgaben_validieren
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
    
    prompt = str(zusammenfassenprompt())

    try:
        client = get_client()

        response = client.responses.create(
            model=get_model_env(),
            instructions=prompt,
            input=inhalt
        )

        return response.output_text
    
    except Exception as f:
        print("Es gab ein Fehler bei dem OpenAI API Aufruf:\n")
        logging.error("Es gab ein Fehler bei dem OpenAI-API Aufruf\n")
        print(f)
        logging.error(f)
        raise SystemExit
    
def ki_task_erstellen(inhalt):

    prompt = str(task_erstellenpromt())

    original_inhalt = inhalt
    letzter_output = None

    try:
        validiert = False
        fehlermeldung = None
        durchlauf = 0

        while not validiert:

            client = get_client()

            if fehlermeldung is None:
                response = client.responses.create(
                    model=get_model_env(),
                    instructions=prompt,
                    reasoning={"effort": "low"},
                    input=original_inhalt
                )

            elif fehlermeldung is not None and durchlauf <= 3:
                response = client.responses.create(
                    model=get_model_env(),
                    instructions=prompt,
                    reasoning={"effort": "medium"},
                    input=[
                        {
                            "role": "user",
                            "content": (
                                "Der vorherige Output war fehlerhaft.\n\n"
                                f"Fehlermeldung:\n{fehlermeldung}\n\n"
                                "Vorheriger fehlerhafter Output:\n"
                                f"{letzter_output}\n\n"
                                "Bitte gib jetzt ausschließlich gültiges JSON zurück.\n"
                                "Keine Erklärung. Kein Markdown. Kein Text vor oder nach dem JSON.\n\n"
                                "Ursprünglicher Inhalt:\n"
                                f"{original_inhalt}"
                            )
                        }
                    ]
                )

            else:
                print("Zu viele Versuche, das Programm wird beendet. Probiere es noch einmal.")
                logging.error("Wegen zu vielen Versuchen wurde das Programm abgebrochen.")
                logging.error(fehlermeldung)
                raise SystemExit

            letzter_output = response.output_text

            validiert, fehler = aufgaben_validieren(letzter_output)

            if validiert:
                return letzter_output
            else:
                fehlermeldung = fehler
                durchlauf += 1

    except Exception as f:
        print("Es gab einen Fehler bei der Task-Erstellung:\n")
        logging.error("Es gab einen Fehler bei der Task-Erstellung.")
        print(f)
        logging.error(f)
        raise SystemExit