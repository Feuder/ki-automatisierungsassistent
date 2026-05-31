# Prompt: Technischen Ordnerbericht zusammenfassen

## Ziel

Du erhältst einen technischen Ordnerbericht mit Informationen über Dateien, Dateitypen, Dateigrößen und gegebenenfalls Ordnerstruktur.

Erstelle daraus einen verständlichen Markdown-Bericht.

Der Bericht soll den Inhalt des Ordners zusammenfassen, mögliche Auffälligkeiten nennen und sinnvolle allgemeine Empfehlungen geben.

## Wichtige Regeln

* Verwende ausschließlich Informationen aus dem übergebenen Ordnerbericht.
* Erfinde keine Dateien.
* Erfinde keine Inhalte, die nicht aus dem Bericht ableitbar sind.
* Wenn der Zweck des Ordners nicht sicher erkennbar ist, sage das klar.
* Spekuliere nicht über Dateiinhalte.
* Bewerte nur Dateinamen, Dateitypen, Größen und Ordnerstruktur.
* Führe keine Dateiaktionen aus.
* Schlage keine konkrete automatische Umsetzung vor.
* Gib keinen JSON-Text aus.
* Gib keinen Markdown-Codeblock aus.
* Die Ausgabe soll ein normaler Markdown-Bericht sein.
* Schreibe klar, sachlich und gut verständlich.

## Erforderliche Abschnittsstruktur

Gib genau die folgenden Abschnitte in dieser Reihenfolge aus:

# Ordnerbericht

## 1. Zusammenfassung

Fasse kurz zusammen, was im Ordner erkennbar ist.

Nenne dabei, falls vorhanden:

* Anzahl der Dateien
* erkennbare Dateitypen
* auffällige Häufungen bestimmter Dateitypen
* erkennbare Strukturmerkmale

## 2. Zweck des Ordners

Erkläre, wofür der Ordner wahrscheinlich genutzt wird.

Wenn der Zweck nicht sicher aus dem Bericht ableitbar ist, schreibe ausdrücklich:

Der Zweck des Ordners ist anhand der vorhandenen Metadaten nicht eindeutig bestimmbar.

## 3. Auffälligkeiten

Nenne erkennbare Auffälligkeiten, zum Beispiel:

* viele Dateien eines Typs
* unklare Dateinamen
* fehlende Dateiendungen
* sehr große Dateien
* uneinheitliche Struktur
* mögliche Vermischung verschiedener Dateikategorien

Wenn keine Auffälligkeiten erkennbar sind, schreibe:

Es sind anhand der vorhandenen Metadaten keine klaren Auffälligkeiten erkennbar.

## 4. Allgemeine Sortierempfehlung

Beschreibe allgemein, wie der Ordner sinnvoller strukturiert werden könnte.

Wichtig:

* Gib nur allgemeine Empfehlungen.
* Gib keine verbindlichen Dateiaktionen aus.
* Nenne keine automatische Ausführung.
* Schlage keine Löschung vor.
* Schlage keine echten Verschiebe- oder Umbenennungsaktionen als ausgeführte Schritte vor.

## 5. Empfohlene nächste Prüfschritte

Formuliere kurze, konkrete Prüfschritte für den Nutzer.

Jeder Punkt soll als nummerierte Liste ausgegeben werden.

Beispiel:

1. Prüfen, ob die Dateinamen eindeutig genug sind.
2. Prüfen, ob Dateien nach Typ oder Thema getrennt werden sollten.
3. Prüfen, ob sehr große Dateien separat betrachtet werden müssen.

## 6. Mögliche Zielstruktur

Erstelle eine einfache visuelle Ordnerstruktur als Vorschlag.

Wichtig:

* Zeige nur mögliche Ordner.
* Zeige keine einzelnen Dateien.
* Führe keine Aktionen aus.
* Wenn keine sinnvolle Struktur ableitbar ist, schreibe:

Eine belastbare Zielstruktur ist anhand der vorhandenen Metadaten nicht sicher ableitbar.

## Ausgabeformat

Gib ausschließlich den Markdown-Bericht aus.

Keine Erklärung vor dem Bericht.
Keine Erklärung nach dem Bericht.
Kein JSON.
Kein Markdown-Codeblock.
