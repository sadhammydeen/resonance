# 📐 System Architecture Diagrams

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        USER                                  │
│                          ↓                                   │
│                    Uploads Audio                             │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                           │
│                  (routes.py: /api/analyze)                   │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                 Music Orchestrator                           │
│              (Rule-Based Coordinator)                        │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Beat    │  │Structure │  │ Energy   │  │ Pattern  │   │
│  │  Expert  │→ │  Expert  │→ │ Expert   │→ │  Logic   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│       ↓             ↓              ↓              ↓         │
│  ┌────────────────────────────────────────────────────┐    │
│  │            Synthesize → MusicState                 │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              Simplify to ExplanationContext                  │
│        (Semantic buckets: "moderate", "high", etc.)          │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  Local LLM Service                           │
│              (Phi-2 / TinyLlama / Flan-T5)                   │
│         Generate explanation (visual metaphors only)         │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   JSON Response                              │
│             {analysis: {...}, explanation: "..."}            │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
                        USER
```

---

## Data Flow Detail

```
Audio File (MP3/WAV)
        │
        ├─→ [Beat Expert] ─────→ BeatAnalysis
        │                         - bpm: 120.5
        │                         - regularity: 0.87
        │                         - density: "high"
        │                         - time_signature: "4/4"
        │
        ├─→ [Structure Expert] ─→ StructureAnalysis
        │                         - sections: 5
        │                         - repetition: 0.65
        │                         - pattern: "repetitive"
        │
        ├─→ [Energy Expert] ────→ EnergyAnalysis
        │                         - overall: "medium"
        │                         - buildup: true
        │                         - arc: "wave"
        │                         - timeline: [...]
        │
        └─→ [Pattern Logic] ────→ PatternLogic
                                  - predictability: 0.72
                                  - variation: "medium"
                                  - focus: "rhythm_pattern"
                                  
                    ↓
            [Orchestrator Synthesizes]
                    ↓
                MusicState
                    ├─ beat: BeatAnalysis
                    ├─ structure: StructureAnalysis
                    ├─ energy: EnergyAnalysis
                    ├─ pattern: PatternLogic
                    ├─ primary: "rhythm_focused"
                    ├─ strategy: "Follow the beat"
                    └─ complexity: "medium"
                    
                    ↓
          [Simplify to Buckets]
                    ↓
           ExplanationContext
                ├─ tempo: "moderate"
                ├─ energy: "medium"
                ├─ structure: "repetitive"
                ├─ pattern: "predictable"
                └─ focus: "rhythm_focused"
                
                    ↓
            [LLM Generates]
                    ↓
        "This music flows like waves,
         with steady rhythm building
         and releasing energy..."
```

---

## Module Dependencies

```
api/routes.py
    ↓ imports
orchestrator/music_orchestrator.py
    ↓ imports
    ├─→ experts/beat_tempo_expert.py
    ├─→ experts/structure_expert.py
    ├─→ experts/energy_expert.py
    └─→ experts/pattern_logic_expert.py
            ↓ all import
        schema/music_schema.py
        
services/local_llm_service.py
    ↓ imports
schema/music_schema.py
```

**Key**: No circular dependencies, clean hierarchy

---

## Expert Analysis Pipeline

```
┌───────────────────────────────────────────────────────────┐
│ BEAT & TEMPO EXPERT                                       │
├───────────────────────────────────────────────────────────┤
│ Input:  Audio file path                                   │
│ Method: librosa.beat.beat_track()                         │
│         librosa.onset.onset_detect()                      │
│ Output: BeatAnalysis                                      │
│         - BPM (float)                                     │
│         - Regularity (0-1)                                │
│         - Density (LOW/MEDIUM/HIGH)                       │
│         - Time signature (3/4 or 4/4)                     │
└───────────────────────────────────────────────────────────┘
                          ↓
