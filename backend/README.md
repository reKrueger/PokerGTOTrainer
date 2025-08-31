# Django Backend - Setup Instructions

## 🚀 Quick Start

```bash
cd backend
python start_server.py
```

Das war's! Der Script macht alles automatisch:
- Erstellt Virtual Environment
- Installiert Dependencies  
- Führt Migrations aus
- Startet Server auf http://localhost:8000

## 🔌 API Endpoints

```
GET  /api/health/              # Health check
GET  /api/random-situation/    # Random training situation  
GET  /api/position-ranges/     # Opening ranges
GET  /api/scenarios/           # Available scenarios
POST /api/analyze-hand/        # Analyze specific hand
POST /api/validate-action/     # Validate user action
```

## 🧪 Testing

```bash
# Test backend structure
python test_structure.py

# Demo API functionality  
python api_demo.py

# Start Django server
python start_server.py
```

## 📊 Example API Response

```json
{
  "situation_id": 1234,
  "position": {"short_name": "BTN", "full_name": "Button"},
  "hand": {
    "card1": {"rank": "A", "suit": "H"},
    "card2": {"rank": "K", "suit": "S"}, 
    "notation": "AKo"
  },
  "gto_analysis": {
    "recommended_action": "raise/4-bet/all in",
    "explanation": "AKo is premium - raise and go all-in if 4-bet"
  }
}
```

Backend ist ready für React Frontend! 🎰
