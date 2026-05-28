# Prompt: Dateivorschläge aus technischem Ordnerbericht erstellen

## Ziel

Analysiere einen technischen Ordnerbericht und erstelle konkrete Vorschläge zur Sortierung, Umbenennung oder Beibehaltung der Dateien.
Die Ausgabe dient zur weiteren automatisierten Verarbeitung. Deshalb muss ausschließlich gültiges JSON im vorgegebenen Format ausgegeben werden.

## Aufgabe

Erstelle für jede erkennbare Datei aus dem Ordnerbericht genau einen Dateivorschlag.

Ein Dateivorschlag beschreibt, ob die Datei:

* unverändert bleiben soll
* in einen anderen Ordner verschoben werden soll
* Ein neuer Ordner erstellt werden soll, in den dann Dateien verschoben werden sollen
* umbenannt werden soll
* umbenannt und verschoben werden soll
* nicht zuverlässig bewertet werden kann

## Regeln

* Verwende ausschließlich Informationen aus dem übergebenen Ordnerbericht.
* Erfinde keine Dateien.
* Erfinde keine Inhalte, die nicht aus dem Bericht ableitbar sind.
* Wenn der Zweck einer Datei oder eines Ordners nicht sicher erkennbar ist, verwende `unclear`.
* Gib keine Erklärungen außerhalb des JSON aus.
* Gib keinen Markdown-Codeblock aus.
* Gib ausschließlich gültiges JSON aus.
* Alle Textwerte müssen UTF-8-kompatibel sein.
* Verwende exakt die vorgegebenen Feldnamen.
* Verwende keine zusätzlichen Felder.
* Jeder Eintrag muss alle Pflichtfelder enthalten.
* Jeder Wert muss als String ausgegeben werden.

## Erlaubte Werte für `action_type`

Verwende ausschließlich einen dieser Werte:

* `keep`
* `move_suggestion`
* `rename_suggestion`
* `rename_and_move_suggestion`
* `unclear`

## Bedeutung von `action_type`

### `keep`

Die Datei soll unverändert bleiben.

Verwende diesen Wert, wenn Name und Speicherort sinnvoll wirken.

### `move_suggestion`

Die Datei soll in einen anderen Ordner verschoben werden, aber der Dateiname bleibt gleich.

### `rename_suggestion`

Die Datei soll umbenannt werden, aber im gleichen Ordner bleiben.

### `rename_and_move_suggestion`

Die Datei soll umbenannt und zusätzlich in einen anderen Ordner verschoben werden.

### `unclear`

Es ist nicht zuverlässig ableitbar, was mit der Datei passieren soll.

## Feldbeschreibung

### `original_name`

Der ursprüngliche Dateiname aus dem Bericht.

### `relative_path`

Der relative Pfad der Datei aus dem Bericht.

### `file_type`

Der Dateityp oder die Dateiendung.

Beispiele:

* `pdf`
* `docx`
* `xlsx`
* `txt`
* `png`
* `unknown`

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
* `Unklar`

### `suggested_folder`

Der vorgeschlagene Zielordner als relativer Ordnerpfad.
Es dürfen neue Ordner vorgeschlagen werden
Wenn keine Verschiebung vorgeschlagen wird, verwende den bisherigen Ordner.
Wenn der Zielordner nicht sicher bestimmbar ist, verwende `Unklar`.

### `suggested_new_name`

Der vorgeschlagene neue Dateiname.
Wenn keine Umbenennung vorgeschlagen wird, verwende den ursprünglichen Dateinamen.
Wenn kein sinnvoller neuer Name ableitbar ist, verwende den ursprünglichen Dateinamen.

### `action_type`

Die vorgeschlagene Aktion für die Datei.
Erlaubt sind ausschließlich:

* `keep`
* `move_suggestion`
* `rename_suggestion`
* `rename_and_move_suggestion`
* `unclear`

### `reason`

Kurze sachliche Begründung für den Vorschlag.
Die Begründung muss sich auf den Ordnerbericht stützen.

## Ausgabeformat

Die Ausgabe muss exakt dieses JSON-Objekt sein:

```json
{
  "datei_vorschläge": [
    {
      "original_name": "...",
      "relative_path": "...",
      "file_type": "...",
      "suggested_category": "...",
      "suggested_folder": "...",
      "suggested_new_name": "...",
      "action_type": "...",
      "reason": "..."
    }
  ]
}
```
