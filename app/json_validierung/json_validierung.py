import json
from jsonschema import validate, ValidationError, FormatChecker 
import logging

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
    
def vorschlag_validieren(inhalt):

    schema_datei_vorschläge = {

        "type": "object",
        "required": ["datei_vorschläge"],
        "additionalProperties": False,
        "properties": {
            "datei_vorschläge": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "required": [
                        "original_name",
                        "relative_path",
                        "file_type",
                        "suggested_category",
                        "suggested_folder",
                        "suggested_new_name",
                        "action_type",
                        "reason"
                    ],
                    "additionalProperties": False,
                    "properties": {
                        "original_name": {
                            "type": "string",
                            "minLength": 1
                        },
                        "relative_path": {
                            "type": "string",
                            "minLength": 1
                        },
                        "file_type": {
                            "type": "string",
                            "minLength": 1
                        },
                        "suggested_category": {
                            "type": "string",
                            "minLength": 1
                        },
                        "suggested_folder": {
                            "type": "string",
                            "minLength": 1
                        },
                        "suggested_new_name": {
                            "type": "string",
                            "minLength": 1
                        },
                        "action_type": {
                            "type": "string",
                            "enum": [
                                "keep",
                                "move_suggestion",
                                "rename_suggestion",
                                "rename_and_move_suggestion",
                                "unclear"
                            ]
                        },
                        "reason": {
                            "type": "string",
                            "minLength": 1
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
            schema=schema_datei_vorschläge,
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