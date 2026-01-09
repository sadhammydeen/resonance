"""
Data Schema: Contracts between modules
Each expert produces structured output that flows to the orchestrator
"""

from dataclasses import dataclass, asdict
from typing import List, Literal, Optional
from enum import Enum


# ============================================================================
# ENUMS: Semantic Buckets
# ============================================================================

class IntensityLevel(str, Enum):
    """Normalized intensity levels across all experts"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TempoCategory(str, Enum):
    """Human-readable tempo categories"""
    VERY_SLOW = "very_slow"    # < 60 BPM
    SLOW = "slow"              # 60-90 BPM
    MODERATE = "moderate"      # 90-120 BPM
    FAST = "fast"              # 120-150 BPM
    VERY_FAST = "very_fast"    # > 150 BPM


class EnergyLevel(str, Enum):
    """Energy states over time"""
    CALM = "calm"
    BUILDING = "building"
    INTENSE = "intense"
    RELEASING = "releasing"


class PatternType(str, Enum):
    """Types of musical patterns"""
    REPETITIVE = "repetitive"
    VARIED = "varied"
    EVOLVING = "evolving"
    CHAOTIC = "chaotic"


# ============================================================================
# EXPERT OUTPUTS: Structured Data from Each Module
# ============================================================================

@dataclass
class BeatAnalysis:
    """Output from Beat & Tempo Expert"""
    bpm: float                          # Exact tempo
    tempo_category: TempoCategory       # Semantic bucket
    beat_times: List[float]             # Beat positions in seconds
    beat_regularity: float              # 0-1: how steady the beat is
    beat_density: IntensityLevel        # low/medium/high
    total_beats: int
    time_signature: str                 # "4/4", "3/4", etc.


@dataclass
class StructureSection:
    """One section detected by Structure Expert"""
    name: str                           # "intro", "verse", "chorus", etc.
    start_time: float
    end_time: float
    duration: float
    repetition_count: int               # How many times this pattern appears
    similarity_score: float             # 0-1: how similar to other sections


@dataclass
class StructureAnalysis:
    """Output from Structure Expert"""
    sections: List[StructureSection]
    total_sections: int
    repetition_ratio: float             # 0-1: how much repeats
    pattern_type: PatternType           # repetitive/varied/evolving/chaotic


@dataclass
class EnergyMoment:
    """Energy state at one point in time"""
    time: float
    energy_level: EnergyLevel           # calm/building/intense/releasing
    tension: float                      # 0-1: normalized tension
    intensity: float                    # 0-1: normalized intensity


@dataclass
class EnergyAnalysis:
    """Output from Energy Expert"""
    timeline: List[EnergyMoment]
    overall_energy: IntensityLevel      # low/medium/high
    has_buildup: bool                   # Presence of tension build
    has_release: bool                   # Presence of tension release
    energy_arc: str                     # "stable", "ascending", "descending", "wave"


@dataclass
class PatternLogic:
    """Output from Pattern Logic Expert"""
    predictability: float               # 0-1: how predictable
    variation_level: IntensityLevel     # low/medium/high
    repetition_strength: float          # 0-1: how much repeats
    surprise_moments: List[float]       # Timestamps of unexpected changes
    teaching_focus: str                 # What learner should focus on


# ============================================================================
# ORCHESTRATOR STATE: Combined Understanding
# ============================================================================

@dataclass
class MusicState:
    """
    Complete music understanding state
    This is what the orchestrator produces and LLM consumes
    """
    
    # Basic metadata
    duration: float
    sample_rate: int
    
    # Expert outputs
    beat: BeatAnalysis
    structure: StructureAnalysis
    energy: EnergyAnalysis
    pattern: PatternLogic
    
    # Orchestrator decisions
    primary_characteristic: str         # "rhythm-focused", "structure-driven", etc.
    learning_strategy: str              # "start with beats", "focus on repetition", etc.
    complexity_level: IntensityLevel    # low/medium/high
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return asdict(self)


# ============================================================================
# LLM INPUT: Simplified State for Explanation
# ============================================================================

@dataclass
class ExplanationContext:
    """
    Simplified context for LLM explanation generation
    Contains only semantic information, no raw numbers
    """
    
    # Tempo & Rhythm
    tempo_category: str                 # "very_slow", "fast", etc.
    beat_regularity: str                # "very steady", "somewhat irregular", etc.
    beat_density: str                   # "sparse", "moderate", "dense"
    
    # Structure
    total_sections: int
    pattern_type: str                   # "repetitive", "varied", etc.
    repetition_strength: str            # "highly repetitive", "somewhat varied", etc.
    
    # Energy
    energy_arc: str                     # "stable", "ascending", "wave"
    has_buildup: bool
    has_release: bool
    overall_energy: str                 # "calm", "moderate", "intense"
    
    # Pattern Logic
    predictability: str                 # "very predictable", "somewhat surprising", etc.
    teaching_focus: str                 # What to explain first
    complexity_level: str               # "simple", "moderate", "complex"
    
    # Duration
    duration_seconds: float
    
    @classmethod
    def from_music_state(cls, state: MusicState) -> "ExplanationContext":
        """Convert MusicState to simplified explanation context"""
        
        # Map beat regularity to human terms
        if state.beat.beat_regularity > 0.9:
            regularity = "very steady"
        elif state.beat.beat_regularity > 0.7:
            regularity = "mostly steady"
        else:
            regularity = "somewhat irregular"
        
        # Map repetition to human terms
        if state.structure.repetition_ratio > 0.7:
            repetition = "highly repetitive"
        elif state.structure.repetition_ratio > 0.4:
            repetition = "somewhat repetitive"
        else:
            repetition = "highly varied"
        
        # Map predictability to human terms
        if state.pattern.predictability > 0.7:
            predictability = "very predictable"
        elif state.pattern.predictability > 0.4:
            predictability = "moderately predictable"
        else:
            predictability = "full of surprises"
        
        return cls(
            tempo_category=state.beat.tempo_category.value,
            beat_regularity=regularity,
            beat_density=state.beat.beat_density.value,
            total_sections=state.structure.total_sections,
            pattern_type=state.structure.pattern_type.value,
            repetition_strength=repetition,
            energy_arc=state.energy.energy_arc,
            has_buildup=state.energy.has_buildup,
            has_release=state.energy.has_release,
            overall_energy=state.energy.overall_energy.value,
            predictability=predictability,
            teaching_focus=state.pattern.teaching_focus,
            complexity_level=state.complexity_level.value,
            duration_seconds=state.duration
        )
