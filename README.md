# PokerGTOTrainer

Ein Python-basierter Poker GTO (Game Theory Optimal) Trainer für das Lernen und Üben von optimalen Spielstrategien.

## 🎯 Projektübersicht

Das Projekt wird als **Django Backend + Streamlit Frontend** Anwendung entwickelt:
1. **Part 1: Klassenstruktur** ✅ **FERTIG**
2. **Part 2: GTO-Analyse** ✅ **FERTIG**
3. **Part 3: Django API Backend** ✅ **FERTIG**
4. **Part 4: Streamlit Frontend** ✅ **FERTIG**

## 📋 Part 1-2: Core System (Abgeschlossen)

### Implementierte Klassen:

#### 🃏 Deck-System (`poker_gto/core/deck.py`)
- **`Suit`**: Enum für Kartenfarben (H/D/C/S)
- **`Rank`**: Enum für Kartenwerte (2-A mit Vergleichslogik)
- **`Card`**: Einzelne Spielkarte mit Rang und Farbe + JSON Serialization
- **`Deck`**: Vollständiges 52-Karten Deck mit Mischen und Ausgeben

#### 📍 Position-System (`poker_gto/core/position.py`)
- **`Position`**: Enum für Tischpositionen (UTG, MP, CO, BTN, SB, BB)
- **`PositionManager`**: Verwaltung der Positionen für verschiedene Tischgrößen (6-max)

#### 🤲 Hand-System (`poker_gto/core/hand.py`)
- **`Hand`**: Poker-Hand mit zwei Hole Cards und Notation (AKs, QQ, T9o)
- **`HandRange`**: Sammlung von Händen mit Frequenzen für GTO-Analysen

#### 🧠 GTO-System (`poker_gto/gto/`)
- **`Action`**: Enum für alle Preflop-Aktionen (raise/fold, raise/call, raise/4-bet/all in, etc.)
- **`GTORange`**: GTO-Range für spezifische Position und Szenario
- **`GTOChartParser`**: Parser für GTO-Charts basierend auf der bereitgestellten Tabelle
- **`GTOAnalyzer`**: Hauptanalyse-Engine mit Hand-Empfehlungen

## 🚀 Part 3: Django API Backend

### 🔌 API Endpoints

Das Django Backend bietet eine vollständige REST API:

```
http://localhost:8000/api/
├── health/                 # Health check endpoint
├── analyze-hand/          # POST - Analysiere spezifische Hand
├── random-situation/      # GET - Generiere zufällige Trainingssituation  
├── validate-action/       # POST - Validiere Benutzeraktion gegen GTO
├── position-ranges/       # GET - Hole Opening-Ranges für Positionen
└── scenarios/            # GET - Verfügbare Szenarien und Positionen
```

### 📊 API Response Examples

**Random Training Situation:**
```json
{
  "situation_id": 1234,
  "position": {"short_name": "BTN", "full_name": "Button", "order": 3},
  "hand": {
    "card1": {"rank": "A", "suit": "H", "rank_name": "ace", "suit_name": "hearts"},
    "card2": {"rank": "K", "suit": "S", "rank_name": "king", "suit_name": "spades"},
    "notation": "AKs",
    "is_suited": false,
    "is_pair": false
  },
  "scenario": "first_in",
  "scenario_description": "You are BTN and no one has raised yet.",
  "gto_analysis": {
    "hand": "AKo",
    "position": "BTN", 
    "recommended_action": "raise/4-bet/all in",
    "explanation": "AKo is premium - raise and go all-in if 4-bet",
    "confidence": "high"
  }
}
```

## 🎮 Part 4: Streamlit Frontend - Position Trainer

### ✨ Features der Streamlit App:

#### 🎯 **Interaktive Poker-Tisch Visualisierung:**
- **Dynamischer 6-Max Tisch** mit Plotly-Grafiken
- **Position Highlighting**: Deine aktuelle Position wird rot markiert mit Pfeilen
- **Dealer Button**: Visuelle Anzeige der Dealer-Position
- **Responsive Design**: Skaliert automatisch für verschiedene Bildschirmgrößen

#### 🃏 **Enhanced Card Display:**
- **Realistische Kartenansicht** mit Farben und Symbolen
- **Große, gut lesbare Karten** mit Border und Schatten
- **Hand-Notation Display** (AKs, QQ, T9o, etc.)
- **Suit-Emojis**: ♥️♦️♣️♠️ für bessere Visualisierung

#### 🧠 **GTO Training Features:**
- **Zufällige Situationen**: Neue Hand-Position-Kombinationen
- **Sofortiges Feedback**: Richtig/Falsch mit GTO-Erklärungen
- **Score Tracking**: Erfolgsquote über alle gespielten Hände
- **Position-spezifische Ranges**: Verschiedene Szenarien je Position

#### 🎮 **Benutzerfreundliche Kontrollen:**
- **Große Action-Buttons**: FOLD, CALL, RAISE, ALL-IN
- **Prominenter "NEUE HAND" Button**: Einfache Navigation
- **Auto-Rerun**: Tisch wird bei jeder neuen Hand neu gezeichnet
- **Sidebar Controls**: Score-Reset, Anleitungen

### 🎲 **Training Modi:**

