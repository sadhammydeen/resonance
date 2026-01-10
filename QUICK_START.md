# 🚀 Resonance Without Sound - Quick Start Guide

## System Overview
Modern AI-powered music analysis using **local expert system** (no API keys needed!).

### Architecture
- **4 DSP-Based Experts**: Beat/Tempo, Structure, Energy, Pattern Logic
- **Rule-Based Orchestrator**: Transparent decision-making
- **Local LLM**: HuggingFace models for explanations only
- **Modern React UI**: Inspired by professional music creation tools

---

## Prerequisites

### Required Software
- **Python 3.12** (verify: `python --version`)
- **Node.js 16+** (verify: `node --version`)
- **Git** (for version control)

### Hardware Requirements
- **Minimum**: 4GB RAM, 2GB disk space
- **Recommended**: 8GB+ RAM for larger models
- **GPU**: Optional (PyTorch will auto-detect CUDA/MPS)

---

## Installation

### 1. Clone Repository
```bash
cd f:\ai_ignite
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

**Key Dependencies** (Python 3.12 compatible):
- FastAPI, Uvicorn - Web framework
- librosa 0.10.2 - Audio DSP
- HuggingFace Transformers - Local LLM
- PyTorch 2.2+ - Deep learning

#### First-Time Model Download
On first run, HuggingFace will auto-download models:
- **Phi-2** (2.7B) - Best quality, ~5GB
- **TinyLlama** (1.1B) - Fast, ~2.2GB
- **Flan-T5** (250M) - Fastest, ~1GB

Models cache to `~/.cache/huggingface/`

### 3. Frontend Setup

```bash
cd ..\frontend
npm install
```

---

## Running the Application

### Terminal 1: Start Backend
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Backend running at**: http://localhost:8000
- Swagger API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

### Terminal 2: Start Frontend
```bash
cd frontend
npm start
```

**Frontend running at**: http://localhost:3000

---

## Using the Application

### 1. Upload Audio
- **Drag & Drop** audio file onto upload area
- **Or Click** to browse files
- Supported: MP3, WAV, FLAC, OGG, M4A

### 2. Analyze
- Click **"Analyze Audio"** button
- Wait 10-30 seconds for expert analysis
- First run may take longer (model loading)

### 3. View Results

#### Key Insights Section
- **Tempo**: Overall BPM classification
- **Beat Regularity**: Consistency level
- **Emotional Arc**: Structural strategy
- **Predictability**: Pattern complexity

#### Detailed Analysis Tabs

**Rhythm & Tempo**
- BPM (beats per minute)
- Tempo category (Very Slow → Very Fast)
- Beat regularity score
- Time signature detection

**Structure Timeline**
- Detected sections (Intro, Verse, Chorus, Bridge, Outro)
- Section timestamps
- Duration metrics

**Energy Dynamics**
- Intensity levels over time
- Tension analysis
- Energy peaks and valleys
- 4 categories: Calm, Building, Intense, Releasing

**Pattern & Predictability**
- Repetition patterns
- Variation analysis
- Surprise elements
- Predictability score

---

## Architecture Details

### Expert System Flow

```
Audio File → Orchestrator → [4 Parallel Experts] → Local LLM → Results
```

#### 1. Beat/Tempo Expert (`beat_tempo_expert.py`)
- Extracts BPM using `librosa.beat.beat_track()`
- Classifies tempo (Very Slow → Very Fast)
- Measures beat regularity via onset detection

#### 2. Structure Expert (`structure_expert.py`)
- Segments audio into sections
- Detects repeated patterns
- Labels sections (Intro/Verse/Chorus/Bridge/Outro)

#### 3. Energy Expert (`energy_expert.py`)
- Analyzes RMS energy levels
- Tracks spectral centroid (brightness)
- Identifies tension through dissonance
- Categories: Calm, Building, Intense, Releasing

#### 4. Pattern Logic Expert (`pattern_logic_expert.py`)
- Measures repetition vs. variation
- Detects surprises and breaks
- Calculates predictability score

#### 5. Orchestrator (`music_orchestrator.py`)
- Coordinates all experts
- Rule-based decision making
- Synthesizes final strategy

#### 6. Local LLM Service (`local_llm_service.py`)
- **Used ONLY for**: Natural language explanation generation
- **NOT used for**: Core analysis (that's DSP-based)
- Models: Phi-2 (default), TinyLlama, Flan-T5

---

## Configuration

### Backend Config (`backend/config/settings.py`)
```python
# LLM Model Selection
LLM_MODEL = "microsoft/phi-2"  # or "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# Upload Settings
MAX_UPLOAD_SIZE_MB = 50
ALLOWED_EXTENSIONS = [".mp3", ".wav", ".flac", ".ogg", ".m4a"]

