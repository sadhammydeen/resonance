# Resonance Without Sound

**Teach musical understanding without sound, using structure, rhythm, visuals, emotion, and patterns.**

## Core Promise
Enable anyone — including deaf and neurodivergent learners — to understand music through AI-powered visual interpretation.

## MVP Features (6-8 weeks)
- ✅ Upload audio files (MP3/WAV)
- ✅ Visual rhythm maps
- ✅ Emotion timeline visualization
- ✅ Structural section breakdown
- ✅ AI-powered explanations in natural language
- ✅ Adaptive feedback collection

## Tech Stack
- **Frontend**: React + Recharts (visualization)
- **Backend**: Python + FastAPI
- **AI**: librosa (audio analysis) + OpenAI API (explanations)
- **Storage**: Local filesystem (MVP), Firebase (future)

## Project Structure
```
ai_ignite/
├── backend/           # Python FastAPI server
│   ├── api/          # API endpoints
│   ├── analysis/     # Audio analysis engine
│   └── services/     # LLM and processing services
├── frontend/         # React application
│   ├── src/
│   │   ├── components/  # UI components
│   │   └── services/    # API client
└── docs/            # Documentation
```

## Getting Started

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## Architecture Flow
1. User uploads audio file
2. Backend extracts: BPM, beats, sections, emotional features
3. LLM generates human-readable explanations
4. Frontend displays visual rhythm maps + emotion timeline
5. User provides feedback → system adapts

## Target Users
- Deaf and hard-of-hearing learners
- Neurodivergent individuals
- Visual learners
- Music education innovators

## Validation Metrics
- Can users identify when music repeats?
- Can users feel tension vs release?
- Do visuals make sense without sound?
