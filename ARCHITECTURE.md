# 🏗️ System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER                                     │
│                    (Web Browser)                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTP/React
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                   FRONTEND                                       │
│              React Application                                   │
│              (Port 3000)                                        │
│                                                                  │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐        │
│  │   App.js    │  │  Components  │  │     Styles     │        │
│  │             │  │              │  │                │        │
│  │ - Upload    │  │ - RhythmMap  │  │  index.css     │        │
│  │ - State     │  │ - Emotion    │  │                │        │
│  │ - API calls │  │ - Structure  │  │  (Gradients,   │        │
│  │             │  │ - Explain    │  │   Colors)      │        │
│  │             │  │ - Feedback   │  │                │        │
│  └─────────────┘  └──────────────┘  └────────────────┘        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTP POST /api/analyze
                         │ (multipart/form-data)
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                    BACKEND                                       │
│               FastAPI Server                                     │
│               (Port 8000)                                       │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    main.py                               │   │
│  │  - CORS middleware                                       │   │
│  │  - Route registration                                    │   │
│  │  - File upload handling                                  │   │
│  └────────────────────┬────────────────────────────────────┘   │
│                       │                                          │
│  ┌────────────────────▼─────────────────────────────────────┐  │
│  │              api/routes.py                               │  │
│  │  POST /api/analyze:                                      │  │
│  │    1. Validate file                                      │  │
│  │    2. Save to uploads/                                   │  │
│  │    3. Call AudioAnalyzer                                 │  │
│  │    4. Call ExplanationGenerator                          │  │
│  │    5. Return JSON                                        │  │
│  └────────┬─────────────────────────┬───────────────────────┘  │
│           │                         │                            │
│  ┌────────▼───────────────┐  ┌─────▼─────────────────────────┐ │
│  │  AudioAnalyzer         │  │  ExplanationGenerator         │ │
│  │  (analysis/)           │  │  (services/)                  │ │
│  │                        │  │                               │ │
│  │  ┌──────────────────┐ │  │  ┌─────────────────────────┐ │ │
│  │  │ Extract Beats    │ │  │  │ Build Prompt            │ │ │
│  │  │ - BPM            │ │  │  │ - Format data           │ │ │
│  │  │ - Beat times     │ │  │  │ - Add context           │ │ │
│  │  │ - Time sig       │ │  │  └──────────┬──────────────┘ │ │
│  │  └──────────────────┘ │  │             │                 │ │
│  │                        │  │             │                 │ │
│  │  ┌──────────────────┐ │  │  ┌──────────▼──────────────┐ │ │
│  │  │ Extract Structure│ │  │  │ Call OpenAI API         │ │ │
│  │  │ - Sections       │ │  │  │ - GPT-4o-mini           │ │ │
│  │  │ - Boundaries     │ │  │  │ - Temperature 0.7       │ │ │
│  │  │ - Labels         │ │  │  └──────────┬──────────────┘ │ │
│  │  └──────────────────┘ │  │             │                 │ │
│  │                        │  │             │                 │ │
│  │  ┌──────────────────┐ │  │  ┌──────────▼──────────────┐ │ │
│  │  │ Extract Emotions │ │  │  │ Parse & Structure       │ │ │
│  │  │ - Energy         │ │  │  │ - Overview              │ │ │
│  │  │ - Intensity      │ │  │  │ - Rhythm                │ │ │
│  │  │ - Tension        │ │  │  │ - Structure             │ │ │
│  │  │ - Labels         │ │  │  │ - Emotions              │ │ │
│  │  └──────────────────┘ │  │  │ - Learning focus        │ │ │
│  │                        │  │  └─────────────────────────┘ │ │
│  └────────────────────────┘  └───────────────────────────────┘ │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                External Dependencies                      │  │
│  │                                                           │  │
│  │  📚 librosa - Audio signal processing                    │  │
│  │  🧮 numpy - Numerical computation                        │  │
│  │  📊 scipy - Scientific computing                         │  │
│  │  🤖 OpenAI API - Natural language generation            │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────────┐
│                     DATA FLOW                                     │
└──────────────────────────────────────────────────────────────────┘

1. Upload Audio File (MP3/WAV)
   ↓
2. Save to backend/uploads/
   ↓
3. librosa.load() → numpy array
   ↓
