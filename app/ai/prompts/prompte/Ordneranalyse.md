# Prompt: Dateivorschläge aus technischem Ordnerbericht erstellen

## Ziel

Analysiere einen technischen Ordnerbericht und erstelle konkrete Vorschläge zur Sortierung, Umbenennung oder Beibehaltung der Dateien.

Die Ausgabe dient zur weiteren automatisierten Verarbeitung. Deshalb muss ausschließlich gültiges JSON im vorgegebenen Format ausgegeben werden.

## Aufgabe

Erstelle für jede erkennbare Datei aus dem Ordnerbericht genau einen Dateivorschlag.

Ein Dateivorschlag beschreibt, ob die Datei:

* unverändert bleiben soll
* in einen anderen Ordner verschoben werden soll
* umbenannt werden soll
* umbenannt und verschoben werden soll
* nicht zuverlässig bewertet werden kann

## Grundregeln

* Verwende ausschließlich Informationen aus dem übergebenen Ordnerbericht.
* Erfinde keine Dateien.
* Erfinde keine Inhalte, die nicht aus dem Bericht ableitbar sind.
* Jede Datei aus dem Ordnerbericht muss genau einmal verarbeitet werden.
* Es darf keine Datei ausgelassen werden.
* Wenn der Zweck einer Datei oder eines Ordners nicht sicher erkennbar ist, verwende `unclear`.
* Gib keine Erklärungen außerhalb des JSON aus.
* Gib keinen Markdown-Codeblock aus.
* Gib ausschließlich gültiges JSON aus.
* Alle Textwerte müssen UTF-8-kompatibel sein.
* Verwende exakt die vorgegebenen Feldnamen.
* Verwende keine zusätzlichen Felder.
* Jeder Eintrag muss alle vorgegebenen Felder enthalten.
* Jeder Wert muss als String ausgegeben werden.
* Verwende für nicht benötigte oder nicht sicher ableitbare optionale Werte einen leeren String `""`.
* Verwende niemals `null`.

## Pflichtwerte

Die folgenden Felder müssen bei jeder Datei immer einen nicht-leeren String enthalten:

* `original_name`
* `relative_path`
* `file_type`
* `action_type`
* `reason`

Die folgenden Felder dürfen leer sein, wenn sie für die vorgeschlagene Aktion nicht benötigt werden oder nicht sicher ableitbar sind:

* `suggested_category`
* `suggested_folder`
* `suggested_new_name`

## Bedingte Pflichtwerte

Je nach `action_type` gelten zusätzliche Regeln:

### `keep`

Die Datei soll unverändert bleiben.

Pflichtwerte:

* `original_name`
* `relative_path`
* `file_type`
* `action_type`
* `reason`

Optionale Felder:

* `suggested_category`: nur befüllen, wenn die Kategorie sicher aus dem Bericht ableitbar ist, sonst `""`
* `suggested_folder`: `""`
* `suggested_new_name`: `""`

### `move_suggestion`

Die Datei soll in einen anderen Ordner verschoben werden, aber der Dateiname bleibt gleich.

Zusätzlich verpflichtend:

* `suggested_folder`

Nicht benötigte Felder:

* `suggested_new_name`: `""`

`suggested_category` nur befüllen, wenn die Kategorie sicher aus dem Bericht ableitbar ist, sonst `""`.

### `rename_suggestion`

Die Datei soll umbenannt werden, aber im gleichen Ordner bleiben.

Zusätzlich verpflichtend:

* `suggested_new_name`

Nicht benötigte Felder:

* `suggested_folder`: `""`

`suggested_category` nur befüllen, wenn die Kategorie sicher aus dem Bericht ableitbar ist, sonst `""`.

### `rename_and_move_suggestion`

Die Datei soll umbenannt und zusätzlich in einen anderen Ordner verschoben werden.

Zusätzlich verpflichtend:

* `suggested_folder`
* `suggested_new_name`

`suggested_category` nur befüllen, wenn die Kategorie sicher aus dem Bericht ableitbar ist, sonst `""`.

### `unclear`

Die Datei kann nicht zuverlässig bewertet werden.

Pflichtwerte:

* `original_name`
* `relative_path`
* `file_type`
* `action_type`
* `reason`

Nicht sicher ableitbare Felder müssen leer bleiben:

* `suggested_category`: `""`
* `suggested_folder`: `""`
* `suggested_new_name`: `""`

## Erlaubte Werte für `action_type`

Verwende ausschließlich einen dieser Werte:

* `keep`
* `move_suggestion`
* `rename_suggestion`
* `rename_and_move_suggestion`
* `unclear`

## Feldbeschreibung

### `original_name`

Der ursprüngliche Dateiname aus dem Bericht.

Muss immer befüllt sein.

### `relative_path`

Der relative Pfad der Datei aus dem Bericht.

Muss immer befüllt sein.

### `file_type`

Der Dateityp oder die Dateiendung.

Beispiele:

* `pdf`
* `docx`
* `xlsx`
* `txt`
* `png`
* `unknown`

Muss immer befüllt sein.

Wenn der Dateityp nicht erkennbar ist, verwende `unknown`.

### `suggested_category`

Die vorgeschlagene fachliche Kategorie der Datei.

Beispiele:

* `Dokumentation`
* `Vertrag`
* `Rechnung`
* `Bild`
* `Export`
* `Quellcode`
* `Konfiguration`

Nur befüllen, wenn die Kategorie sicher aus dem Ordnerbericht ableitbar ist.

Wenn keine sichere Kategorie ableitbar ist, verwende `""`.

### `suggested_folder`

Der vorgeschlagene Zielordner als relativer Ordnerpfad.

Es dürfen neue Ordner vorgeschlagen werden.

Nur befüllen, wenn `action_type` den Wert `move_suggestion` oder `rename_and_move_suggestion` hat.

Wenn keine Verschiebung vorgeschlagen wird, verwende `""`.

Wenn ein Zielordner nicht sicher bestimmbar ist, darf keine Verschiebung vorgeschlagen werden. Verwende dann stattdessen `unclear`.

### `suggested_new_name`

Der vorgeschlagene neue Dateiname.

Nur befüllen, wenn `action_type` den Wert `rename_suggestion` oder `rename_and_move_suggestion` hat.

Wenn keine Umbenennung vorgeschlagen wird, verwende `""`.

Wenn kein sinnvoller neuer Name sicher ableitbar ist, darf keine Umbenennung vorgeschlagen werden. Verwende dann stattdessen `unclear`.

### `action_type`

Die vorgeschlagene Aktion für die Datei.

Erlaubt sind ausschließlich:

* `keep`
* `move_suggestion`
* `rename_suggestion`
* `rename_and_move_suggestion`
* `unclear`

Muss immer befüllt sein.

### `reason`

Kurze sachliche Begründung für den Vorschlag.

Die Begründung muss sich ausschließlich auf den Ordnerbericht stützen.

Muss immer befüllt sein.

## Ausgabeformat

Die Ausgabe muss exakt dieses JSON-Objekt sein:

{
"datei_vorschläge": [
{
"original_name": "...",
"relative_path": "...",
"file_type": "...",
"suggested_category": "",
"suggested_folder": "",
"suggested_new_name": "",
"action_type": "...",
"reason": "..."
}
]
}
