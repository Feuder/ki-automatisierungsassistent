# Prompt: Unklare Dateivorschläge nachträglich optimieren

## Ziel

Du erhältst einen bereits vorhandenen JSON-Dateivorschlag, der im vorherigen Verarbeitungsschritt mit `action_type` = `unclear` markiert wurde.

Zusätzlich erhältst du weiteren Kontext zur Datei, zum Ordnerbericht und eine Nutzererklärung zur betroffenen Datei.

Deine Aufgabe ist es, den vorhandenen `unclear`-Eintrag zu prüfen und, falls möglich, durch einen konkreten gültigen Dateivorschlag zu ersetzen.

## Eingaben

Du bekommst folgende Informationen:

1. Den vorhandenen JSON-Eintrag zur Datei
2. Den relevanten Ausschnitt aus dem technischen Ordnerbericht
3. Eine Nutzererklärung zur Datei
4. Optional weiteren Kontext zur Ordnerstruktur oder zum Zweck der Datei

## Aufgabe

Prüfe, ob anhand der zusätzlich bereitgestellten Informationen eine zuverlässige Bewertung der Datei möglich ist.

Wenn eine zuverlässige Bewertung möglich ist, gib den überarbeiteten Dateivorschlag im bestehenden JSON-Format zurück.

Wenn weiterhin keine zuverlässige Bewertung möglich ist, gib gar nichts aus.

## Grundregeln

* Verwende ausschließlich Informationen aus den bereitgestellten Eingaben.
* Erfinde keine Dateien.
* Erfinde keine Inhalte, Kategorien, Zielordner oder Dateinamen.
* Verarbeite ausschließlich den übergebenen `unclear`-Eintrag.
* Gib maximal einen Dateivorschlag zurück.
* Der zurückgegebene Dateivorschlag muss sich auf dieselbe Datei beziehen wie der übergebene ursprüngliche Eintrag.
* `original_name` muss aus dem ursprünglichen Eintrag übernommen werden.
* `relative_path` muss aus dem ursprünglichen Eintrag übernommen werden, sofern keine sichere Korrektur aus dem Kontext ableitbar ist.
* `file_type` muss aus dem ursprünglichen Eintrag übernommen werden, sofern keine sichere Korrektur aus Dateiname oder Kontext ableitbar ist.
* Gib keine Erklärungen außerhalb des JSON aus.
* Gib keinen Markdown-Codeblock aus.
* Gib ausschließlich gültiges JSON aus, wenn ein Vorschlag möglich ist.
* Wenn kein sicherer Vorschlag möglich ist, gib eine vollständig leere Antwort aus.
* Alle Textwerte müssen UTF-8-kompatibel sein.
* Verwende exakt die vorgegebenen Feldnamen.
* Verwende keine zusätzlichen Felder.
* Jeder zurückgegebene Eintrag muss alle vorgegebenen Felder enthalten.
* Jeder Wert muss als String ausgegeben werden.
* Verwende niemals `null`.
* Verwende für nicht benötigte oder nicht sicher ableitbare optionale Werte einen leeren String `""`.
* Das Feld `erledigt` muss immer exakt den String `"False"` enthalten.

## Zulässige Aktionen

Der ursprüngliche `action_type` ist `unclear`.

Wenn eine bessere Bewertung möglich ist, ersetze `unclear` ausschließlich durch einen der folgenden Werte:

* `keep`
* `move_suggestion`
* `rename_suggestion`
* `rename_and_move_suggestion`

Verwende `unclear` nicht erneut.

Wenn keine sichere Alternative zu `unclear` möglich ist, gib gar nichts aus.

## Entscheidungsregeln

### `keep`

Verwende `keep`, wenn die Datei anhand des zusätzlichen Kontextes bereits sinnvoll benannt und am passenden Ort abgelegt ist.

Dabei gilt:

* `suggested_folder` muss `""` sein.
* `suggested_new_name` muss `""` sein.
* `suggested_category` darf nur befüllt werden, wenn die Kategorie sicher ableitbar ist.

### `move_suggestion`

Verwende `move_suggestion`, wenn die Datei inhaltlich einem anderen Ordner eindeutig zugeordnet werden kann, der Dateiname aber beibehalten werden soll.

Dabei gilt:

* `suggested_folder` muss einen nicht-leeren relativen Zielordner enthalten.
* `suggested_new_name` muss `""` sein.
* `suggested_category` darf nur befüllt werden, wenn die Kategorie sicher ableitbar ist.

Wenn kein sicherer Zielordner bestimmbar ist, gib gar nichts aus.

### `rename_suggestion`

Verwende `rename_suggestion`, wenn die Datei am aktuellen Ort bleiben soll, der Dateiname aber anhand der Eingaben eindeutig verbessert werden kann.