4. Signal Processing:
   ┌─────────────────┬──────────────────┬─────────────────┐
   │ Beat Detection  │ Structure Detect │ Emotion Extract │
   │                 │                  │                 │
   │ • Tempo track   │ • Chromagram     │ • RMS energy    │
   │ • Beat frames   │ • Similarity     │ • Spectral      │
   │ • Time sig      │ • Boundaries     │ • Loudness      │
   └────────┬────────┴────────┬─────────┴────────┬────────┘
            │                 │                  │
            └─────────────────┴──────────────────┘
                              │
                              ▼
5. Structured Data:
   {
     beat_info: { bpm, beat_times, time_signature },
     sections: [{ name, start, end, characteristics }],
     emotional_timeline: [{ time, energy, tension, label }]
   }
   ↓
6. LLM Prompt Building:
   "Explain this music WITHOUT sound references..."
   + Structured data
   ↓
7. OpenAI API Call
   ↓
8. Parse Response → Sections
   ↓
9. Combined JSON Response:
   {
     analysis: { ... },
     explanations: { overview, rhythm, structure, emotions, focus }
   }
   ↓
10. Frontend Visualization:
    • RhythmMap → Bar chart
    • EmotionTimeline → Area chart
    • StructureView → Timeline + cards
    • ExplanationPanel → Text sections
    ↓
11. User Feedback → POST /api/feedback
    ↓
12. Adaptive Response (future: ML model)
```

---

## Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    Component Relationships                       │
└─────────────────────────────────────────────────────────────────┘

App.js
  │
  ├──► useState(file) ────────────────┐
  ├──► useState(analysis) ────────┐   │
  ├──► useState(loading) ─────┐   │   │
  │                           │   │   │
  ├──► handleFileSelect() ◄───┘   │   │
  ├──► handleUpload() ────────────┼───┼──► axios.post('/api/analyze')
  │                               │   │         │
  │                               │   │         ▼
  ├──► if (analysis) ◄────────────┘   │    Backend Processing
  │      │                             │         │
  │      ├──► RhythmMap ◄──────────────┘         │
  │      │      └─ Recharts BarChart            │
  │      │                                       │
  │      ├──► EmotionTimeline                   │
  │      │      └─ Recharts AreaChart           │
  │      │                                       │
  │      ├──► StructureView                     │
  │      │      └─ Timeline + Cards             │
  │      │                                       │
  │      ├──► ExplanationPanel                  │
  │      │      └─ Text sections                │
  │      │                                       │
  │      └──► FeedbackSection ◄─────────────────┘
  │             └─ handleFeedback()
  │                  └──► axios.post('/api/feedback')
  │
  └──► Error handling / Loading states
```

---

## File Processing Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│               Audio Analysis Pipeline                            │
└─────────────────────────────────────────────────────────────────┘

Input: audio_file.mp3
  │
  ├──► librosa.load(audio_file, sr=22050)
  │         │
  │         ▼
  │    y: numpy.ndarray (audio samples)
  │    sr: int (sample rate)
  │
  ├──► Beat Analysis
  │         │
  │         ├─► librosa.beat.beat_track(y, sr)
  │         │      → tempo (BPM), beat_frames
  │         │
  │         └─► librosa.frames_to_time(beat_frames)
  │                → beat_times (seconds)
  │
  ├──► Structure Analysis
  │         │
  │         ├─► librosa.feature.chroma_cqt(y, sr)
  │         │      → chroma (harmonic content)
  │         │
  │         ├─► librosa.segment.recurrence_matrix(chroma)
  │         │      → similarity matrix
  │         │
  │         └─► librosa.segment.agglomerative(chroma, k=5)
  │                → boundaries (section changes)
  │
  └──► Emotion Analysis
            │
            ├─► Segment audio (5-second chunks)
            │
            ├─► For each segment:
            │     │
            │     ├─► librosa.feature.rms(segment)
            │     │      → energy level
            │     │
            │     ├─► librosa.amplitude_to_db(rms)
            │     │      → intensity (loudness)
            │     │
            │     └─► librosa.feature.spectral_centroid(segment)
            │            → tension (brightness)
            │
            └─► Map to emotion labels:
                  (energy, intensity, tension) → "Calm & Peaceful"
                                               → "Building Anticipation"
                                               → "Intense & Climactic"
                                               → etc.

Output: AudioAnalysisResult
  ├─ beat_info: BeatInfo
  ├─ sections: List[StructureSection]
  ├─ emotional_timeline: List[EmotionalFeature]
  └─ duration: float