┌───────────────────────────────────────────────────────────┐
│ STRUCTURE EXPERT                                          │
├───────────────────────────────────────────────────────────┤
│ Input:  Audio file path, duration                         │
│ Method: librosa.feature.chroma_cqt()                      │
│         sklearn.cluster.AgglomerativeClustering()         │
│ Output: StructureAnalysis                                 │
│         - Sections (list with timestamps)                 │
│         - Repetition ratio (0-1)                          │
│         - Pattern type (enum)                             │
└───────────────────────────────────────────────────────────┘
                          ↓
┌───────────────────────────────────────────────────────────┐
│ ENERGY EXPERT                                             │
├───────────────────────────────────────────────────────────┤
│ Input:  Audio file path, duration                         │
│ Method: librosa.feature.rms()                             │
│         librosa.feature.spectral_centroid()               │
│ Output: EnergyAnalysis                                    │
│         - Timeline (EnergyMoment list)                    │
│         - Overall energy (LOW/MEDIUM/HIGH)                │
│         - Buildup/Release (bool)                          │
│         - Arc shape (string)                              │
└───────────────────────────────────────────────────────────┘
                          ↓
┌───────────────────────────────────────────────────────────┐
│ PATTERN LOGIC EXPERT                                      │
├───────────────────────────────────────────────────────────┤
│ Input:  BeatAnalysis, StructureAnalysis, EnergyAnalysis   │
│ Method: Rule-based synthesis (if/else logic)              │
│ Output: PatternLogic                                      │
│         - Predictability (0-1)                            │
│         - Variation level (enum)                          │
│         - Surprise moments (timestamps)                   │
│         - Teaching focus (string)                         │
└───────────────────────────────────────────────────────────┘
```

---

## Orchestrator Decision Tree

```
Orchestrator receives all expert outputs
            ↓
┌─────────────────────────────────────────┐
│ Determine Primary Characteristic        │
├─────────────────────────────────────────┤
│ IF beat.regularity > 0.8                │
│    AND beat.density ≠ LOW               │
│    → "rhythm_focused"                   │
│                                         │
│ ELIF structure.repetition > 0.7         │
│    → "repetition_driven"                │
│                                         │
│ ELIF energy.buildup AND energy.release  │
│    → "energy_driven"                    │
│                                         │
│ ELIF structure.sections ≥ 5             │
│    → "structure_complex"                │
│                                         │
│ ELSE                                    │
│    → "balanced"                         │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│ Determine Learning Strategy             │
├─────────────────────────────────────────┤
│ BASED ON pattern.teaching_focus:        │
│                                         │
│ "rhythm_pattern" → "Follow the beat"    │
│ "repetition" → "Notice what repeats"    │
│ "tension_release" → "Feel the waves"    │
│ "section_structure" → "See the parts"   │
│ "variation" → "Watch for changes"       │
│ "overall" → "Big picture first"         │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│ Determine Complexity Level              │
├─────────────────────────────────────────┤
│ complexity_score = 0                    │
│                                         │
│ IF beat.regularity < 0.7: +0.3          │
│ IF structure.sections > 5: +0.3         │
│ IF pattern.variation == HIGH: +0.2      │
│ IF pattern.predictability < 0.5: +0.2   │
│                                         │
│ IF score < 0.3: LOW                     │
│ IF score < 0.6: MEDIUM                  │
│ ELSE: HIGH                              │
└─────────────────────────────────────────┘
            ↓
        MusicState
```

---

## LLM Processing Flow

```
MusicState (full data)
        ↓
