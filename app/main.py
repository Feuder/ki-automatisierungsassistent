import logging
import json
from collections import Counter
from config.settings import EINGABE_ORDNER, AUSGABE_ORDNER, LOG_ORDNER, SUMMARY_ORDNER, TASK_ORDNER, REPORT_ORDNER, MAX_TIEFE
from ai.ai_client import KI_anfrage, ki_task_erstellen, dateiablage_vorschlag, ordnerbericht, dateiablage_vorschlag_erklärung
from Testing.test_response_ki import test_dateiablage_vorschlag
from utils.text_reader import datei_inhalt
from utils.folder_scanner import ordnerinhaltunteror, ordnerinhaltohne
from utils.File_actions.file_actions import move_file, rename_file
from pathlib import Path

#-------Hier wird überprüft ob die Pfade alle in Ordnung sind-------
LOG_ORDNER.mkdir(parents=True, exist_ok=True)
AUSGABE_ORDNER.mkdir(parents=True, exist_ok=True)
SUMMARY_ORDNER.mkdir(parents=True, exist_ok=True)
TASK_ORDNER.mkdir(parents=True, exist_ok=True)
REPORT_ORDNER.mkdir(parents=True, exist_ok=True)

LOG_DATEI = LOG_ORDNER / "logs.log"

pfad = EINGABE_ORDNER
zusammenfassung_ordner = SUMMARY_ORDNER
aufgaben_ordner = TASK_ORDNER
report_ordner = REPORT_ORDNER
ki_response = None
max_unterordner = MAX_TIEFE

logging.basicConfig(filename=LOG_DATEI, level=logging.INFO, encoding="utf-8")
logging.info("-" * 100)
logging.info("Programm startet")
logging.info("Ausgabe wurde geprüft, oder erstellt")

if not pfad.exists() or not pfad.is_dir():
    print("Es gibt ein Problem mit dem Pfad der input Dateien.")
    logging.error("Der Input Pfad wurde nicht gefunden")
    raise SystemExit
#---------------------------------------------

print("Was möchtest du machen?:\n" \
"1. Metadaten aller Dateien anzeigen\n" \
"2. Den Inhalt einer Datei zusammenfassen\n" \
"3. Aufgaben erstellen\n" \
"4. Einen Report erzeugen\n" \
"5. Ordnerstrukur Optimieren")

print("Gebe eine Zahl von 1 bis 5 ein:\n")

auswahlzahlen = ["1", "2", "3", "4", "5"]

while True:
    userstartwahl = input()

    if userstartwahl in auswahlzahlen:
        break
    else:
        print("Bitte gebe eine gültige Zahl ein!")

dateien = [f for f in pfad.iterdir() if f.is_file()]
dateianzahl = []

if userstartwahl == "1":
    #Ab hier wird geguckt was es für Dateien gibt und wie diese heißen.
    bericht = []

    logging.info(f"Anzahl Gefundener Dateien: {len(dateien)}")

    bericht.append("============= Ordnerbericht =============")
    bericht.append("")
    bericht.append(f"Analysierter Pfad: {pfad}")
    bericht.append(f"Anzahl der Dateien: {len(dateien)}")
    bericht.append("")
    bericht.append("Dateien:")

    #Hier werden die Dateien ausgeben
    if dateien:
        for f in dateien:
            if f.suffix:
                bericht.append(f"{f.name} | {f.suffix} | {f.stat().st_size} Bytes")
            else:
                bericht.append(f"{f.name} | Keine Endung | {f.stat().st_size} Bytes")
    else:
        bericht.append("Es wurden keine Dateien gefunden.")
        logging.info("Es wurden keine Dateien gefunden")

    for b in bericht:
        print(b)

elif userstartwahl == "2" or userstartwahl == "3":

    if not dateien:
        print("Es wurden keine Dateien im Eingabeordner gefunden.")
        logging.info("Keine Dateien im Eingabeordner gefunden.")
        raise SystemExit

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
        ki_response = KI_anfrage(inhalt)
    elif userstartwahl == "3":
        ki_response = ki_task_erstellen(inhalt)

