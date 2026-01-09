# 🏗️ New Architecture: Expert System Design

## Overview

This is a **complete redesign** using a modular expert system instead of relying on large AI models. The system is:

- **Offline-first**: No API calls, runs locally
- **Open source**: Uses HuggingFace models
- **Transparent**: Rule-based orchestration, not black-box AI
- **Testable**: Each expert is independent
- **Efficient**: Small models (1-3B parameters) only for explanation generation

## Architecture Layers

```
┌─────────────────────────────────────────────────────┐
│                   API Layer                          │
│              (FastAPI routes.py)                     │
└───────────────────┬─────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│              Orchestrator                            │
│         (Rule-based coordinator)                     │
│    Calls experts → Produces MusicState               │
└───────┬────────────┬────────────┬────────────┬──────┘
        │            │            │            │
        ▼            ▼            ▼            ▼
   ┌────────┐  ┌─────────┐  ┌────────┐  ┌──────────┐
   │ Beat & │  │Structure│  │ Energy │  │ Pattern  │
   │ Tempo  │  │ Expert  │  │ Expert │  │  Logic   │
   │ Expert │  │         │  │        │  │  Expert  │
   └────────┘  └─────────┘  └────────┘  └──────────┘
        │            │            │            │
        └────────────┴────────────┴────────────┘
                      │
                      ▼ (MusicState)
              ┌──────────────────┐
              │   ExplanationContext
              │   (Simplified)   │
              └────────┬──────────┘
                       │
                       ▼
              ┌──────────────────┐
              │   Local LLM      │
              │  (Phi-2/TinyLlama)
              │  HuggingFace     │
              └────────┬──────────┘
                       │
                       ▼
              Natural Language Explanation
```

## Components

### 1. Data Schema (`schema/music_schema.py`)

**Purpose**: Define contracts between all modules

**Key Classes**:
- `BeatAnalysis`: Tempo, regularity, beat positions
- `StructureAnalysis`: Sections, repetition patterns
- `EnergyAnalysis`: Intensity timeline, tension/release
- `PatternLogic`: Predictability, variation, teaching focus
- `MusicState`: Complete understanding (orchestrator output)
- `ExplanationContext`: Simplified state for LLM

**Why**: Type safety, clear interfaces, no ambiguity

### 2. Expert Modules

#### Beat & Tempo Expert (`experts/beat_tempo_expert.py`)
- **Input**: Audio file
- **Processing**: DSP (librosa beat tracking, onset detection)
- **Output**: `BeatAnalysis`
- **NO ML**: Pure signal processing

#### Structure Expert (`experts/structure_expert.py`)
- **Input**: Audio file
- **Processing**: Chroma features + clustering
- **Output**: `StructureAnalysis`
- **NO ML**: Pattern matching, not neural nets

#### Energy Expert (`experts/energy_expert.py`)
- **Input**: Audio file
- **Processing**: RMS energy, spectral features
- **Output**: `EnergyAnalysis`
- **NO ML**: Acoustic measurements

#### Pattern Logic Expert (`experts/pattern_logic_expert.py`)
- **Input**: Outputs from other 3 experts
- **Processing**: Rule-based synthesis
- **Output**: `PatternLogic`
- **NO ML**: Explicit decision trees

### 3. Orchestrator (`orchestrator/music_orchestrator.py`)

**Role**: Central coordinator

**Responsibilities**:
1. Call all 4 experts in sequence
2. Synthesize high-level insights
3. Produce complete `MusicState`
4. Make teaching decisions (rule-based)

**NOT an LLM**: Explicit Python logic, fully transparent

### 4. Local LLM Service (`services/local_llm_service.py`)

**Role**: Natural language generation ONLY

**Models Supported**:
- `phi-2` (2.7B) - Recommended for quality
- `tinyllama` (1.1B) - Faster, lighter
- `flan-t5-base` (250M) - Minimal resources

**Input**: `ExplanationContext` (simplified semantic buckets)
**Output**: Accessible explanation (visual/tactile metaphors)

**Constraints**:
- NO sound references
- NO analysis (already done by experts)
- ONLY translation to natural language

### 5. API Routes (`api/routes.py`)

**Flow**:
1. Receive audio upload
2. Call orchestrator → get `MusicState`
3. Convert to `ExplanationContext`
4. Call LLM → get explanation
5. Return JSON response

## Data Flow

```
Audio File
    ↓
Orchestrator coordinates experts:
    ↓
Beat Expert → BeatAnalysis (tempo, regularity)
    ↓
Structure Expert → StructureAnalysis (sections, repetition)
    ↓
Energy Expert → EnergyAnalysis (intensity, tension)
    ↓
Pattern Logic Expert → PatternLogic (predictability, focus)
    ↓
Orchestrator synthesizes → MusicState (complete)
    ↓
Simplify to ExplanationContext (semantic buckets)
    ↓
Local LLM → Natural Language Explanation
    ↓
API Response (JSON)
```

## Design Principles

### ✅ DO:
- Small, focused modules
- Explicit orchestration logic
- Type-safe data contracts
- Independent, testable experts
- DSP-based analysis
- Small LLM only for NLG

### ❌ DON'T:
- Large monolithic models
- LLM-driven orchestration
- Implicit/magical behavior
- Coupling between experts
- LLM for analysis (only for explanation)
- Sound references in output

## Key Differences from Old Architecture

| Aspect | Old (Monolithic) | New (Expert System) |
|--------|------------------|---------------------|
| **Analysis** | One big OpenAI call | 4 specialized experts |
| **Orchestration** | OpenAI decides | Explicit Python rules |
| **LLM Role** | Everything | Explanation only |
| **Offline** | No (API required) | Yes (fully local) |
| **Cost** | $$ per request | Free after setup |
| **Transparency** | Black box | Inspectable at every step |
| **Testing** | Hard (API mocking) | Easy (unit test experts) |

## Why This Design?

1. **Transparency**: See exactly how decisions are made
2. **Control**: Modify orchestrator logic without retraining
3. **Efficiency**: No overkill - DSP for analysis, LLM for language
4. **Offline**: Works without internet
5. **Free**: No API costs
6. **Testable**: Each component isolated
7. **Educational**: Perfect for showing "how it works"

## Next Steps

See [SETUP_NEW.md](SETUP_NEW.md) for installation and testing instructions.
