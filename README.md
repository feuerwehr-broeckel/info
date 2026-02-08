# Feuerwehr Bröckel - Dokumentation

Dokumentation für die Feuerwehr Bröckel, erstellt mit [Zensical](https://github.com/zensical/zensical).

## Voraussetzungen

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (Python package manager)

## Installation

```bash
# Repository klonen
git clone <repository-url>
cd info

# Abhängigkeiten installieren
uv sync

# Playwright Browser installieren (einmalig)
uv run playwright install chromium
```

## Dokumentation lokal anzeigen

```bash
uv run zensical serve
```

Die Dokumentation ist dann unter http://localhost:8000 erreichbar.

## Screenshot-Generierung

### FeuerON Screenshots

Die Screenshots für die FeuerON-Dokumentation werden automatisch mit Playwright erstellt.

#### Umgebungsvariablen setzen

```bash
export FEUERON_USERNAME='dein_benutzername'
export FEUERON_PASSWORD='dein_passwort'
export FEUERON_REGION_ID='156'  # Optional, Standard ist 156
```

#### Screenshots erstellen

```bash
# Alle Screenshots erstellen, annotieren und rahmen
uv run info screenshots generate

# Nur Screenshots erstellen
uv run info screenshots capture

# Nur Annotationen auf bestehende Screenshots anwenden
uv run info screenshots annotate

# Nur Browser-Rahmen anwenden
uv run info screenshots frame
```

Die Screenshots werden in `docs/assets/feueron/screenshots/raw/` gespeichert, annotierte Versionen in `docs/assets/feueron/screenshots/annotated/`, gerahmte Versionen in `docs/assets/feueron/screenshots/framed/`.

## Datenmigration (Fox112 → FeuerON)

### Adressen abgleichen

Erstellt eine FeuerON-kompatible CSV-Datei, die Adressen aus einem Fox112-Excel-Export aktualisiert:

```bash
uv run info migration address-check Fox_Rahmen_XLS.php-5.xlsx Adressenliste.csv -o adressen_update.csv
```

### Annotationen bearbeiten

Die Annotationen (Markierungen auf Screenshots) werden in `scripts/feueron/annotations.py` definiert.

Beispiel:

```python
from tools.annotation import Marker

ANNOTATIONS = {
    "01_feueron_homepage.png": [
        (
            "_login_highlighted",  # Suffix für die Ausgabedatei
            [
                Marker.rectangle(
                    x=100, y=200, width=400, height=300,
                    label="1",
                    border_color="#ff0000",
                    radius=8,
                ),
                Marker.circle(
                    x=500, y=150, diameter=50,
                    label="2",
                    border_color="#00ff00",
                ),
            ],
        ),
    ],
}
```

#### Marker-Optionen

| Option | Typ | Standard | Beschreibung |
|--------|-----|----------|--------------|
| `x` | int | erforderlich | X-Koordinate (Rechteck: oben-links, Kreis: Mittelpunkt) |
| `y` | int | erforderlich | Y-Koordinate (Rechteck: oben-links, Kreis: Mittelpunkt) |
| `width` | int | erforderlich | Breite (oder Durchmesser bei Kreisen) |
| `height` | int | 0 | Höhe (wird bei Kreisen ignoriert) |
| `shape` | `"rectangle"` \| `"circle"` | `"rectangle"` | Form |
| `fill_color` | str | `"#ff0000"` | Füllfarbe |
| `border_color` | str | `"#ff0000"` | Rahmenfarbe |
| `fill_opacity` | int | 51 | Fülltransparenz (0-255) |
| `border_opacity` | int | 255 | Rahmentransparenz (0-255) |
| `border_width` | int | 2 | Rahmenbreite in Pixel |
| `radius` | int | 0 | Eckenradius (nur für Rechtecke) |
| `label` | str \| None | None | Beschriftung |
| `label_size` | int | 24 | Schriftgröße |
| `label_color` | str | `"#ffffff"` | Schriftfarbe |

## Projektstruktur

```text
info/
├── docs/                           # Dokumentations-Inhalte (Markdown)
│   ├── index.md
│   ├── feueron/                    # FeuerON-Dokumentation
│   │   └── login.md
│   └── assets/                     # Generierte Assets
│       └── feueron/
│           └── screenshots/
│               ├── raw/            # Unbearbeitete Screenshots
│               ├── annotated/      # Annotierte Screenshots
│               └── framed/         # Screenshots mit Browser-Rahmen
│
├── tools/                          # Wiederverwendbare Python-Tools
│   ├── __init__.py
│   ├── annotation.py               # Marker & annotate_screenshot()
│   └── browserframe.py             # Browser-Rahmen-Kompositor
│
├── scripts/                        # Anwendungsspezifische Skripte
│   ├── cli.py                      # Typer CLI (uv run info ...)
│   └── feueron/
│       ├── screenshots.py          # Playwright-Automatisierung
│       ├── annotations.py          # Marker-Definitionen
│       ├── generate.py             # Screenshot-Pipeline-Funktionen
│       ├── models/                 # FeuerON CSV-Import Pydantic-Modelle
│       └── migration/              # Fox112 → FeuerON Datenmigration
│
├── pyproject.toml
├── zensical.toml
└── README.md
```

## Dokumentation bauen

```bash
uv run zensical build
```

Die fertige Dokumentation befindet sich dann im `site/` Verzeichnis.