#### **Position Awareness Training:**
- Jede neue Hand zeigt sofort deine Position am Tisch
- Verschiedene Positionen: UTG, MP, CO, BTN, SB, BB  
- Position-spezifische Opening-Ranges
- Visual Learning durch Tisch-Darstellung

#### **Scenario-Based Training:**
- **First In**: Du bist der erste Spieler der handelt
- **vs Button/SB**: Defending the Big Blind
- **vs CO**: Reagieren auf Cut-Off Raise
- **vs MP**: Entscheiden gegen Middle Position

## 💻 Installation und Nutzung

### 🚀 Schnellstart (Streamlit App):
```bash
# Streamlit App direkt starten
python streamlit_position_trainer.py
```

Das Script startet automatisch auf: `http://localhost:8501`

### 🔧 Backend starten (optional):
```bash
# Django API Server (falls benötigt)
python manage.py runserver
```

Backend läuft auf: `http://localhost:8000`

### 📦 Dependencies:
```bash
pip install -r requirements.txt
```

**Hauptabhängigkeiten:**
- **Streamlit**: Web-Interface und Interaktivität
- **Plotly**: Poker-Tisch Visualisierung
- **Django**: API Backend (optional)
- **Custom Poker Classes**: Core Game Logic

## 🏗️ Projektstruktur

```
PokerGTOTrainer/
├── streamlit_position_trainer.py  # 🎮 Hauptanwendung (Streamlit)
├── start.bat                      # Windows Startup Script
├── poker_gto/                     # 🧠 Poker Core Logic
│   ├── core/                      # Basis-Poker-Komponenten
│   │   ├── deck.py               # Karten und Deck
│   │   ├── position.py           # Tischpositionen  
│   │   ├── hand.py               # Pokerhände und Ranges
│   │   └── apps.py               # Django App Config
│   ├── gto/                      # GTO-Analyse-Engine
│   │   ├── ranges.py             # GTO-Range-Klassen
│   │   ├── parser.py             # Chart-Parser
│   │   ├── analyzer.py           # Haupt-Analyse-Engine
│   │   └── apps.py               # Django App Config
│   ├── api/                      # REST API Views (optional)
│   │   ├── views.py              # API Endpoints
│   │   ├── urls.py               # URL Routing
│   │   └── apps.py               # Django App Config
│   └── training/                 # Training-spezifische Logik
├── manage.py                     # Django Management (optional)
├── requirements.txt              # Python Dependencies
└── README.md                     # Dieses File
```

## 📊 GTO-Daten Features

### Positionsbasierte Ranges:
- **UTG (Under The Gun)**: Sehr eng (~12%) - Premium Hände only
- **MP (Middle Position)**: Eng (~15%) - konservatives Spiel
- **CO (Cut Off)**: Medium (~25%) - erweiterte Range
- **BTN (Button)**: Weit (~45%) - aggressivste Opening-Range
- **SB (Small Blind)**: Kompleting/Folding Range (~35%)
- **BB (Big Blind)**: Defensive Ranges gegen verschiedene Positionen

### Analyse-Features:
- **Hand-Analyse**: GTO-Empfehlung für jede Hand-Position-Kombination
- **Action Validation**: Überprüfe Benutzeraktionen gegen GTO
- **Range-Übersicht**: Komplette Opening-Ranges pro Position
- **Scenario Support**: Various preflop situations (first-in, vs raises)
- **Immediate Feedback**: Sofortige Erklärung der optimalen Strategie

## 🎯 Anleitung - Wie verwenden:

### 1. **App starten:**
```bash
python streamlit_position_trainer.py
```

### 2. **Training beginnen:**
- Klicke "🎲 NEUE HAND" in der Sidebar
- Betrachte deine Position (rot markiert am Tisch)
- Schaue deine zwei Hole Cards an
- Wähle deine Aktion: FOLD, CALL, RAISE, ALL-IN

### 3. **Lernen vom Feedback:**
- ✅ **Richtig**: Deine Aktion stimmt mit GTO überein
- ❌ **Falsch**: Lerne die optimale GTO-Empfehlung
- 📊 **Score Tracking**: Verfolge deine Erfolgsquote

### 4. **Verschiedene Positionen meistern:**
- **Early Position** (UTG/MP): Sehr selektiv spielen
- **Late Position** (CO/BTN): Mehr Hände spielen
- **Blinds** (SB/BB): Defending lernen

## 🚀 Features Highlights

### 🎨 **Visual Learning:**
- Echter Poker-Tisch mit 6 Positionen
- Farbkodierte Position (du bist immer rot)
- Große, lesbare Spielkarten
- Intuitive Button-Bedienung

### 📈 **Progress Tracking:**
- Erfolgsquote in Echtzeit
- Score über alle Sessions
- Sofortiges GTO-Feedback
- Lernkurve verfolgen

### 🎯 **Training Focus:**
- **Position Awareness**: Verstehe wo du sitzt
- **Hand Selection**: Welche Hände zu spielen
- **GTO Strategy**: Optimal Game Theory basierte Entscheidungen
- **Scenario Training**: Verschiedene Preflop-Situationen

---

**Status**: Alle 4 Parts abgeschlossen! ✅✅✅✅  
**Hauptanwendung**: Streamlit Position Trainer  
**Version**: 1.0.0 - Full Streamlit Implementation

**Quick Start**: `python streamlit_position_trainer.py`  
**Training URL**: `http://localhost:8501`