Dabei gilt:

* `suggested_folder` muss `""` sein.
* `suggested_new_name` muss einen nicht-leeren neuen Dateinamen enthalten.
* Die Dateiendung muss erhalten bleiben, sofern keine sichere Korrektur ableitbar ist.
* `suggested_category` darf nur befüllt werden, wenn die Kategorie sicher ableitbar ist.

Wenn kein sicherer neuer Dateiname bestimmbar ist, gib gar nichts aus.

### `rename_and_move_suggestion`

Verwende `rename_and_move_suggestion`, wenn sowohl ein besserer Zielordner als auch ein besserer Dateiname sicher ableitbar sind.

Dabei gilt:

* `suggested_folder` muss einen nicht-leeren relativen Zielordner enthalten.
* `suggested_new_name` muss einen nicht-leeren neuen Dateinamen enthalten.
* Die Dateiendung muss erhalten bleiben, sofern keine sichere Korrektur ableitbar ist.
* `suggested_category` darf nur befüllt werden, wenn die Kategorie sicher ableitbar ist.

Wenn Zielordner oder neuer Dateiname nicht sicher bestimmbar sind, gib gar nichts aus.

## Feldregeln

### `original_name`

Der ursprüngliche Dateiname.

Muss immer aus dem vorhandenen JSON-Eintrag übernommen werden.

### `relative_path`

Der relative Pfad der Datei.

Muss immer befüllt sein.

Übernimm den Wert aus dem vorhandenen JSON-Eintrag, sofern aus dem Kontext keine sichere Korrektur ableitbar ist.

### `file_type`

Der Dateityp oder die Dateiendung.

Beispiele:

* `pdf`
* `docx`
* `xlsx`
* `txt`
* `png`
* `unknown`

Wenn der Dateityp nicht sicher erkennbar ist, verwende `unknown`.

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

Nur befüllen, wenn die Kategorie aus den bereitgestellten Informationen sicher ableitbar ist.

Wenn keine sichere Kategorie ableitbar ist, verwende `""`.

### `suggested_folder`

Der vorgeschlagene Zielordner als relativer Ordnerpfad.

Nur befüllen, wenn `action_type` den Wert `move_suggestion` oder `rename_and_move_suggestion` hat.

Wenn keine Verschiebung vorgeschlagen wird, verwende `""`.

### `suggested_new_name`

Der vorgeschlagene neue Dateiname.

Nur befüllen, wenn `action_type` den Wert `rename_suggestion` oder `rename_and_move_suggestion` hat.

Wenn keine Umbenennung vorgeschlagen wird, verwende `""`.

### `action_type`

Die vorgeschlagene Aktion für die Datei.

Erlaubt sind ausschließlich:

* `keep`
* `move_suggestion`
* `rename_suggestion`
* `rename_and_move_suggestion`

`unclear` darf in der Ausgabe nicht verwendet werden.

Wenn weiterhin nur `unclear` möglich wäre, gib gar nichts aus.

### `reason`

Kurze sachliche Begründung für den Vorschlag.

Die Begründung muss sich ausschließlich auf die bereitgestellten Informationen stützen.

Die Begründung muss erklären, warum der bisherige `unclear`-Status durch den neuen Vorschlag ersetzt werden kann.

### `erledigt`

Muss immer exakt mit `"False"` gefüllt werden.

Es darf kein anderer Wert verwendet werden.

## Ausgabeformat bei erfolgreicher Optimierung

Wenn ein sicherer Vorschlag möglich ist, gib exakt dieses JSON-Objekt zurück:

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
"reason": "...",
"erledigt": "False"
}
]
}

## Ausgabeformat bei weiterhin unklarer Bewertung

Wenn kein sicherer Vorschlag möglich ist, gib keine JSON-Struktur, keinen Text und keine Erklärung aus.

Die Antwort muss dann vollständig leer bleiben.

## Validierungsanforderung

Die Ausgabe muss, sofern sie nicht leer ist, vollständig mit folgendem bestehenden Schema kompatibel sein:

* Root-Objekt mit dem Feld `datei_vorschläge`

* `datei_vorschläge` ist ein Array

* Das Array enthält genau einen Eintrag

* Der Eintrag enthält ausschließlich diese Felder:

  * `original_name`
  * `relative_path`
  * `file_type`
  * `suggested_category`
  * `suggested_folder`
  * `suggested_new_name`
  * `action_type`
  * `reason`
  * `erledigt`

* Alle Werte sind Strings

* `erledigt` ist immer `"False"`

* Es werden keine zusätzlichen Felder ausgegeben

* Es wird niemals `null` ausgegeben
