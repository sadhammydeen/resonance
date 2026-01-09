# 🚀 Setup Guide (New Architecture)

## Prerequisites

- Python 3.9+
- pip
- 4GB+ RAM (8GB+ recommended for LLM)
- GPU optional (CPU works fine with small models)

## Installation

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**What this installs**:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `librosa` - Audio analysis (DSP)
- `torch` - PyTorch (for LLM)
- `transformers` - HuggingFace models
- `accelerate` - Faster model loading
- `numpy`, `scipy` - Scientific computing

### 2. Download LLM Model (First Run)

The model downloads automatically on first request (~5GB for Phi-2).

**To pre-download**:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "microsoft/phi-2"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)
```

**Model Options**:
- `microsoft/phi-2` (2.7B) - Best quality, recommended
- `TinyLlama/TinyLlama-1.1B-Chat-v1.0` (1.1B) - Faster
- `google/flan-t5-base` (250M) - Minimal

To change model, edit `services/local_llm_service.py`:

```python
llm_service = get_llm_service(model_name="tinyllama")  # or "phi-2" or "flan-t5-base"
```

### 3. Test the Architecture

```bash
cd backend
python test_architecture.py
```

**What this tests**:
1. ✅ All 4 experts load correctly
2. ✅ Orchestrator coordinates them
3. ✅ Complete MusicState produced
4. ✅ (Optional) LLM generates explanation

**Sample output**:
```
============================================================
TESTING NEW MODULAR ARCHITECTURE
============================================================

1️⃣  Initializing Orchestrator...
   ✅ All experts loaded

2️⃣  Analyzing: uploads/test.mp3
------------------------------------------------------------
🎵 Orchestrator: Starting analysis for test.mp3
   Duration: 180.5s | Sample Rate: 22050Hz
🥁 Calling Beat & Tempo Expert...
   ✅ BPM: 120.3 | Regularity: 0.87
🏗️  Calling Structure Expert...
   ✅ Sections: 5 | Repetition: 0.65
❤️  Calling Energy Expert...
   ✅ Energy: medium | Arc: wave
🧠 Calling Pattern Logic Expert...
   ✅ Predictability: 0.72 | Focus: rhythm_pattern
🎯 Orchestrator: Making high-level decisions...
   Primary: rhythm_focused
   Strategy: Start by following the steady beat
   Complexity: medium
✅ Orchestrator: Analysis complete!
------------------------------------------------------------

3️⃣  RESULTS:
   [... detailed output ...]

✅ TEST PASSED!
```

### 4. Start the Server

```bash
cd backend
uvicorn main:app --reload
```

Server runs at: `http://localhost:8000`

### 5. Install Frontend (Optional)

```bash
cd frontend
npm install
npm start
```

Frontend runs at: `http://localhost:3000`

## Directory Structure

```
backend/
├── schema/
│   └── music_schema.py          # Data contracts
├── experts/
│   ├── beat_tempo_expert.py     # Rhythm analysis
│   ├── structure_expert.py      # Section detection
│   ├── energy_expert.py         # Energy/tension
│   └── pattern_logic_expert.py  # Pattern synthesis
├── orchestrator/
│   └── music_orchestrator.py    # Rule-based coordinator
├── services/
│   └── local_llm_service.py     # HuggingFace LLM
├── api/
│   └── routes.py                # FastAPI endpoints
├── test_architecture.py         # Test suite
├── requirements.txt
└── main.py                      # FastAPI app

frontend/
├── src/
│   ├── App.js                   # Main component
│   └── components/              # Visualization components
├── package.json
└── public/
```

## API Usage

### Analyze Audio

**Endpoint**: `POST /api/analyze`

**Request**:
```bash
curl -X POST http://localhost:8000/api/analyze \
  -F "file=@song.mp3" \
  -F "user_level=beginner"
```

**Response**:
```json
{
  "file_id": "uuid",
  "filename": "song.mp3",
  "analysis": {
    "rhythm": {
      "bpm": 120.5,
      "tempo_category": "moderate",
      "regularity": 0.87,
      "density": "high"
    },
    "structure": {
      "total_sections": 5,
      "repetition_ratio": 0.65,
      "pattern_type": "repetitive"
    },
    "energy": {
      "overall": "medium",
      "has_buildup": true,
      "has_release": true,
      "arc": "wave"
    },
    "pattern": {
      "predictability": 0.72,
      "variation": "medium",
      "teaching_focus": "rhythm_pattern"
    },
    "insights": {
      "primary_characteristic": "rhythm_focused",
      "learning_strategy": "Start by following the steady beat",
      "complexity": "medium"
    }
  },
  "explanation": "This music has a strong, steady pulse - like waves returning to shore. Energy builds and releases in predictable patterns...",
  "user_level": "beginner"
}
```

## Troubleshooting

### "Model not found"
- First run downloads ~5GB
- Check internet connection
- Or manually download (see step 2)

### "Out of memory"
- Use smaller model: `tinyllama` or `flan-t5-base`
- Reduce `max_length` in `local_llm_service.py`
- Close other applications

### "librosa import error"
- Install ffmpeg: `conda install -c conda-forge ffmpeg`
- Or: `sudo apt-get install ffmpeg` (Linux)
- Or download from ffmpeg.org (Windows)

### "No audio file found"
- Place test file at `backend/uploads/test.mp3`
- Or update path in `test_architecture.py`

### "CUDA not available"
- That's OK! CPU works fine with small models
- Phi-2 on CPU: ~10-30 seconds per explanation

## Performance Tips

### Speed up inference:
1. Use GPU if available (automatic)
2. Use smaller model (`tinyllama`)
3. Reduce `max_length` (fewer words)
4. Keep model loaded (singleton pattern already implemented)

### Reduce memory:
1. Use `flan-t5-base` (250M params)
2. Set `torch_dtype=torch.float32` (instead of float16)
3. Process shorter audio clips

### Improve quality:
1. Use `phi-2` (best balance)
2. Increase `temperature` for more creative explanations
3. Customize prompt in `local_llm_service.py`

## Development Workflow

### Add new expert:
1. Create `experts/my_expert.py`
2. Define output dataclass in `schema/music_schema.py`
3. Call from `orchestrator/music_orchestrator.py`
4. Update `MusicState` to include new expert output

### Modify orchestrator logic:
- Edit `music_orchestrator.py`
- Update decision rules (pure Python)
- No need to retrain anything

### Change LLM:
- Edit `services/local_llm_service.py`
- Update `RECOMMENDED_MODELS` dict
- Or pass custom HuggingFace model ID

### Test changes:
```bash
python test_architecture.py
```

## Next Steps

1. ✅ Verify installation with test script
2. ✅ Start server
3. ✅ Upload test audio
4. 📖 Read [ARCHITECTURE_NEW.md](ARCHITECTURE_NEW.md) for design details
5. 🎨 Customize frontend visualizations
6. 🔧 Modify orchestrator rules for your use case

## Resources

- [HuggingFace Models](https://huggingface.co/models)
- [librosa Documentation](https://librosa.org/doc/latest/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [PyTorch Docs](https://pytorch.org/docs/)