┌─────────────────────────────────────────┐
│ Simplify to ExplanationContext          │
├─────────────────────────────────────────┤
│ beat.tempo_category → "moderate"        │
│ energy.overall → "high"                 │
│ structure.repetition → "repetitive"     │
│ pattern.predictability → "predictable"  │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ Build Prompt                            │
├─────────────────────────────────────────┤
│ "You are explaining music to someone    │
│  who cannot hear. Use visual metaphors. │
│                                         │
│  Music: moderate tempo, high energy,    │
│         repetitive structure            │
│                                         │
│  Teaching: Follow the steady beat       │
│                                         │
│  Generate short explanation..."         │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ LLM Inference                           │
├─────────────────────────────────────────┤
│ Model: Phi-2 (2.7B parameters)          │
│ Method: Causal language generation      │
│ Temperature: 0.7 (balanced)             │
│ Max tokens: 300                         │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ Post-Process                            │
├─────────────────────────────────────────┤
│ - Remove prompt from output             │
│ - Extract complete sentences            │
│ - Filter sound-related words            │
│ - Take first 4 sentences                │
└─────────────────────────────────────────┘
        ↓
   Explanation Text
        ↓
┌─────────────────────────────────────────┐
│ Fallback if LLM fails                   │
├─────────────────────────────────────────┤
│ Use template-based generation           │
│ "This music has [characteristic]..."    │
│ Always returns valid text               │
└─────────────────────────────────────────┘
```

---

## File Organization

```
backend/
│
├── schema/
│   └── music_schema.py           ← Data contracts (enums, dataclasses)
│
├── experts/                      ← Specialized analysis modules
│   ├── beat_tempo_expert.py      ← DSP: rhythm analysis
│   ├── structure_expert.py       ← DSP: pattern detection
│   ├── energy_expert.py          ← DSP: energy/tension
│   └── pattern_logic_expert.py   ← Rules: synthesis
│
├── orchestrator/                 ← Coordination layer
│   └── music_orchestrator.py     ← Rule-based coordinator
│
├── services/                     ← External services
│   └── local_llm_service.py      ← HuggingFace LLM wrapper
│
├── api/                          ← Web interface
│   └── routes.py                 ← FastAPI endpoints
│
├── uploads/                      ← Temporary audio storage
│
├── test_architecture.py          ← Test suite
├── requirements.txt              ← Dependencies
└── main.py                       ← FastAPI app

docs/                             ← Documentation
├── ARCHITECTURE_NEW.md           ← Design details
├── SETUP_NEW.md                  ← Installation guide
├── ARCHITECTURE_COMPARISON.md    ← Old vs New
├── QUICKSTART.md                 ← Quick reference
└── PROJECT_COMPLETE.md           ← Summary
```

---

## Type System

```
┌─────────────────────────────────────────────────────────┐
│ ENUMS (Semantic Buckets)                                │
├─────────────────────────────────────────────────────────┤
│ IntensityLevel    : LOW | MEDIUM | HIGH                 │
│ TempoCategory     : VERY_SLOW | SLOW | MODERATE |       │
│                     FAST | VERY_FAST                     │
│ EnergyLevel       : CALM | BUILDING | INTENSE |         │
│                     RELEASING                            │
│ PatternType       : REPETITIVE | VARIED | EVOLVING |    │
│                     CHAOTIC                              │
└─────────────────────────────────────────────────────────┘
            ↓ used in
┌─────────────────────────────────────────────────────────┐
│ DATACLASSES (Structured Output)                         │
├─────────────────────────────────────────────────────────┤
│ BeatAnalysis                                            │
│   - bpm: float                                          │
│   - tempo_category: TempoCategory                       │
│   - beat_regularity: float                              │
│   - beat_density: IntensityLevel                        │
│   - time_signature: str                                 │
│   - beat_positions: List[float]                         │
│                                                         │
│ StructureAnalysis                                       │
│   - sections: List[Section]                             │
│   - total_sections: int                                 │
│   - repetition_ratio: float                             │
│   - pattern_type: PatternType                           │
│   - repetition_count: int                               │
│                                                         │
│ EnergyAnalysis                                          │
│   - timeline: List[EnergyMoment]                        │
│   - overall_energy: IntensityLevel                      │
│   - has_buildup: bool                                   │
│   - has_release: bool                                   │
│   - energy_arc: str                                     │
│                                                         │
│ PatternLogic                                            │
│   - predictability: float                               │
│   - variation_level: IntensityLevel                     │
│   - repetition_strength: float                          │
│   - surprise_moments: List[float]                       │
│   - teaching_focus: str                                 │
└─────────────────────────────────────────────────────────┘
            ↓ combined into
