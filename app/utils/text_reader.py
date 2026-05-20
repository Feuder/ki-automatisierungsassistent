import logging

def datei_inhalt(ausgedate):
    komp_pfad = ausgedate

    Text = komp_pfad.read_text(encoding="utf-8") 
    text = Text.strip()


    if not Text.strip():
        print(
        "----------------------------------------------------------\n" \
        "Es wurde kein Dateiinhalt gefunden" \
        "----------------------------------------------------------\n" \
        "")
        logging.info("[Log] Es wurde kein Textinhalt gefunden")
        raise SystemExit
    
    return text