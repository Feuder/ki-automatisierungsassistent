from config.settings import get_api_key, get_model, get_fehler_moodel
from ai.prompts.prompt_reader import (zusammenfassenprompt, task_erstellenpromt, ordnerbericht_prompt, dateiablage_prompt, erklärung_prompt,datei_anaylse_Prompt)
from json_validierung.json_validierung import aufgaben_validieren, vorschlag_validieren
from utils.loading_screen import ladeanzeige
from utils.text_reader import datei_inhalt
import logging
import json
from openai import OpenAI
from pathlib import Path

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

    try:
        client = get_client()

        with ladeanzeige("Ordnerbericht wird erstellt..."):
            response = client.responses.create(
                model=get_model_env(),
                instructions=prompt,
                input=inhalt
            )

        return response.output_text

    except Exception as fehler:
        print("Es gab einen Fehler bei der Erstellung des Ordnerberichts.")
        print(fehler)
        logging.error("Es gab einen Fehler bei der Erstellung des Ordnerberichts.")
        logging.error(fehler)
        raise SystemExit

def dateiablage_vorschlag(inhalt, anweisung):
    prompt = str(dateiablage_prompt())

    original_inhalt = inhalt
    letzter_output = None
    connection_error = False
    useranweisungen = anweisung

    if useranweisungen:
        anfrage_inhalt = ("Du bekommst gleich einen Inhalt. Dazu kommen folgende Anweisungen, die du ausführen sollst:\n" \
                        f"{useranweisungen}\n" \
                        "Das ist der Inhalt\n" \
                        f"{original_inhalt}"
        )
    else:
        anfrage_inhalt = original_inhalt

    try:
        validiert = False
        fehlermeldung = None
        durchlauf = 0

        while not validiert:
            client = get_client()

            if fehlermeldung is None:
                with ladeanzeige("Dateiablage-Vorschläge werden erstellt..."):
                    response = client.responses.create(
                        model=get_model_env(),
                        instructions=prompt,
                        reasoning={"effort": "low"},
                        input= anfrage_inhalt
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
                logging.error("Wegen zu vielen JSON-Korrekturversuchen wurde das Programm abgebrochen.")
                logging.error(fehlermeldung)
                raise SystemExit

            letzter_output = response.output_text

            validiert, fehler = vorschlag_validieren(letzter_output)

            if validiert:
                return letzter_output
            else:
                fehlermeldung = fehler
                durchlauf += 1

    except Exception as fehler:
        print("-" * 50)
        print("Es gab einen Fehler bei der Erstellung der Dateiablage-Vorschläge.")
        print(fehler)
        logging.error("Es gab einen Fehler bei der Erstellung der Dateiablage-Vorschläge.")
        logging.error(fehler)
        raise SystemExit
    except ConnectionError as ce:
        print("Es gab ein Problem mit der Internet verbindung:" \
        f"{ce}")
        logging.error("Es gab einen Connection Error. Es wird einmal neu probiert")
        logging.error(ce)
        raise SystemExit


def dateiablage_vorschlag_erklärung(json_daten, erklärung):
    prompt = str(erklärung_prompt())

    if isinstance(json_daten, str):
        original_inhalt = json_daten
    else:
        original_inhalt = json.dumps(json_daten, ensure_ascii=False, indent=2)

    user_erklärung = str(erklärung)

    try:
        validiert = False
        fehlermeldung = None
        letzter_output = None
        durchlauf = 0

        while not validiert:
            client = get_client()

            if fehlermeldung is None:
                with ladeanzeige("Dateiablage-Vorschlag wird erstellt..."):
                    response = client.responses.create(
                        model=get_model_env(),
                        instructions=prompt,
                        reasoning={"effort": "low"},
                        input=[
                            {
                                "role": "user",
                                "content": (
                                    "Verbessere diesen Dateiablage-Vorschlag anhand der Erklärung.\n"
                                    "Antworte ausschließlich als gültiges JSON-Objekt.\n"
                                    "Kein Markdown. Kein Text vor oder nach dem JSON.\n\n"
                                    f"Dateiablage-Vorschlag:\n{original_inhalt}\n\n"
                                    f"Erklärung:\n{user_erklärung}"
                                )
                            }
                        ],
                        text={"format": {"type": "json_object"}}
                    )

            elif durchlauf <= 3:
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
                                    "Ursprünglicher Dateiablage-Vorschlag:\n"
                                    f"{original_inhalt}\n\n"
                                    "Ursprüngliche Erklärung:\n"
                                    f"{user_erklärung}"
                                )
                            }
                        ],
                        text={"format": {"type": "json_object"}}
                    )

            else:
                logging.error("Zu viele JSON-Korrekturversuche.")
                logging.error(fehlermeldung)
                raise RuntimeError("Zu viele JSON-Korrekturversuche.")

            letzter_output = response.output_text
            validiert, fehler = vorschlag_validieren(letzter_output)

            if validiert:
                return letzter_output

            fehlermeldung = fehler
            durchlauf += 1

    except Exception as fehler:
        print("Es gab einen Fehler bei der Erstellung der Dateiablage-Vorschlag-Verbesserung.")
        print(fehler)
        logging.error("Fehler bei Dateiablage-Vorschlag-Verbesserung.")
        logging.error(fehler)
        raise

