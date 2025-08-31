# PokerGTOTrainer

Ein Python-basierter Poker GTO (Game Theory Optimal) Trainer für das Lernen und Üben von optimalen Spielstrategien.

## 🎯 Projektübersicht

Das Projekt wird als **Django + React** Full-Stack Anwendung entwickelt:
1. **Part 1: Klassenstruktur** ✅ **FERTIG**
2. **Part 2: GTO-Analyse** ✅ **FERTIG**
3. **Part 3: Django API Backend** ✅ **FERTIG**
4. **Part 4: React Frontend** (In Entwicklung)

## 📋 Part 1-2: Core System (Abgeschlossen)

### Implementierte Klassen:

#### 🃏 Deck-System (`backend/poker_gto/core/deck.py`)
- **`Suit`**: Enum für Kartenfarben (H/D/C/S)
- **`Rank`**: Enum für Kartenwerte (2-A mit Vergleichslogik)
- **`Card`**: Einzelne Spielkarte mit Rang und Farbe + JSON Serialization
- **`Deck`**: Vollständiges 52-Karten Deck mit Mischen und Ausgeben

#### 📍 Position-System (`backend/poker_gto/core/position.py`)
- **`Position`**: Enum für Tischpositionen (UTG, MP, CO, BTN, SB, BB)
- **`PositionManager`**: Verwaltung der Positionen für verschiedene Tischgrößen (6-max)

#### 🤲 Hand-System (`backend/poker_gto/core/hand.py`)
- **`Hand`**: Poker-Hand mit zwei Hole Cards und Notation (AKs, QQ, T9o)
- **`HandRange`**: Sammlung von Händen mit Frequenzen für GTO-Analysen

#### 🧠 GTO-System (`backend/poker_gto/gto/`)
- **`Action`**: Enum für alle Preflop-Aktionen (raise/fold, raise/call, raise/4-bet/all in, etc.)
- **`GTORange`**: GTO-Range für spezifische Position und Szenario
- **`GTOChartParser`**: Parser für GTO-Charts basierend auf der bereitgestellten Tabelle
- **`GTOAnalyzer`**: Hauptanalyse-Engine mit Hand-Empfehlungen

## 🚀 Part 3: Django API Backend (Neu!)

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

**Action Validation:**
```json
{
  "is_correct": true,
  "user_action": "raise",
  "gto_action": "raise/4-bet/all in", 
  "gto_explanation": "AKo is premium - raise and go all-in if 4-bet",
  "feedback": "Correct! Raise is the GTO play here."
}
```

### 🏗️ Neue Projektstruktur

```
PokerGTOTrainer/
├── backend/                    # Django API Backend
│   ├── poker_gto/
│   │   ├── core/              # Basis-Poker-Komponenten (mit JSON Support)
│   │   │   ├── deck.py        # Karten und Deck
│   │   │   ├── position.py    # Tischpositionen  
│   │   │   ├── hand.py        # Pokerhände und Ranges
│   │   │   └── apps.py        # Django App Config
│   │   ├── gto/               # GTO-Analyse-Engine
│   │   │   ├── ranges.py      # GTO-Range-Klassen
│   │   │   ├── parser.py      # Chart-Parser
│   │   │   ├── analyzer.py    # Haupt-Analyse-Engine
│   │   │   └── apps.py        # Django App Config
│   │   ├── api/               # REST API Views
│   │   │   ├── views.py       # API Endpoints
│   │   │   ├── urls.py        # URL Routing
│   │   │   └── apps.py        # Django App Config
│   │   ├── training/          # Training-spezifische Logik
│   │   └── settings.py        # Django Settings (CORS enabled)
│   ├── manage.py              # Django Management
│   ├── requirements.txt       # Python Dependencies
│   └── start_server.py        # Backend Startup Script
├── frontend/                  # React Frontend (Coming Next!)
├── src/                       # Legacy Console App (Backup)
├── demo.py                    # Part 1 Demo (Legacy)
└── start.py                   # Console UI (Legacy)
```

## 💻 Installation und Nutzung

### Backend starten:
```bash
cd backend
python start_server.py
```

Das Script:
- Erstellt automatisch ein Virtual Environment
- Installiert alle Dependencies 
- Führt Django Migrations aus
- Startet den Development Server auf `http://localhost:8000`

### API Testing:
```bash
# Health Check
curl http://localhost:8000/api/health/

# Random Training Situation
curl http://localhost:8000/api/random-situation/

# Available Scenarios  
curl http://localhost:8000/api/scenarios/

# Position Ranges
curl "http://localhost:8000/api/position-ranges/?position=BTN&scenario=first_in"
```

## 🔧 Technische Details

### Backend:
- **Django 5.0.6** mit REST Framework
- **CORS Headers** für React Frontend
- **JSON Serialization** für alle Poker-Klassen
- **Error Handling** und Validation
- **Modular Architecture** mit separaten Apps

### API Features:
- **RESTful Design** mit standardisierten HTTP Methods
- **JSON Responses** für alle Endpoints
- **Error Handling** mit HTTP Status Codes
- **CORS Support** für Cross-Origin Requests
- **Flexible Parameter Handling**

## 📊 GTO-Daten Features

### Positionsbasierte Ranges:
- **MP (Middle Position)**: Eng (40 Hände) - konservatives Spiel
- **CO (Cut Off)**: Medium (52 Hände) - erweiterte Range
- **BTN (Button)**: Weit (69 Hände) - aggressivste Opening-Range
- **BB (Big Blind)**: Defensive Ranges gegen verschiedene Positionen

### Analyse-Features:
- **Hand-Analyse**: GTO-Empfehlung für jede Hand-Position-Kombination
- **Action Validation**: Überprüfe Benutzeraktionen gegen GTO
- **Range-Übersicht**: Komplette Opening-Ranges pro Position
- **Scenario Support**: Various preflop situations (first-in, vs raises)

## 🔮 Part 4: React Frontend (Next)

### Geplante Features:
- **Moderne React UI** mit TypeScript
- **Interactive Training Mode** mit schöner Visualisierung
- **Hand Range Charts** und Poker Table Display
- **Progress Tracking** und Statistics
- **Responsive Design** für Desktop und Mobile
- **Real-time API Integration** mit Django Backend

---

**Status**: Parts 1-3 abgeschlossen ✅✅✅  
**Aktueller Meilenstein**: Part 4 - React Frontend Implementation  
**Version**: 0.3.0 - Django API Backend

**API Base URL**: `http://localhost:8000/api/`  
**Health Check**: `http://localhost:8000/api/health/`