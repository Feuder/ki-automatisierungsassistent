import json

def test_dateiablage_vorschlag(inhalt):
    
    t = inhalt

    test_inhalt = {
"datei_vorschläge": [
{
"original_name": "Alte_Notiz_ohne_Zusammenhang.txt",
"relative_path": "Alte_Notiz_ohne_Zusammenhang.txt",
"file_type": "txt",
"suggested_category": "",
"suggested_folder": "",
"suggested_new_name": "Alte_Notiz_ohne_Zusammenhang(Neu).txt",
"action_type": "rename_suggestion",
"reason": "Datei liegt im Root ohne eindeutigen Kontext oder Zielordner im Bericht.",
"erledigt": "False"
},
{
"original_name": "Archivrest_2024.old",
"relative_path": "Archivrest_2024.old",
"file_type": "old",
"suggested_category": "",
"suggested_folder": "10_Archiv\\Altbestand",
"suggested_new_name": "",
"action_type": "move_suggestion",
"reason": "Name deutet auf Altbestand hin; passender Ordner 10_Archiv\\Altbestand ist vorhanden.",
"erledigt": "False"
},
{
"original_name": "Bild_ohne_Kontest sda.png",
"relative_path": "Bild_ohne_Kontest sda.png",
"file_type": "png",
"suggested_category": "Bild",
"suggested_folder": "05_Bilder",
"suggested_new_name": "",
"action_type": "move_suggestion",
"reason": "PNG-Bild liegt im Root; zentraler Bilder-Ordner 05_Bilder existiert.",
"erledigt": "False"
},
{
"original_name": "Download_Unbekannt_2026.dat",
"relative_path": "Download_Unbekannt_2026.dat",
"file_type": "dat",
"suggested_category": "",
"suggested_folder": "01_Eingang",
"suggested_new_name": "",
"action_type": "move_suggestion",
"reason": "Unbekannter Download passt in den Eingangsordner 01_Eingang.",
"erledigt": "False"
},
{
"original_name": "Kopie_von_Datei.alt",
"relative_path": "Kopie_von_Datei.alt",
"file_type": "alt",
"suggested_category": "",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "unclear",
"reason": "Datei im Root mit unbekannter Endung und Zweck nicht erkennbar.",
"erledigt": "False"
},
{
"original_name": "Liesmich_Altbestand.md",
"relative_path": "Liesmich_Altbestand.md",
"file_type": "md",
"suggested_category": "Dokumentation",
"suggested_folder": "10_Archiv\\Altbestand",
"suggested_new_name": "",
"action_type": "move_suggestion",
"reason": "„Liesmich“ zum Altbestand passt in 10_Archiv\\Altbestand.",
"erledigt": "False"
},
{
"original_name": "Privater_Merkzettel.txt",
"relative_path": "Privater_Merkzettel.txt",
"file_type": "txt",
"suggested_category": "",
"suggested_folder": "07_Sonstiges",
"suggested_new_name": "",
"action_type": "move_suggestion",
"reason": "Privater Merkzettel ohne fachlichen Bezug passt in 07_Sonstiges.",
"erledigt": "False"
},
{
"original_name": "Temp_Import_ohne_Bezug.csv",
"relative_path": "Temp_Import_ohne_Bezug.csv",
"file_type": "csv",
"suggested_category": "",
"suggested_folder": "07_Sonstiges",
"suggested_new_name": "",
"action_type": "move_suggestion",
"reason": "Als temporäre Importdatei ohne Bezug eignet sich 07_Sonstiges.",
"erledigt": "False"
},
{
"original_name": "Testdatei_Leerstand.bin",
"relative_path": "Testdatei_Leerstand.bin",
"file_type": "bin",
"suggested_category": "",
"suggested_folder": "07_Sonstiges",
"suggested_new_name": "",
"action_type": "move_suggestion",
"reason": "Testdatei ohne fachliche Zuordnung passt in 07_Sonstiges.",
"erledigt": "False"
},
{
"original_name": "Unbenannte_Ablage_01.log",
"relative_path": "Unbenannte_Ablage_01.log",
"file_type": "log",
"suggested_category": "",
"suggested_folder": "07_Sonstiges",
"suggested_new_name": "",
"action_type": "move_suggestion",
"reason": "Unbenannte Ablagedatei ohne Kontext; Ablage in 07_Sonstiges naheliegend.",
"erledigt": "False"
},
{
"original_name": "Unklare_Sammlung.zip",
"relative_path": "Unklare_Sammlung.zip",
"file_type": "zip",
"suggested_category": "",
"suggested_folder": "07_Sonstiges",
"suggested_new_name": "",
"action_type": "move_suggestion",
"reason": "ZIP mit unklarem Inhalt; allgemeiner Ordner 07_Sonstiges vorhanden.",
"erledigt": "False"
},
{
"original_name": "USV.txt",
"relative_path": "USV.txt",
"file_type": "txt",
"suggested_category": "",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "unclear",
"reason": "„USV.txt“ im Root ohne eindeutige Zuordnung zu Doku oder Konfiguration.",
"erledigt": "False"
},
{
"original_name": "Zwischenablage_Unsortiert.tmp",
"relative_path": "Zwischenablage_Unsortiert.tmp",
"file_type": "tmp",
"suggested_category": "",
"suggested_folder": "07_Sonstiges",
"suggested_new_name": "",
"action_type": "move_suggestion",
"reason": "Temporäre Zwischenablage-Datei passt in 07_Sonstiges.",
"erledigt": "False"
},
{
"original_name": "bild1.png",
"relative_path": "01_Eingang\\bild1.png",
"file_type": "png",
"suggested_category": "Bild",
"suggested_folder": "05_Bilder",
"suggested_new_name": "",
"action_type": "move_suggestion",
"reason": "Bilddatei liegt im Eingangsordner; zentraler Bilder-Ordner ist 05_Bilder.",
"erledigt": "False"
},
{
"original_name": "code.txt",
"relative_path": "01_Eingang\\code.txt",
"file_type": "txt",
"suggested_category": "",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "unclear",
"reason": "Inhalt/Zweck von code.txt im Eingangsordner nicht erkennbar.",
"erledigt": "False"
},
{
"original_name": "datei_neu.pdf",
"relative_path": "01_Eingang\\datei_neu.pdf",
"file_type": "pdf",
"suggested_category": "",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "unclear",
"reason": "Allgemeiner Name ohne sicheren Hinweis auf Kategorie oder Zielordner.",
"erledigt": "False"
},
{
"original_name": "export.csv",
"relative_path": "01_Eingang\\export.csv",
"file_type": "csv",
"suggested_category": "Export",
"suggested_folder": "06_Exporte",
"suggested_new_name": "",
"action_type": "move_suggestion",
"reason": "CSV-Export im Eingangsordner; thematisch zu 06_Exporte passend.",
"erledigt": "False"
},
{
"original_name": "ohne_kontext.bin",
"relative_path": "01_Eingang\\ohne_kontext.bin",
"file_type": "bin",
"suggested_category": "",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "unclear",
"reason": "Binärdatei ohne Kontext im Eingangsordner; Zuordnung nicht sicher.",
"erledigt": "False"
},
{
"original_name": "scan_001.pdf",
"relative_path": "01_Eingang\\scan_001.pdf",
"file_type": "pdf",
"suggested_category": "",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "unclear",
"reason": "Gescanntes PDF ohne Hinweis, ob Rechnung, Vertrag oder Doku.",
"erledigt": "False"
},
{
"original_name": "ablage.tmp",
"relative_path": "07_Sonstiges\\ablage.tmp",
"file_type": "tmp",
"suggested_category": "",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Temporäre Datei befindet sich bereits im Sammelordner 07_Sonstiges.",
"erledigt": "False"
},
{
"original_name": "Unbekannte_Datei_001.dat",
"relative_path": "07_Sonstiges\\Unbekannte_Datei_001.dat",
"file_type": "dat",
"suggested_category": "",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Unklare DAT-Datei liegt bereits in 07_Sonstiges.",
"erledigt": "False"
},
{
"original_name": "vertrag_alt.pdf",
"relative_path": "07_Sonstiges\\vertrag_alt.pdf",
"file_type": "pdf",
"suggested_category": "Vertrag",
"suggested_folder": "02_Verträge",
"suggested_new_name": "",
"action_type": "move_suggestion",
"reason": "Dateiname deutet auf Vertrag; Zielbereich 02_Verträge vorhanden.",
"erledigt": "False"
},
{
"original_name": "bericht_neu.pdf",
"relative_path": "12_Berichte\\Monatsberichte\\bericht_neu.pdf",
"file_type": "pdf",
"suggested_category": "Bericht",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Liegt bereits unter 12_Berichte\\Monatsberichte.",
"erledigt": "False"
},
{
"original_name": "Monatsbericht_Mai_2026.pdf",
"relative_path": "12_Berichte\\Monatsberichte\\Monatsbericht_Mai_2026.pdf",
"file_type": "pdf",
"suggested_category": "Bericht",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Klarer Monatsbericht im passenden Berichte-Ordner.",
"erledigt": "False"
},
{
"original_name": "doku_neu.md",
"relative_path": "10_Archiv\\Altbestand\\doku_neu.md",
"file_type": "md",
"suggested_category": "Dokumentation",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Dokumentationsdatei befindet sich im Archiv-Altbestand.",
"erledigt": "False"
},
{
"original_name": "notiz_alt.txt",
"relative_path": "10_Archiv\\Altbestand\\notiz_alt.txt",
"file_type": "txt",
"suggested_category": "",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Alt-Notiz liegt bereits im Archiv-Altbestand.",
"erledigt": "False"
},
{
"original_name": "backup.json",
"relative_path": "09_Konfiguration\\Server\\backup.json",
"file_type": "json",
"suggested_category": "Konfiguration",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Backup unter 09_Konfiguration\\Server korrekt abgelegt.",
"erledigt": "False"
},
{
"original_name": "Konfiguration_Switch_EG-02_2026-06.json",
"relative_path": "09_Konfiguration\\Switches\\Konfiguration_Switch_EG-02_2026-06.json",
"file_type": "json",
"suggested_category": "Konfiguration",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Switch-Konfiguration im passenden Konfigurationsordner.",
"erledigt": "False"
},
{
"original_name": "switch_backup_neu.json",
"relative_path": "09_Konfiguration\\Switches\\switch_backup_neu.json",
"file_type": "json",
"suggested_category": "Konfiguration",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Switch-Backup liegt unter 09_Konfiguration\\Switches.",
"erledigt": "False"
},
{
"original_name": "Switch_EG-01_Konfiguration_2026-06.json",
"relative_path": "09_Konfiguration\\Switches\\Switch_EG-01_Konfiguration_2026-06.json",
"file_type": "json",
"suggested_category": "Konfiguration",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Switch-Konfigurationsdatei korrekt einsortiert.",
"erledigt": "False"
},
{
"original_name": "PowerShell_Benutzeranlage.ps1",
"relative_path": "08_Quellcode\\PowerShell\\PowerShell_Benutzeranlage.ps1",
"file_type": "ps1",
"suggested_category": "Quellcode",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "PowerShell-Skript im Quellcode-PowerShell Ordner.",
"erledigt": "False"
},
{
"original_name": "user_script_final.ps1",
"relative_path": "08_Quellcode\\PowerShell\\user_script_final.ps1",
"file_type": "ps1",
"suggested_category": "Quellcode",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "PowerShell-Skript liegt korrekt unter 08_Quellcode\\PowerShell.",
"erledigt": "False"
},
{
"original_name": "Auswertung_Ticketsystem.py",
"relative_path": "08_Quellcode\\Python\\Auswertung_Ticketsystem.py",
"file_type": "py",
"suggested_category": "Quellcode",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Python-Skript im Quellcode-Python Ordner.",
"erledigt": "False"
},
{
"original_name": "script_alt.py",
"relative_path": "08_Quellcode\\Python\\script_alt.py",
"file_type": "py",
"suggested_category": "Quellcode",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Python-Skript korrekt in 08_Quellcode\\Python.",
"erledigt": "False"
},
{
"original_name": "test.py",
"relative_path": "08_Quellcode\\Python\\test.py",
"file_type": "py",
"suggested_category": "Quellcode",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Testsript befindet sich im Quellcode-Ordner.",
"erledigt": "False"
},
{
"original_name": "export_alt.csv",
"relative_path": "06_Exporte\\Ticketsystem\\export_alt.csv",
"file_type": "csv",
"suggested_category": "Export",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "CSV-Export korrekt im Exporte-Unterordner.",
"erledigt": "False"
},
{
"original_name": "Export_Ticketsystem_Juni_2026.csv",
"relative_path": "06_Exporte\\Ticketsystem\\Export_Ticketsystem_Juni_2026.csv",
"file_type": "csv",
"suggested_category": "Export",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Ticketsystem-Export im passenden Ordner.",
"erledigt": "False"
},
{
"original_name": "Export_Ticketsystem_Mai_2026.csv",
"relative_path": "06_Exporte\\Ticketsystem\\Export_Ticketsystem_Mai_2026.csv",
"file_type": "csv",
"suggested_category": "Export",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "CSV-Export liegt bereits unter 06_Exporte\\Ticketsystem.",
"erledigt": "False"
},
{
"original_name": "Baustellenfoto_Edewecht_2026-06-04.jpg",
"relative_path": "05_Bilder\\Baustellen\\Baustellenfoto_Edewecht_2026-06-04.jpg",
"file_type": "jpg",
"suggested_category": "Bild",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Baustellenfoto korrekt im Bilder-Baustellen Ordner.",
"erledigt": "False"
},
{
"original_name": "IMG_4421.jpg",
"relative_path": "05_Bilder\\Baustellen\\IMG_4421.jpg",
"file_type": "jpg",
"suggested_category": "Bild",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Bilddatei korrekt im Bilder-Baustellen Verzeichnis.",
"erledigt": "False"
},
{
"original_name": "Screenshot_Fehler_Anmeldung_2026-06-03.png",
"relative_path": "05_Bilder\\Screenshots\\Screenshot_Fehler_Anmeldung_2026-06-03.png",
"file_type": "png",
"suggested_category": "Bild",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Screenshot ist bereits unter Bilder\\Screenshots abgelegt.",
"erledigt": "False"
},
{
"original_name": "Screenshot_VPN_Fehler_2026-06-05.png",
"relative_path": "05_Bilder\\Screenshots\\Screenshot_VPN_Fehler_2026-06-05.png",
"file_type": "png",
"suggested_category": "Bild",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Screenshot im richtigen Screenshots-Ordner.",
"erledigt": "False"
},
{
"original_name": "handbuch_neu.docx",
"relative_path": "04_Dokumentation\\Handbücher\\handbuch_neu.docx",
"file_type": "docx",
"suggested_category": "Dokumentation",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Handbuch im passenden Dokumentationsordner.",
"erledigt": "False"
},
{
"original_name": "Handbuch_Zeiterfassung_V2.docx",
"relative_path": "04_Dokumentation\\Handbücher\\Handbuch_Zeiterfassung_V2.docx",
"file_type": "docx",
"suggested_category": "Dokumentation",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Handbuch liegt korrekt unter 04_Dokumentation\\Handbücher.",
"erledigt": "False"
},
{
"original_name": "doku_final_final.md",
"relative_path": "04_Dokumentation\\Projektunterlagen\\doku_final_final.md",
"file_type": "md",
"suggested_category": "Dokumentation",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Dokumentation in 04_Dokumentation\\Projektunterlagen ist passend.",
"erledigt": "False"
},
{
"original_name": "Projektbericht_Zugangsbeschränkung_Juni_2026.pdf",
"relative_path": "04_Dokumentation\\Projektunterlagen\\Projektbericht_Zugangsbeschränkung_Juni_2026.pdf",
"file_type": "pdf",
"suggested_category": "Dokumentation",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Projektbericht ist im Ordner Projektunterlagen abgelegt.",
"erledigt": "False"
},
{
"original_name": "Projektdokumentation_Zugangsbeschränkung_2026.md",
"relative_path": "04_Dokumentation\\Projektunterlagen\\Projektdokumentation_Zugangsbeschränkung_2026.md",
"file_type": "md",
"suggested_category": "Dokumentation",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Projektdokumentation liegt korrekt in 04_Dokumentation\\Projektunterlagen.",
"erledigt": "False"
},
{
"original_name": "Rechnung_Bueromaterial_Mai_2026.pdf",
"relative_path": "03_Rechnungen\\2026\\Rechnung_Bueromaterial_Mai_2026.pdf",
"file_type": "pdf",
"suggested_category": "Rechnung",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Rechnung liegt im Jahresordner 2026.",
"erledigt": "False"
},
{
"original_name": "Rechnung_Stadtwerke_Mai_2026.pdf",
"relative_path": "03_Rechnungen\\2026\\Rechnung_Stadtwerke_Mai_2026.pdf",
"file_type": "pdf",
"suggested_category": "Rechnung",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Rechnung im korrekten Rechnungen-Ordner für 2026.",
"erledigt": "False"
},
{
"original_name": "rechnung_strom_mai.pdf",
"relative_path": "03_Rechnungen\\2026\\rechnung_strom_mai.pdf",
"file_type": "pdf",
"suggested_category": "Rechnung",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Rechnung liegt bereits im passenden Jahresunterordner.",
"erledigt": "False"
},
{
"original_name": "Rechnung_Telekom_April_2026.pdf",
"relative_path": "03_Rechnungen\\2026\\Rechnung_Telekom_April_2026.pdf",
"file_type": "pdf",
"suggested_category": "Rechnung",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Telekom-Rechnung im Ordner 03_Rechnungen\\2026.",
"erledigt": "False"
},
{
"original_name": "Rechnung_Telekom_Juni_2026.pdf",
"relative_path": "03_Rechnungen\\2026\\Rechnung_Telekom_Juni_2026.pdf",
"file_type": "pdf",
"suggested_category": "Rechnung",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Telekom-Rechnung korrekt einsortiert.",
"erledigt": "False"
},
{
"original_name": "telekom_final_neu.pdf",
"relative_path": "03_Rechnungen\\2026\\telekom_final_neu.pdf",
"file_type": "pdf",
"suggested_category": "Rechnung",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "PDF im Rechnungen-Jahresordner 2026; genaue Umbenennung nicht sicher.",
"erledigt": "False"
},
{
"original_name": "rechnung_scan.pdf",
"relative_path": "03_Rechnungen\\Unsortiert\\rechnung_scan.pdf",
"file_type": "pdf",
"suggested_category": "Rechnung",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Liegt in 03_Rechnungen\\Unsortiert; Zieljahr/-ordner nicht sicher ableitbar.",
"erledigt": "False"
},
{
"original_name": "Lieferantenvertrag_Büromaterial_2026.pdf",
"relative_path": "02_Verträge\\Lieferanten\\Lieferantenvertrag_Büromaterial_2026.pdf",
"file_type": "pdf",
"suggested_category": "Vertrag",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Lieferantenvertrag korrekt unter 02_Verträge\\Lieferanten.",
"erledigt": "False"
},
{
"original_name": "Lieferantenvertrag_Netzwerkhaus_2026.pdf",
"relative_path": "02_Verträge\\Lieferanten\\Lieferantenvertrag_Netzwerkhaus_2026.pdf",
"file_type": "pdf",
"suggested_category": "Vertrag",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Liegt im passenden Lieferantenvertragsordner.",
"erledigt": "False"
},
{
"original_name": "vertrag_drucker_scan.pdf",
"relative_path": "02_Verträge\\Wartung\\vertrag_drucker_scan.pdf",
"file_type": "pdf",
"suggested_category": "Vertrag",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Vertrag im Ordner 02_Verträge\\Wartung korrekt abgelegt.",
"erledigt": "False"
},
{
"original_name": "Wartungsvertrag_Drucker_2026.pdf",
"relative_path": "02_Verträge\\Wartung\\Wartungsvertrag_Drucker_2026.pdf",
"file_type": "pdf",
"suggested_category": "Vertrag",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Wartungsvertrag korrekt unter Verträge\\Wartung.",
"erledigt": "False"
},
{
"original_name": "Wartungsvertrag_HASKAMP_IT_2026.pdf",
"relative_path": "02_Verträge\\Wartung\\Wartungsvertrag_HASKAMP_IT_2026.pdf",
"file_type": "pdf",
"suggested_category": "Vertrag",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "keep",
"reason": "Wartungsvertrag im passenden Ordner 02_Verträge\\Wartung.",
"erledigt": "False"
}
]
}

    return json.dumps(test_inhalt, ensure_ascii=False, indent=2)
    