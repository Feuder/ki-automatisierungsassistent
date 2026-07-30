import logging

from utils.text_reader import datei_inhalt
from ai.ai_client import KI_anfrage, ki_task_erstellen

def extract_content(userstartwahl, relevantes_Objekt):
    logging.info("extract_content wurde aufgerufen")
    dateien = relevantes_Objekt["dateien"]
    dateianzahl = []


    for i in range(1, len(dateien) +1):
        dateianzahl.append(i)

    print("")
    print("------------------------------------------")
    for i, f in enumerate(dateien, start=1):
        print(f"{i}. {f.name}")
    print("------------------------------------------")
    print("")
    
    while True:
        try:
            userinput = int(input(f"Wähle eine Zahl zwischen 1 und {len(dateien)} aus\n"))
            
            if userinput in dateianzahl:
                break
            else:
                print("Gebe nur gültige Zahlen an!")

        except ValueError:
            print("Gebe nur gültige Zahlen an!")
            pass
        except Exception:   
            print("Es gab einen Fehler bei der Dateiaussuche")
            logging.error("Es gab einen Fehler bei der Dateiaussuche")
            raise SystemExit

    print()

    ausgedatei = dateien[userinput -1]

    inhalt = datei_inhalt(ausgedatei)

    if userstartwahl == "2":
        ausgabe = zusammenfassen(inhalt)
    elif userstartwahl == "3":
        ausgabe = aufgabe_erstellen(inhalt)

    return ausgabe

def zusammenfassen(inhalt):
    logging.info("zusammenfassung wurde durch extract_content aufgerufen und wird nun zusammengefasst")

    ki_response = KI_anfrage(inhalt)
    return ki_response

def aufgabe_erstellen(inhalt):
    logging.info("aufgabe_erstellen wurde durch extract_content aufgerufen, Aufgaben werden nun erstellt")
    ki_response = ki_task_erstellen(inhalt)
    return ki_response