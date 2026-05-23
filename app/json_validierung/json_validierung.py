import json
from jsonschema import validate, ValidationError, FormatChecker 
import logging
from config.settings import SUMMARY_ORDNER,TASK_ORDNER 

zusammenfassung_ordner = SUMMARY_ORDNER
aufgaben_ordner = TASK_ORDNER

def aufgaben_validieren(inhalt):

    schema = {
        "type": "object",
        "required": ["aufgaben"],
        "additionalProperties": False,
        "properties": {
            "aufgaben": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "required": [
                        "titel",
                        "beschreibung",
                        "priorität",
                        "status",
                        "kategorie",
                        "quelle",
                        "erstellungsdatum"
                    ],
                    "additionalProperties": False,
                    "properties": {
                        "titel": {"type": "string", "minLength": 1},
                        "beschreibung": {"type": "string", "minLength": 1},
                        "priorität": {
                            "type": "string",
                            "enum": ["niedrig", "mittel", "hoch"]
                        },
                        "status": {
                            "type": "string",
                            "enum": ["offen"]
                        },
                        "kategorie": {"type": "string", "minLength": 1},
                        "quelle": {"type": "string", "minLength": 1},
                        "erstellungsdatum": {
                            "type": "string",
                            "format": "date"
                        }
                    }
                }
            }
        }
    }

    try:
        json_daten = json.loads(inhalt)

        validate(
            instance=json_daten,
            schema=schema,
            format_checker=FormatChecker()
        )

        logging.info("Das JSON-Schema wurde erfolgreich validiert.")
        return True, None

    except json.JSONDecodeError as fehler:
        print(
            "Das zurückgegebene JSON ist syntaktisch ungültig.\n"
            "Es wird nochmal probiert:\n"
        )
        logging.error("--------------------------------------")
        logging.error("JSON konnte nicht gelesen werden.")
        logging.error(fehler)
        logging.error("--------------------------------------")
        return False, fehler

    except ValidationError as fehler:
        print(
            "Das JSON entspricht nicht dem erwarteten Schema.\n"
            "Es wird nochmal probiert:\n"
        )
        logging.error("--------------------------------------")
        logging.error("Schema-Validierung fehlgeschlagen.")
        logging.error(fehler)
        logging.error("--------------------------------------")
        return False, fehler