elif userstartwahl == "4":

    metadaten = []
    dateitypen = Counter()

    metadaten.append("")
    metadaten.append("============= Ordnerbericht =============")
    metadaten.append("")
    metadaten.append(f"Analysierter Pfad: {pfad}")
    metadaten.append(f"Anzahl der Dateien: {len(dateien)}")
    metadaten.append("")
    metadaten.append("Dateien:")

    if dateien:
        for datei in dateien:
            groesse = datei.stat().st_size

            if datei.suffix:
                endung = datei.suffix.lower()
                dateitypen[endung] += 1
                metadaten.append(f"{datei.name} | {endung} | {groesse} Bytes")
            else:
                dateitypen["Ohne Endung"] += 1
                metadaten.append(f"{datei.name} | Keine Endung | {groesse} Bytes")

        metadaten.append("")
        metadaten.append("Dateitypen:")

        for endung, anzahl in dateitypen.items():
            metadaten.append(f"- {endung}: {anzahl}")

    else:
        metadaten.append("Es wurden keine Dateien gefunden.")
        logging.info("Es wurden keine Dateien gefunden.")

    for eintrag in metadaten:
        print(eintrag)

    print("")

    try:
        inhalt = "\n".join(metadaten)

        ki_response = ordnerbericht(inhalt)

        anzahl_dateien = [1 for datei in report_ordner.iterdir() if datei.is_file()]

        with open(report_ordner / f"Report des durchlauf {len(anzahl_dateien) + 1}.md", "w", encoding="utf-8") as antwortdatei:
            antwortdatei.write("# Automatisierter Ordnerbericht\n\n")
            antwortdatei.write("## Technischer Bericht\n\n")
            antwortdatei.write(f"{inhalt}\n\n")
            antwortdatei.write("## KI-Auswertung\n\n")
            antwortdatei.write(f"{ki_response}\n")

    except Exception as fehler:
        print("Es gab einen Fehler bei der Erstellung des Reports.")
        print(fehler)
        logging.error("Es gab einen Fehler bei der Erstellung des Reports.")
        logging.error(fehler)
        raise SystemExit

