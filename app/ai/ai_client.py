from config.settings import get_api_key, get_model, get_fehler_moodel
from ai.prompts.prompt_reader import zusammenfassenprompt, task_erstellenpromt, ordnerbericht_prompt
from json_validierung.json_validierung import aufgaben_validieren, vorschlag_validieren
from utils.loading_screen import ladeanzeige
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

        with ladeanzeige("Zusammenfassung wird erstellt..."):
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
                with ladeanzeige("Aufgaben werden erstellt..."):
                    response = client.responses.create(
                        model=get_model_env(),
                        instructions=prompt,
                        reasoning={"effort": "low"},
                        input=original_inhalt
                    )

            elif fehlermeldung is not None and durchlauf <= 3:
                with ladeanzeige("JSON wird korrigiert..."):
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
    

def ordnerbericht(inhalt):
    prompt = str(ordnerbericht_prompt())
    
    original_inhalt = inhalt
    letzter_output = None

    try:
        validiert = False
        fehlermeldung = None
        durchlauf = 0

        while not validiert:
            client = get_client()

            if fehlermeldung is None:
                with ladeanzeige("Ordnerbericht wird erstellt..."):
                    response = client.responses.create(
                        model=get_model_env(),
                        instructions=prompt,
                        reasoning={"effort": "low"},
                        input= inhalt
                    )

            elif fehlermeldung is not None and durchlauf <= 3:
                with ladeanzeige("JSON wird korrigiert..."):
                    response = client.responses.create(
                        model=get_fehler_moodel(),
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

            validiert, fehler = vorschlag_validieren(letzter_output)

            if validiert:
                return letzter_output
            else:
                fehlermeldung = fehler
                durchlauf += 1

        return response.output_text
    
    except Exception as f:
        print("Es gab einen Fehler bei der erstellung des Ordnerberichts")
        print(f)
        logging.error("Es gab einen Fehler bei der erstellung des Ordnerberichts")
        logging.error(f)
        raise SystemExit