# Analysis Settings
MIN_AUDIO_DURATION_SECS = 10
```

### Frontend Config (`frontend/src/App.js`)
```javascript
// API Base URL
const API_URL = 'http://localhost:8000';
```

---

## Troubleshooting

### Backend Issues

#### "No module named 'distutils'"
**Fix**: Already resolved in requirements.txt with `setuptools>=69.0.0`

#### "Model download slow/stuck"
**Solution**: 
- Check internet connection
- Model downloads only once, then cached
- Use smaller model: Change to `TinyLlama` in `local_llm_service.py`

#### "Out of memory"
**Solution**:
- Use smaller model (Flan-T5 or TinyLlama)
- Close other applications
- Reduce batch size in LLM service

### Frontend Issues

#### "Cannot connect to backend"
**Fix**: Ensure backend is running on port 8000
```bash
curl http://localhost:8000/health
```

#### "Upload fails"
**Fix**: Check file size (<50MB) and format (MP3, WAV, etc.)

### Audio Analysis Issues

#### "Analysis taking too long"
**Normal**: First run loads models (~30-60 seconds)
**Subsequent**: Should be faster (~10-20 seconds)

#### "Poor accuracy"
**Note**: Works best with:
- Clear recordings (not heavily distorted)
- Music with defined beats
- Duration: 1-10 minutes

---

## Development Guide

### Project Structure
```
f:\ai_ignite\
├── backend/
│   ├── api/routes.py            # FastAPI endpoints
│   ├── experts/                 # 4 expert modules
│   ├── orchestrator/            # Rule-based coordinator
│   ├── services/local_llm_service.py  # HuggingFace wrapper
│   ├── schema/music_schema.py   # Type definitions
│   ├── config/settings.py       # Configuration
│   └── main.py                  # Entry point
├── frontend/
│   ├── src/
│   │   ├── App.js              # Modern UI (NEW!)
│   │   └── App.css             # Styling (NEW!)
│   ├── package.json
│   └── public/
└── docs/                        # 7 documentation files
```

### Testing

#### Run Backend Tests
```bash
cd backend
python test_architecture.py
```

#### Test API Endpoints
```bash
# Health check
curl http://localhost:8000/health

# Upload test (replace with real file)
curl -X POST http://localhost:8000/api/analyze \
  -F "file=@test.mp3" \
  -F "level=basic"
```

### Adding New Features

#### Backend: Add New Expert
1. Create `backend/experts/new_expert.py`
2. Follow schema in `music_schema.py`
3. Register in `orchestrator/music_orchestrator.py`

#### Frontend: Modify UI
- Edit `frontend/src/App.js`
- Update styles in `App.css`
- No separate component files needed (single-page design)

---

## Performance Optimization

### Backend Optimization
```python
# Use lighter model
LLM_MODEL = "google/flan-t5-base"  # 250M params

# Reduce analysis resolution
ANALYSIS_HOP_LENGTH = 1024  # Increase for faster processing
```

### Frontend Optimization
- Results cached in component state
- No unnecessary re-renders
- Lazy loading for heavy visualizations

---

## Deployment

### Production Checklist
- [ ] Remove `--reload` flag from uvicorn
- [ ] Build React: `npm run build`
- [ ] Set `CORS` origins in FastAPI
- [ ] Use production WSGI server (Gunicorn)
- [ ] Configure reverse proxy (Nginx)
- [ ] Set environment variables
- [ ] Enable HTTPS

### Docker Support (Future)
```dockerfile
# Coming soon: Containerized deployment
```

---

## Resources

### Documentation
- `docs/ARCHITECTURE.md` - System design
- `docs/EXPERT_SYSTEM.md` - Expert details
- `docs/API_GUIDE.md` - Endpoint reference
- `docs/DSP_TECHNICAL.md` - Audio processing
- `docs/DEPLOYMENT.md` - Production guide

### Model Documentation
- Phi-2: https://huggingface.co/microsoft/phi-2
- TinyLlama: https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0
- Flan-T5: https://huggingface.co/google/flan-t5-base

### Libraries
- librosa: https://librosa.org/
- FastAPI: https://fastapi.tiangolo.com/
- HuggingFace: https://huggingface.co/docs
- React: https://react.dev/

---

## Support & Contributing

### Getting Help
- Check `docs/TROUBLESHOOTING.md`
- Review API docs: http://localhost:8000/docs
- Check logs in `backend/logs/`

### Version Control
```bash
# Create feature branch
git checkout -b feature/new-expert

# Commit changes
git add .
git commit -m "Add new energy expert"

# Push to remote
git push origin feature/new-expert
```

---

## What's Next?

### Roadmap
- [ ] MIDI export functionality
- [ ] Real-time streaming analysis
- [ ] Advanced visualization (3D spectrograms)
- [ ] Mobile app (React Native)
- [ ] Plugin system for custom experts
- [ ] Cloud deployment templates

---

## Credits

**Resonance Without Sound** - AI-Powered Music Analysis
- Architecture: Expert System + Local LLM
- Frontend Design: Inspired by modern music creation tools
- Open Source, Privacy-First, No API Keys Required

Built with ❤️ using Python, React, and open-source AI

---

**Last Updated**: 2024
**Version**: 2.0 (Modern UI + Expert System)