elif userstartwahl == "5":

    while True:
        wahlpfad = input("Gebe den zu zu Optimierenden Pfad ein:\n")

        wahlpfad = Path(wahlpfad)

        if not wahlpfad.exists():
            print("Den angegebenen Ordner gibt es nicht. Gebe einen anderen Pfad an!\n")
            logging.error("Der angebene Pfad wurde nicht gefunden!\n")
        elif wahlpfad.is_file():
            print("Der angebene Pfad führt zu einer Datei und kann nicht Analyisert werden!\n")
            logging.warning("Der angebene Pfad führt zu einer Datei und kann nicht Analyisert werden!")
        elif wahlpfad.is_dir() and not any(wahlpfad.iterdir()):
            print("Der Ordner ist leer und kann nicht Analysiert werden\n")
            logging.warning("Der angebenene Ordner ist leer und kann nicht Analysiert werden!")
        else:
            logging.info("Es wurde ein Unterordner oder eine Datei gefunden")
            break

    print("Sollen Unterordner mit einbezogen sein? j/n\n")

    while True:
        unterorderentsch = input().lower()

        if unterorderentsch == "j" or unterorderentsch == "n":
            if unterorderentsch == "j":

                ordnerstat, inhalt = ordnerinhaltunteror(wahlpfad)
            else:

                ordnerstat, inhalt = ordnerinhaltohne(wahlpfad)
            break
        else:
            print("Gebe nur j/n ein!")

    inhalt = "\n".join("".join(i) for i in inhalt)
    
    logging.info("Anfrage an die KI wird gesendet. Es wird auf die Antwort gewartet\n")
    ki_response = dateiablage_vorschlag(inhalt) # Hier wurde erstmal eine statische reingemacht, um Zeit und Kosten für das Testen zu sparen
    #ki_response =  str(test_dateiablage_vorschlag(inhalt))

    if ki_response:
        logging.info("KI Antwort erhalten und erfolgreich zurück bekommen\n")
    else:
        logging.error("Es ist keine Antwort zurück gekommen!\n" \
        "Programm wird beendet!\n")
        raise SystemExit

    anzahl_dateien = [1 for f in report_ordner.iterdir() if f.is_dir()]

    reportpfad = report_ordner / f"Report des durchlauf {len(anzahl_dateien) + 1}"

    reportpfad.mkdir(parents=True, exist_ok=True)

    with open(reportpfad / f"Report des durchlauf {len(anzahl_dateien) +1}.md", "a", encoding="utf-8") as antwortdatei:
        antwortdatei.write("## Technischer Bericht:")
        antwortdatei.write(ordnerstat)
        antwortdatei.write("## KI Ausgabe:")
        antwortdatei.write(f"{ki_response}\n")

    with open(reportpfad / f"Report des durchlauf {len(anzahl_dateien) +1}.json", "w", encoding="utf-8") as antwortdatei:
        antwortdatei.write(f"{ki_response}\n")


    eingetragene_aktionen = []

    while True:

        anzahl_keine_änderungen = 0
        anzahl_neuer_name = 0
        anzahl_verschiebungen  = 0
        anzahl_neuername_verschiebung = 0
        unklar = 0

        print("------------------Zusammenfassung der Analyse:------------------")
        with open(reportpfad / f"Report des durchlauf {len(anzahl_dateien) +1}.json", "r", encoding="utf-8") as antwortdatei:

            roh_daten = json.load(antwortdatei)

            json_daten = roh_daten["datei_vorschläge"]

            for eintrag in json_daten:
                match eintrag["action_type"]:
                    case "keep":
                        if eintrag["erledigt"] == "False":
                            anzahl_keine_änderungen += 1

                    case "move_suggestion":
                        if eintrag["erledigt"] == "False":
                            anzahl_verschiebungen += 1

                    case "rename_suggestion":
                        if eintrag["erledigt"] == "False":
                            anzahl_neuer_name += 1

                    case "rename_and_move_suggestion":
                        if eintrag["erledigt"] == "False":
                            anzahl_neuername_verschiebung += 1

                    case "unclear":
                        if eintrag["erledigt"] == "False":
                            unklar += 1
                        
                    case _:
                        print(f"Unbekannter action_type: {eintrag['action_type']}")

        print(f"Keine Änderungen: {anzahl_keine_änderungen}")
        print(f"Verschiebungen: {anzahl_verschiebungen}")
        print(f"Neuer Name: {anzahl_neuer_name}")
        print(f"Neuer Name + Verschiebung: {anzahl_neuername_verschiebung}")
        print(f"Unklar: {unklar}")

        print()
        print("Möchtest du dir die Vorschläge angucken?")
        print("Wenn ja, was möchtest du machen:")
        print("1. Dateien ohne einen Vorschlag zur Änderung anzeigen")
        print("2. Verschiebungen anzeigen")
        print("3. Neuer Name anzeigen")
        print("4. Neuer Name + Verschiebung anzeigen")
        print("5. Unklare Vorschläge anzeigen")
        print("6. Alle Vorschläge anzeigen")
        print("7. Alle Änderungen anzeigen")
        print("8. Keine Vorschläge anzeigen")

        auswahl = input("Bitte wähle eine Option von 1 bis 8: ").strip()
        auswaählbare_Kategorien = ["1", "2", "3", "4", "5", "6", "7", "8"]

        while True:
            if auswahl in auswaählbare_Kategorien:
                break
            else:
                print(f"Gebe nur 1 - {len(auswaählbare_Kategorien)} ein!")

            auswahl = input()

        match auswahl:
            case "1":
                print("Kategorie: Keine Änderungen")
                ausgewählte_vorschlagen_komp = [eintrag for eintrag in json_daten if eintrag["action_type"] == "keep" and eintrag["erledigt"] == "False"]

            case "2":
                print("Kategorie: Verschiebungen")
                ausgewählte_vorschlagen_komp = [eintrag for eintrag in json_daten if eintrag["action_type"] == "move_suggestion" and eintrag["erledigt"] == "False"]

            case "3":
                print("Kategorie: Neuer Name")
                ausgewählte_vorschlagen_komp = [eintrag for eintrag in json_daten if eintrag["action_type"] == "rename_suggestion" and eintrag["erledigt"] == "False"]

            case "4":
                print("Kategorie: Neuer Name + Verschiebung")
                ausgewählte_vorschlagen_komp = [eintrag for eintrag in json_daten if eintrag["action_type"] == "rename_and_move_suggestion" and eintrag["erledigt"] == "False"]

            case "5":
                print("Kategorie: Unklar")
                ausgewählte_vorschlagen_komp = [eintrag for eintrag in json_daten if eintrag["action_type"] == "unclear" and eintrag["erledigt"] == "False"]

            case "6":
                print("Kategorie: Alle Vorschläge")
                ausgewählte_vorschlagen_komp = [eintrag for eintrag in json_daten if eintrag["erledigt"] == "False" and not eintrag["action_type"] == "keep" and not eintrag["action_type"] == "unclear"]

            case "7":
                print("Es werden alle Änderungen angezeigt")
                ausgewählte_vorschlagen_komp = [eintrag for eintrag in json_daten if not eintrag["action_type"] == "keep" and not eintrag["action_type"] == "unclear" and eintrag["erledigt"] == "False"]

            case "8":
                print("Es wird keine der Vorschläge getätigt.")
                ausgewählte_vorschlagen_komp = []

        print("-" * 50)

        neuer_eintrag = []

        for eintrag in ausgewählte_vorschlagen_komp:
            for key, wert in eintrag.items():
                if wert is not None and str(wert).strip() != "":
                    print(f"{key}: {wert}")
            print("-" * 50)
                                
            if auswahl == "5":
                print("Du kannst mir diesen Unclear erklären, wenn du möchtest. j/n\n")

                while True:
                    erklär_auswahl = input().strip()

                    if erklär_auswahl == "j":
                        print("Okay, dann erkläre mir diese Datei:\n")
                        erklärung = input("")
                        
                        verbessertereintrag = json.loads(
                            dateiablage_vorschlag_erklärung(eintrag, erklärung)
                        )

                        vorschlag = verbessertereintrag["datei_vorschläge"][0]

                        eintrag.update(vorschlag)

                        break

                    elif erklär_auswahl == "n":
                        break
                    else:
                        print("Gebe nur 'j' oder 'n' ein!")

        
        if auswahl == "8":
            print("Es wird kein Vorschlag angezeigt\n" \
            "Sollen andere Vorschläge getätigt werden? j/n\n")

        elif ausgewählte_vorschlagen_komp: 
            print("Sollen die Vorschäge ausgeführt werden? j/n")

            while True:
                phase5_auswahl = input().strip()

                if  phase5_auswahl == "j":
                    logging.info("Die Vorgeschlagenen Vorschläge sollen umgesetzt werden")
                    break

                elif phase5_auswahl == "n":
                    logging.info("Dateivorschläge sollen nicht ausgeführt werden. Programm wird beendet")
                    raise SystemExit
                
                else:
                    print("Gebe nur j/n ein!")


            for i in ausgewählte_vorschlagen_komp:

                if i["erledigt"] == "False":

                    if i["action_type"] == "move_suggestion":

                        datei_name = i["original_name"]
                        alter_pfad = Path(wahlpfad) / i["relative_path"]
                        neuer_pfad = Path(wahlpfad) / i["suggested_folder"]

                        logging.info(
                            f"\n"
                            f"{'-' * 50}\n"
                            f"Aktuelles Objekt: {datei_name}\n"
                            f"Der aktuelle Pfad: {alter_pfad}\n"
                            f"Der neue geplante Pfad: {neuer_pfad}\n"
                            ""
                        )

                        if alter_pfad.exists():

                            if move_file(datei_name, alter_pfad, neuer_pfad):
                                i["erledigt"] = "True"

                        else:
                            logging.warning("" \
                            "Bei dem aktuellen Objekt wurde der alte Pfad nicht gefunden:" \
                            f"{datei_name}\n" \
                            f"{alter_pfad}" \
                            ""
                            )

                    elif i["action_type"] == "rename_suggestion":

                        datei_name = i["original_name"]
                        alter_pfad = Path(wahlpfad) / i["relative_path"]
                        neuer_name =    i["suggested_new_name"]

                        if alter_pfad.exists():
                            logging.info("Pfad existiert, Datei wird bearbeitet.")

                            if rename_file(datei_name, neuer_name, alter_pfad):
                                i["erledigt"] = "True"
                        
                        else:
                            logging.warning("Bei dem aktuellen Objekt wurde der alte Pfad nicht gefunden:" \
                            f"{datei_name}\n" \
                            f"{alter_pfad}\n" \
                            )
                            
                    elif i["action_type"] == "rename_and_move_suggestion":
                        
                        datei_name = i["original_name"]
                        alter_pfad = Path(wahlpfad) / i["relative_path"]
                        neuer_name =    i["suggested_new_name"]
                        neuer_pfad = Path(wahlpfad) / i["suggested_folder"]

                        if alter_pfad.exists() and neuer_name != "":

                            verschobener_pfad = neuer_pfad / datei_name

                            if move_file(datei_name, alter_pfad, neuer_pfad) and rename_file(datei_name, neuer_name, verschobener_pfad):
                                i["erledigt"] = "True"
                        
                        else:
                            logging.warning("Bei dem aktuellen Objekt wurde der alte Pfad nicht gefunden, oder der neue Name ist leer:" \
                            f"{datei_name}\n" \
                            f"{alter_pfad}" \
                            f"{neuer_name}"
                            )
                    else:
                        logging.warning("Es konnte keine Änderung getätigt werden. Es wird übersprungen")
                    
                    if i["erledigt"] == "True":
                        eingetragene_aktionen.append(i)

            roh_daten["datei_vorschläge"] = json_daten

            with open(reportpfad / f"Report des durchlauf {len(anzahl_dateien) +1}.json", "w", encoding="utf-8") as antwortdatei:
                json.dump(roh_daten, antwortdatei, ensure_ascii=False, indent=4)

            with open(reportpfad / f"Ausgeführte Aktionen des durchlauf {len(anzahl_dateien) +1}.json", "w", encoding="utf-8") as ausgeführteaktionen:
                json.dump(eingetragene_aktionen, ausgeführteaktionen, ensure_ascii=False, indent=4)

            print("Sollen auch noch andere Änderungen getätigt werden? j/n")

        else:
            print(""
            "Es wurde kein Vorschlag für diese Funktion gefunden!\n" \
            "Möchtest du andere Änderungen Tätigen? j/n\n")

        neu_input = input().strip()

        while True:
            if neu_input == "j":
                print("Die anderen Änderungen werden angezeigt:")
                break
            elif neu_input == "n":
                print("Änderungen wurden getätigt. Programm wird nun beendet")
                raise SystemExit
            else:
                print("Gebe nur j/n an!\n")
                neu_input = input().strip()   