def Datei_anylsieren(eintrag, inhalt, basis_pfad):
    prompt = datei_anaylse_Prompt()
    OrdneranaylsiePrompt = dateiablage_prompt()

    dateipfad = Path(basis_pfad) / eintrag["relative_path"]
    Datei_inhalt = datei_inhalt(dateipfad)

    try:
        validiert = False
        fehlermeldung = None
        letzter_output = None
        durchlauf = 0

        while not validiert:
            client = get_client()

            if fehlermeldung is None:
                model = get_model_env()
                effort = "low"
                lade_text = "Datei wird analysiert..."
                korrektur_text = ""
            elif durchlauf <= 3:
                model = get_fehler_moodel()
                effort = "medium"
                lade_text = "Datei wird erneut geprüft..."
                korrektur_text = (
                    "\n\nDer vorherige Vorschlag war ungültig.\n"
                    f"Validierungsfehler:\n{fehlermeldung}\n\n"
                    f"Vorherige KI-Ausgabe:\n{letzter_output}\n\n"
                    "Erstelle jetzt eine korrigierte gültige JSON-Ausgabe."
                )
            else:
                logging.error("Zu viele JSON-Korrekturversuche.")
                logging.error(fehlermeldung)
                raise RuntimeError("Zu viele JSON-Korrekturversuche.")

            with ladeanzeige(lade_text):
                response = client.responses.create(
                    model=model,
                    instructions=prompt,
                    reasoning={"effort": effort},
                    input=[
                        {
                            "role": "developer",
                            "content": (
                                "Die gegebene Datei ist als 'unclear' markiert worden. "
                                "Analysiere den Inhalt der Datei und entscheide, ob ein besserer Vorschlag möglich ist.\n\n"
                                "Beachte dabei diese Regeln:\n"
                                f"{OrdneranaylsiePrompt}\n\n"
                                "Das ist nicht dein Hauptprompt, sondern nur die Schema- und Regelgrundlage.\n"
                                "Gib nur diese eine Datei aus."
                            ),
                        },
                        {
                            "role": "user",
                            "content": (
                                "Antworte ausschließlich als gültiges JSON-Objekt.\n"
                                "Kein Markdown. Kein Text vor oder nach dem JSON.\n\n"
                                f"Aktueller unclear-Vorschlag:\n{eintrag}\n\n"
                                f"Inhalt der Datei:\n{Datei_inhalt}\n\n"
                                f"Zusätzlicher Kontext aus der Ordneranalyse:\n{inhalt}\n"
                                f"{korrektur_text}"
                            ),
                        }
                    ],
                    text={"format": {"type": "json_object"}}
                )

            letzter_output = response.output_text
            validiert, fehler = vorschlag_validieren(letzter_output)

            if validiert:
                return letzter_output

            fehlermeldung = fehler
            durchlauf += 1

    except Exception as fehler:
        print("Es gab einen Fehler bei der Erstellung der Dateiablage-Vorschlag-Verbesserung.")
        print(fehler)
        logging.error("Fehler bei Dateiablage-Vorschlag-Verbesserung.")
        logging.error(fehler)
        raise
    
