# PokerGTOTrainer

Ein Python-basierter Poker GTO (Game Theory Optimal) Trainer für das Lernen und Üben von optimalen Spielstrategien.

## 🎯 Projektübersicht

Das Projekt wird in 3 Hauptteile entwickelt:
1. **Part 1: Klassenstruktur** ✅ **FERTIG**
2. **Part 2: GTO-Analyse** ✅ **FERTIG**
3. **Part 3: Benutzeroberfläche** (In Planung)

## 📋 Part 1: Klassenstruktur (Abgeschlossen)

### Implementierte Klassen:

#### 🃏 Deck-System (`src/core/deck.py`)
- **`Suit`**: Enum für Kartenfarben (H/D/C/S)
- **`Rank`**: Enum für Kartenwerte (2-A mit Vergleichslogik)
- **`Card`**: Einzelne Spielkarte mit Rang und Farbe
- **`Deck`**: Vollständiges 52-Karten Deck mit Mischen und Ausgeben

#### 📍 Position-System (`src/core/position.py`)
- **`Position`**: Enum für Tischpositionen (UTG, MP, CO, BTN, SB, BB)
- **`PositionManager`**: Verwaltung der Positionen für verschiedene Tischgrößen (aktuell 6-max)

#### 🤲 Hand-System (`src/core/hand.py`)
- **`Hand`**: Poker-Hand mit zwei Hole Cards und Notation (AKs, QQ, T9o)
- **`HandRange`**: Sammlung von Händen mit Frequenzen für GTO-Analysen

#### 🎲 Tisch-System (`src/core/table.py`)
- **`Player`**: Spieler mit Position, Stack, Hole Cards und Aktionen
- **`Table`**: Pokertisch mit Spielern, Community Cards und Spielzustand

## 📊 Part 2: GTO-Analyse (Abgeschlossen)

### Implementierte GTO-Features:

#### 🧠 GTO-Engine (`src/gto/`)
- **`Action`**: Enum für alle Preflop-Aktionen (raise/fold, raise/call, raise/4-bet/all in, etc.)
- **`GTORange`**: GTO-Range für spezifische Position und Szenario
- **`GTOChartParser`**: Parser für GTO-Charts basierend auf der bereitgestellten Tabelle
- **`GTOAnalyzer`**: Hauptanalyse-Engine mit Hand-Empfehlungen

#### 📈 Positionsbasierte Ranges:
- **MP (Middle Position)**: Eng (40 Hände) - konservatives Spiel
- **CO (Cut Off)**: Medium (52 Hände) - erweiterte Range
- **BTN (Button)**: Weit (69 Hände) - aggressivste Opening-Range
- **BB (Big Blind)**: Defensive Ranges gegen verschiedene Positionen

#### 🎯 Analyse-Features:
- **Hand-Analyse**: GTO-Empfehlung für jede Hand-Position-Kombination
- **Position-Vergleich**: Vergleicht dieselbe Hand aus verschiedenen Positionen
- **Tisch-Analyse**: Analysiert alle Spieler-Hände gleichzeitig
- **Quiz-Modus**: Generiert zufällige Fragen mit Multiple Choice
- **Range-Zusammenfassung**: Zeigt komplette Opening-Ranges pro Position
- **Flop-Analyse**: Grundlegende Texture-Erkennung (Paired/Wet/Dry/Rainbow)

### 🎮 Demos und Tests

```bash
# Part 1 Demo - Basis-Klassenstruktur
python demo.py

# Part 2 Demo - GTO-Analyse-System
python demo_part2.py
```

**Part 2 Demo zeigt:**
- GTO-Empfehlungen für verschiedene Hände (AKs, QQ, 87s, A2o)
- Opening-Range-Übersicht für MP/CO/BTN
- Position-Vergleiche für dieselbe Hand
- Live-Tischanalyse mit GTO-Empfehlungen
- Quiz-Modus mit Multiple Choice Fragen
- Flop-Texture-Analyse (Paired/Wet/Dry)

## 🏗️ Projektstruktur

```
PokerGTOTrainer/
├── src/
│   ├── core/                 # Basis-Poker-Komponenten
│   │   ├── __init__.py
│   │   ├── deck.py          # Karten und Deck
│   │   ├── position.py      # Tischpositionen
│   │   ├── hand.py          # Pokerhände und Ranges
│   │   └── table.py         # Tisch und Spieler
│   ├── gto/                 # GTO-Analyse-Engine
│   │   ├── __init__.py
│   │   ├── ranges.py        # GTO-Range-Klassen
│   │   ├── parser.py        # Chart-Parser (basierend auf Spreadsheet)
│   │   └── analyzer.py      # Haupt-Analyse-Engine
│   └── __init__.py
├── demo.py                  # Part 1 Demo
├── demo_part2.py           # Part 2 Demo - GTO-Analyse
└── README.md
```

## 🔮 Part 3: Benutzeroberfläche (Nächster Schritt)

### Geplante Features:
- **Interaktive Konsolen-Anwendung**
- **Szenario-Generator** für Trainings-Situationen
- **Quiz-Training-Modus** mit Fortschritts-Tracking
- **Range-Visualisierung** in der Konsole
- **Hand-History-Analyse**

## 💻 Technische Details

- **Python 3.8+**
- **Objektorientierte Architektur** mit modularem Design
- **Type Hints** für bessere Code-Qualität
- **Umfangreiche GTO-Daten** basierend auf professionellen Charts
- **Keine externen Dependencies** - pure Python-Implementation

## 🚀 Installation und Nutzung

```bash
# Repository klonen
git clone <repository-url>
cd PokerGTOTrainer

# Part 1: Basis-Demo ausführen
python demo.py

# Part 2: GTO-Analyse-Demo ausführen
python demo_part2.py
```

## 📊 GTO-Beispiele

### Typische GTO-Empfehlungen:
- **AA, KK, QQ, JJ, AKs**: raise/4-bet/all in (Premium-Hände)
- **AQs, AJs, KQs**: raise/4-bet/fold (Starke Hände)
- **ATs, KJs, QJs**: raise/call (Medium-Hände)
- **87s, 76s**: raise/fold vom BTN, fold von MP (Suited Connectors)

### Range-Progression:
- **MP**: 40 Hände (≈9% der Hände) - Sehr eng
- **CO**: 52 Hände (≈12% der Hände) - Medium
- **BTN**: 69 Hände (≈16% der Hände) - Weit

---

**Status**: Part 1 & 2 abgeschlossen ✅✅  
**Aktueller Meilenstein**: Part 3 - Interactive UI Implementation  
**Version**: 0.2.0
