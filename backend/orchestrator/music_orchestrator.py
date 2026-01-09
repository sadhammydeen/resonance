"""
Orchestrator: The Brain
Coordinates all expert modules and produces unified MusicState
Rule-based, transparent, no LLM
"""

import librosa
from pathlib import Path

from schema.music_schema import (
    MusicState,
    IntensityLevel
)
from experts.beat_tempo_expert import BeatTempoExpert
from experts.structure_expert import StructureExpert
from experts.energy_expert import EnergyExpert
from experts.pattern_logic_expert import PatternLogicExpert


class MusicOrchestrator:
    """
    Central coordinator for all expert modules
    Implements explicit, rule-based logic (no ML)
    Produces unified MusicState for LLM consumption
    """
    
    def __init__(self, sample_rate: int = 22050, hop_length: int = 512):
        self.sr = sample_rate
        self.hop_length = hop_length
        
        # Initialize all experts
        self.beat_expert = BeatTempoExpert(sample_rate, hop_length)
        self.structure_expert = StructureExpert(sample_rate, hop_length)
        self.energy_expert = EnergyExpert(sample_rate, hop_length)
        self.pattern_expert = PatternLogicExpert()
    
    def analyze(self, audio_path: str) -> MusicState:
        """
        Orchestrate complete music analysis
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            MusicState with all analysis results
        """
        print(f"🎵 Orchestrator: Starting analysis for {Path(audio_path).name}")
        
        # Get basic metadata
        duration, sample_rate = self._get_metadata(audio_path)
        print(f"   Duration: {duration:.1f}s | Sample Rate: {sample_rate}Hz")
        
        # Call each expert in sequence
        print("🥁 Calling Beat & Tempo Expert...")
        beat_analysis = self.beat_expert.analyze(audio_path)
        print(f"   ✅ BPM: {beat_analysis.bpm:.1f} | Regularity: {beat_analysis.beat_regularity:.2f}")
        
        print("🏗️  Calling Structure Expert...")
        structure_analysis = self.structure_expert.analyze(audio_path, duration)
        print(f"   ✅ Sections: {structure_analysis.total_sections} | Repetition: {structure_analysis.repetition_ratio:.2f}")
        
        print("❤️  Calling Energy Expert...")
        energy_analysis = self.energy_expert.analyze(audio_path, duration)
        print(f"   ✅ Energy: {energy_analysis.overall_energy.value} | Arc: {energy_analysis.energy_arc}")
        
        print("🧠 Calling Pattern Logic Expert...")
        pattern_analysis = self.pattern_expert.analyze(
            beat_analysis,
            structure_analysis,
            energy_analysis
        )
        print(f"   ✅ Predictability: {pattern_analysis.predictability:.2f} | Focus: {pattern_analysis.teaching_focus}")
        
        # Make orchestrator-level decisions
        print("🎯 Orchestrator: Making high-level decisions...")
        primary_characteristic = self._determine_primary_characteristic(
            beat_analysis,
            structure_analysis,
            energy_analysis
        )
        print(f"   Primary: {primary_characteristic}")
        
        learning_strategy = self._determine_learning_strategy(
            pattern_analysis,
            beat_analysis,
            structure_analysis
        )
        print(f"   Strategy: {learning_strategy}")
        
        complexity_level = self._determine_complexity(
            beat_analysis,
            structure_analysis,
            energy_analysis,
            pattern_analysis
        )
        print(f"   Complexity: {complexity_level.value}")
        
        # Assemble final state
        music_state = MusicState(
            duration=duration,
            sample_rate=sample_rate,
            beat=beat_analysis,
            structure=structure_analysis,
            energy=energy_analysis,
            pattern=pattern_analysis,
            primary_characteristic=primary_characteristic,
            learning_strategy=learning_strategy,
            complexity_level=complexity_level
        )
        
        print("✅ Orchestrator: Analysis complete!")
        return music_state
    
    def _get_metadata(self, audio_path: str) -> tuple[float, int]:
        """Get basic audio metadata"""
        y, sr = librosa.load(audio_path, sr=self.sr)
        duration = librosa.get_duration(y=y, sr=sr)
        return duration, sr
    
    def _determine_primary_characteristic(
        self,
        beat,
        structure,
        energy
    ) -> str:
        """
        Decide what the most prominent feature is
        Rule-based decision logic
        """
        # Count "votes" for each characteristic
        
        # Strong, regular beat = rhythm-focused
        if beat.beat_regularity > 0.8 and beat.beat_density != IntensityLevel.LOW:
            return "rhythm_focused"
        
        # High repetition = structure-driven
        if structure.repetition_ratio > 0.7:
            return "repetition_driven"
        
        # Clear energy arc = emotion-focused
        if energy.has_buildup and energy.has_release:
            return "energy_driven"
        
        # Many sections = structure-driven
        if structure.total_sections >= 5:
            return "structure_complex"
        
        # Default
        return "balanced"
    
    def _determine_learning_strategy(
        self,
        pattern,
        beat,
        structure
    ) -> str:
        """
        Decide how to teach this music
        Maps teaching focus to concrete strategy
        """
        focus = pattern.teaching_focus
        
        strategy_map = {
            "rhythm_pattern": "Start by following the steady beat - it's the foundation",
            "repetition_recognition": "Notice what repeats - that's the key to understanding",
            "tension_release": "Feel how energy builds up and releases - like waves",
            "section_structure": "See how the song is organized into different parts",
            "pattern_variation": "Look for what changes and what stays the same",
            "overall_structure": "Get the big picture first, then zoom into details"
        }
        
        return strategy_map.get(focus, "Explore the patterns and see what stands out")
    
    def _determine_complexity(
        self,
        beat,
        structure,
        energy,
        pattern
    ) -> IntensityLevel:
        """
        Determine overall complexity level
        Used to adapt explanation detail
        """
        complexity_score = 0.0
        
        # Beat irregularity increases complexity
        if beat.beat_regularity < 0.7:
            complexity_score += 0.3
        
        # Many sections increase complexity
        if structure.total_sections > 5:
            complexity_score += 0.3
        
        # High variation increases complexity
        if pattern.variation_level == IntensityLevel.HIGH:
            complexity_score += 0.2
        
        # Low predictability increases complexity
        if pattern.predictability < 0.5:
            complexity_score += 0.2
        
        # Classify
        if complexity_score < 0.3:
            return IntensityLevel.LOW
        elif complexity_score < 0.6:
            return IntensityLevel.MEDIUM
        else:
            return IntensityLevel.HIGH
