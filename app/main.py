from pathlib import Path

pfad = Path("data/input/")

if not pfad.is_dir():
    print("Der Zielpfad existiert nicht oder ist kein Ordner.")
    raise SystemExit

dateien = [f for f in Path(pfad).iterdir() if f.is_file()]
bericht = []

bericht.append(f"Analysierter Pfad: {pfad}")
bericht.append(f"Anzahl der Dateien: {len(dateien)}")


if dateien:
    for f in dateien:
        if f.suffix:
            bericht.append(f"{f.name} | {f.suffix} | {f.stat().st_size} Bytes")
        else:
            bericht.append(f"{f.name} | Keine Endung | {f.stat().st_size} Bytes")
else:
    bericht.append("Es wurden keine Dateien gefunden.")

for b in bericht:
    print(b)