┌─────────────────────────────────────────────────────────┐
│ MusicState (Complete Understanding)                     │
├─────────────────────────────────────────────────────────┤
│ - duration: float                                       │
│ - sample_rate: int                                      │
│ - beat: BeatAnalysis                                    │
│ - structure: StructureAnalysis                          │
│ - energy: EnergyAnalysis                                │
│ - pattern: PatternLogic                                 │
│ - primary_characteristic: str                           │
│ - learning_strategy: str                                │
│ - complexity_level: IntensityLevel                      │
└─────────────────────────────────────────────────────────┘
            ↓ simplified to
┌─────────────────────────────────────────────────────────┐
│ ExplanationContext (LLM Input)                          │
├─────────────────────────────────────────────────────────┤
│ - tempo: str                                            │
│ - energy: str                                           │
│ - structure: str                                        │
│ - pattern: str                                          │
│ - primary_focus: str                                    │
│ - teaching_strategy: str                                │
│ - complexity: str                                       │
└─────────────────────────────────────────────────────────┘
```

---

## Error Handling Flow

```
User uploads audio
        ↓
┌─────────────────────────┐
│ Validate file type      │ → Reject if not MP3/WAV/M4A
└─────────────────────────┘
        ↓
┌─────────────────────────┐
│ Save to disk            │ → Catch IOError
└─────────────────────────┘
        ↓
┌─────────────────────────┐
│ Call orchestrator       │
│   ↓                     │
│ Each expert:            │
│   try:                  │
│     analyze()           │ → Catch librosa errors
│   except:               │ → Log and use defaults
│     return defaults     │
└─────────────────────────┘
        ↓
┌─────────────────────────┐
│ Call LLM                │
│   try:                  │
│     generate()          │ → Catch model errors
│   except:               │ → Use fallback templates
│     return template     │
└─────────────────────────┘
        ↓
┌─────────────────────────┐
│ Return JSON             │ → Always valid response
└─────────────────────────┘
        ↓
┌─────────────────────────┐
│ Cleanup (optional)      │ → Delete temp file
└─────────────────────────┘
```

---

## Deployment Options

```
┌───────────────────────────────────────────────────┐
│ OPTION 1: Simple Server                          │
├───────────────────────────────────────────────────┤
│ uvicorn main:app --host 0.0.0.0 --port 8000       │
│                                                   │
│ Pros: Easy, one command                           │
│ Cons: No scaling, single process                  │
└───────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────┐
│ OPTION 2: Docker Container                        │
├───────────────────────────────────────────────────┤
│ FROM python:3.9                                   │
│ COPY backend/ /app                                │
│ RUN pip install -r requirements.txt               │
│ CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]  │
│                                                   │
│ Pros: Portable, reproducible                      │
│ Cons: Need Docker knowledge                       │
└───────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────┐
│ OPTION 3: Cloud Platform (AWS/Azure/GCP)          │
├───────────────────────────────────────────────────┤
│ - AWS: EC2 + ECS/Fargate                          │
│ - Azure: App Service                              │
│ - GCP: Cloud Run                                  │
│                                                   │
│ Pros: Scalable, managed                           │
│ Cons: Cost, complexity                            │
└───────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────┐
│ OPTION 4: Local Network                           │
├───────────────────────────────────────────────────┤
│ Run on local machine, access from LAN             │
│                                                   │
│ Pros: Free, private                               │
│ Cons: Limited to local network                    │
└───────────────────────────────────────────────────┘
```

---

This visual guide complements the other documentation files!
