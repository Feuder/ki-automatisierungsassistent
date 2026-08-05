import logging
import json
from ai.ai_client import dateiablage_vorschlag, dateiablage_vorschlag_erklärung, Datei_anylsieren
from Testing.test_response_ki import test_dateiablage_vorschlag
from utils.folder_scanner import ordnerinhaltunteror, ordnerinhaltohne
from utils.File_actions.file_actions import move_file, rename_file, move_and_rename_file,create_backup
from utils.Validate_Path import validere_Pfad
from pathlib import Path

def phase_5(pfad, report_ordner):

    print("Sollen Unterordner mit einbezogen sein? j/n\n")

    while True:
        unterorderentsch = input().lower()

        if unterorderentsch == "j" or unterorderentsch == "n":
            if unterorderentsch == "j":

                ordnerstat, inhalt = ordnerinhaltunteror(pfad)
            else:
                ordnerstat, inhalt = ordnerinhaltohne(pfad)
            break
        else:
            print("Gebe nur j/n ein!")
    
    print("Gebe hier die Aufgabe rein. Leer lassen, wenn er einfach machen soll:")
    anweisung = input()
    print("")

    inhalt = "\n".join("".join(i) for i in inhalt)
    
    logging.info("Anfrage an die KI wird gesendet. Es wird auf die Antwort gewartet\n")
    ki_response = dateiablage_vorschlag(inhalt, anweisung) #Hiermit wird die Anfrage an die KI gesendet, um Vorschläge für die Dateistruktur zu erhalten.
    
    #ki_response =  str(test_dateiablage_vorschlag(inhalt))# Hier wurde erstmal eine statische reingemacht, um Zeit und Kosten für das Testen zu sparen

    if ki_response:
        logging.info("KI Antwort erhalten und erfolgreich zurück bekommen\n")
    else:
        logging.error("Es ist keine Antwort zurück gekommen!\n" \
        "Programm wird beendet!\n")
        raise SystemExit

    anzahl_dateien = [1 for f in report_ordner.iterdir() if f.is_dir()]

    reportpfad = report_ordner / f"Report des durchlauf {len(anzahl_dateien) + 1}"

    reportpfad.mkdir(parents=True, exist_ok=True)

    roh_daten = json.loads(ki_response)

    if isinstance(roh_daten, dict) and "datei_vorschläge" in roh_daten:
        überprüfte_daten = roh_daten["datei_vorschläge"]
    else:
        raise TypeError("KI-Antwort hat nicht die erwartete Struktur: 'datei_vorschläge' fehlt.")

    gültige_daten = []

    for eintrag in überprüfte_daten:
        if validere_Pfad(eintrag, pfad):
            gültige_daten.append(eintrag)
        else:
            print("Es wurde ein Vorschlag entfernt! Es gab einen Fehler bei der Erstellung des Vorschlages.")
            logging.warning("Es wurde ein Vorschlag wegen ungültigem Pfad entfernt.")

    roh_daten["datei_vorschläge"] = gültige_daten
    überprüfte_daten = gültige_daten

    logging.info("Es wird geprüft, ob es unklare Dateien gibt.")

    for index, eintrag in enumerate(überprüfte_daten):
        if eintrag.get("action_type") == "unclear":
            try:
                logging.info("Unclear wird genauer untersucht.")

                neuer_vorschlag_response = Datei_anylsieren(eintrag, inhalt, pfad)
                neuer_vorschlag = json.loads(neuer_vorschlag_response)

                if "datei_vorschläge" in neuer_vorschlag:
                    neuer_vorschlag = neuer_vorschlag["datei_vorschläge"][0]

                if validere_Pfad(neuer_vorschlag, pfad):
                    überprüfte_daten[index] = neuer_vorschlag
                    logging.info("Unclear-Vorschlag wurde erfolgreich ersetzt.")
                else:
                    logging.warning("Neuer Vorschlag wurde verworfen, weil der Pfad ungültig ist.")

            except Exception as f:
                print(f)
                logging.error("Fehler bei der Nachanalyse einer unclear-Datei.")
                logging.error(f)

    roh_daten["datei_vorschläge"] = überprüfte_daten

    with open(reportpfad / f"Report des durchlauf {len(anzahl_dateien) + 1}.md", "a", encoding="utf-8") as antwortdatei:
        antwortdatei.write("## Technischer Bericht:\n")
        antwortdatei.write(ordnerstat)
        antwortdatei.write("\n## KI Ausgabe:\n")
        antwortdatei.write(json.dumps(roh_daten, ensure_ascii=False, indent=4))

    with open(reportpfad / f"Report des durchlauf {len(anzahl_dateien) + 1}.json", "w", encoding="utf-8") as antwortdatei:
        json.dump(roh_daten, antwortdatei, ensure_ascii=False, indent=4)

    eingetragene_aktionen = []

    while True:

        anzahl_keine_änderungen = 0
        anzahl_neuer_name = 0
        anzahl_verschiebungen  = 0
        anzahl_neuername_verschiebung = 0
        unklar = 0

        print("")
        print("")
        print("------------------Zusammenfassung der Analyse:------------------")
        json_daten = roh_daten["datei_vorschläge"]

        with open(reportpfad / f"Report des durchlauf {len(anzahl_dateien) + 1}.json", "w", encoding="utf-8") as antwortdatei:
            json.dump(roh_daten, antwortdatei, ensure_ascii=False, indent=4)

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

                if create_backup(alter_pfad):
                
                    if i["erledigt"] == "False":

                        if i["action_type"] == "move_suggestion":

                            datei_name = i["original_name"]
                            alter_pfad = Path(pfad) / i["relative_path"]
                            neuer_pfad = Path(pfad) / i["suggested_folder"]

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
                            alter_pfad = Path(pfad) / i["relative_path"]
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
                            alter_pfad = Path(pfad) / i["relative_path"]
                            neuer_name =    i["suggested_new_name"]
                            neuer_pfad = Path(pfad) / i["suggested_folder"]

                            if alter_pfad.exists() and neuer_name != "":
                                verschobener_pfad = neuer_pfad / datei_name
                            
                            if move_and_rename_file:
                                logging.info("Datei erfolgreich verschoben")
                                    
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