#----Ab hier werden die ausgaben der Antworten getätigt.----

if ki_response is not None:

    if userstartwahl == "2":

        anzahl_dateien = [1 for f in zusammenfassung_ordner.iterdir() if f.is_file()]

        try:

            with open(zusammenfassung_ordner / f"summary des durchlauf {len(anzahl_dateien) +1}.md", "a", encoding="utf-8") as antwortdatei:
                antwortdatei.write("-----------------------------\n")
                antwortdatei.write("KI Antwort:\n")
                antwortdatei.write(f"{ki_response}\n")
                antwortdatei.write("-----------------------------\n")

        except Exception as fehler:
            print("")
            print("Es gab ein Fehler bei der Antwort-Datei erstellung:\n")
            logging.error("Es gab ein Fehler bei der Antwort-Datei erstellung:\n")
            print(fehler)
            logging.error(fehler)
            raise SystemExit
    
    elif userstartwahl == "3":

        anzahl_dateien = [1 for f in aufgaben_ordner.iterdir() if f.is_file()]

        try:

            with open(aufgaben_ordner / f"Aufgaben des durchlauf {len(anzahl_dateien) +1}.json", "w", encoding="utf-8") as antwortdatei:
                antwortdatei.write(f"{ki_response}\n")

            aufgaben_daten = json.loads(ki_response)

            print("\n-----------------------------------------------------")

            for aufgabe in aufgaben_daten["aufgaben"]:
                print()
                print(f"Titel: {aufgabe['titel']}")
                print(f"Beschreibung: {aufgabe['beschreibung']}")
                print(f"Priorität: {aufgabe['priorität']}")
                print(f"Status: {aufgabe['status']}")
                print(f"Kategorie: {aufgabe['kategorie']}")
                print(f"Quelle: {aufgabe['quelle']}")
                print(f"Erstellungsdatum: {aufgabe['erstellungsdatum']}")
                print()
                print("-----------------------------------------------------")

            print()

        except Exception as fehler:
            print("")
            print("Es gab ein Fehler bei der Task-erstellungsdatei erstellung:\n")
            logging.error("Es gab ein Fehler bei der Task-erstellungsdatei erstellung:\n")
            print(fehler)
            logging.error(fehler)
            raise SystemExit
        
        print()

    if not userstartwahl == "3" and not userstartwahl =="5":
        print("")
        print("------------------------------------------")
        print(ki_response)
        print("------------------------------------------")

logging.info("Programm endet")
logging.info("-" * 100)
logging.info("")