```

---

## API Request/Response Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                   API Communication                              │
└─────────────────────────────────────────────────────────────────┘

Frontend                          Backend
────────                          ───────

FormData                          FastAPI Endpoint
  ├─ file: File                   ──► POST /api/analyze
  └─ user_level: "beginner"           │
                                       ├─ Validate file type
                                       ├─ Save to uploads/
                                       ├─ AudioAnalyzer.analyze()
                                       │    └─ Returns: AudioAnalysisResult
                                       │
                                       ├─ ExplanationGenerator.generate()
                                       │    ├─ Build prompt
                                       │    ├─ Call OpenAI
                                       │    └─ Parse response
                                       │
                                       └─ Build JSON response
                                            │
JSON Response                                ▼
{
  file_id: "uuid",                 ◄─── JSONResponse
  filename: "song.mp3",
  analysis: {
    beat_info: { ... },
    sections: [ ... ],
    emotional_timeline: [ ... ],
    duration: 180.5
  },
  explanations: {
    overview: "...",
    rhythm_pattern: "...",
    structure: "...",
    emotional_arc: "...",
    learning_focus: "..."
  }
}
  │
  ▼
React State Update
  │
  ├─► Render visualizations
  └─► Display explanations


Feedback Flow:
─────────────

FormData                          FastAPI Endpoint
  ├─ file_id: string              ──► POST /api/feedback
  ├─ understanding: "yes"             │
  └─ comment: string                  ├─ Validate input
                                       ├─ Store feedback
                                       └─ Generate adaptive response
                                            │
JSON Response                                ▼
{
  feedback_received: true,         ◄─── JSONResponse
  suggestion: {
    message: "...",
    next_steps: [ ... ]
  }
}
```

---

## Technology Stack Detail

```
┌─────────────────────────────────────────────────────────────────┐
│                    Technology Layers                             │
└─────────────────────────────────────────────────────────────────┘

Presentation Layer (Frontend)
┌──────────────────────────────────────┐
│ React 18                             │
│  ├─ Component-based UI               │
│  ├─ Hooks (useState, useEffect)      │
│  └─ JSX templating                   │
│                                      │
│ Recharts 2.10                        │
│  ├─ BarChart (rhythm)                │
│  ├─ AreaChart (emotion)              │
│  └─ CartesianGrid, Tooltip           │
│                                      │
│ Axios 1.6                            │
│  └─ HTTP client for API calls        │
└──────────────────────────────────────┘

Application Layer (Backend)
┌──────────────────────────────────────┐
│ FastAPI 0.109                        │
│  ├─ Async request handling           │
│  ├─ Automatic API docs               │
│  ├─ Pydantic validation              │
│  └─ CORS middleware                  │
│                                      │
│ Uvicorn 0.27                         │
│  └─ ASGI server                      │
└──────────────────────────────────────┘

Processing Layer
┌──────────────────────────────────────┐
│ librosa 0.10.1                       │
│  ├─ Audio loading                    │
│  ├─ Beat tracking                    │
│  ├─ Feature extraction               │
│  └─ Segmentation                     │
│                                      │
│ NumPy 1.24                           │
│  └─ Array operations                 │
│                                      │
│ SciPy 1.11                           │
│  └─ Signal processing                │
└──────────────────────────────────────┘

AI Layer
┌──────────────────────────────────────┐
│ OpenAI API (GPT-4o-mini)             │
│  ├─ Natural language generation      │
│  ├─ Context-aware explanations       │
│  └─ Adaptive language level          │
└──────────────────────────────────────┘

Infrastructure
┌──────────────────────────────────────┐
│ Python 3.9+ Runtime                  │
│ Node.js 16+ Runtime                  │
│ Local File System (uploads)          │
└──────────────────────────────────────┘
```

---

## Scalability & Future Architecture

```
Current (MVP):
User → React → FastAPI → librosa/OpenAI → Response

Future (Production):
                    ┌─────────────────┐
                    │   Load Balancer │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
    ┌────▼────┐        ┌────▼────┐        ┌────▼────┐
    │ FastAPI │        │ FastAPI │        │ FastAPI │
    │ Instance│        │ Instance│        │ Instance│
    └────┬────┘        └────┬────┘        └────┬────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
         ┌────▼────┐    ┌───▼────┐    ┌───▼────┐
         │ Worker  │    │ Redis  │    │ MongoDB│
         │ Queue   │    │ Cache  │    │ Storage│
         └─────────┘    └────────┘    └────────┘
```

This architecture is ready to scale when you need it! 🚀
