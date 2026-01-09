"""
Pattern Logic Expert
Analyzes predictability, variation, and repetition patterns
Decides what the learner should focus on
"""

import numpy as np
from typing import List

from schema.music_schema import (
    PatternLogic,
    IntensityLevel,
    BeatAnalysis,
    StructureAnalysis,
    EnergyAnalysis
)


class PatternLogicExpert:
    """
    Expert focused on pattern analysis and learning strategy
    Synthesizes information from other experts to determine teaching focus
    """
    
    def analyze(
        self,
        beat: BeatAnalysis,
        structure: StructureAnalysis,
        energy: EnergyAnalysis
    ) -> PatternLogic:
        """
        Analyze patterns and determine teaching strategy
        
        Args:
            beat: Output from BeatTempoExpert
            structure: Output from StructureExpert
            energy: Output from EnergyExpert
            
        Returns:
            PatternLogic with pattern characteristics and teaching focus
        """
        # Calculate predictability
        predictability = self._calculate_predictability(beat, structure, energy)
        
        # Calculate variation level
        variation_level = self._calculate_variation_level(structure, energy)
        
        # Calculate repetition strength
        repetition_strength = structure.repetition_ratio
        
        # Detect surprise moments
        surprise_moments = self._detect_surprises(beat, structure, energy)
        
        # Determine teaching focus
        teaching_focus = self._determine_teaching_focus(
            beat, 
            structure, 
            energy, 
            predictability,
            repetition_strength
        )
        
        return PatternLogic(
            predictability=float(predictability),
            variation_level=variation_level,
            repetition_strength=float(repetition_strength),
            surprise_moments=surprise_moments,
            teaching_focus=teaching_focus
        )
    
    def _calculate_predictability(
        self,
        beat: BeatAnalysis,
        structure: StructureAnalysis,
        energy: EnergyAnalysis
    ) -> float:
        """
        Calculate how predictable the music is
        
        Returns:
            0.0 (unpredictable) to 1.0 (highly predictable)
        """
        # Factors that increase predictability:
        # - Regular beat
        # - High repetition
        # - Stable energy
        
        # Beat regularity contributes 40%
        beat_score = beat.beat_regularity * 0.4
        
        # Repetition contributes 40%
        repetition_score = structure.repetition_ratio * 0.4
        
        # Energy stability contributes 20%
        energy_variance = np.var([m.intensity for m in energy.timeline]) if energy.timeline else 0.5
        energy_score = (1.0 - min(energy_variance * 2, 1.0)) * 0.2
        
        predictability = beat_score + repetition_score + energy_score
        
        return float(np.clip(predictability, 0, 1))
    
    def _calculate_variation_level(
        self,
        structure: StructureAnalysis,
        energy: EnergyAnalysis
    ) -> IntensityLevel:
        """
        Calculate how much the music varies over time
        """
        # Look at structural variety
        structure_variety = 1.0 - structure.repetition_ratio
        
        # Look at energy variation
        energy_variance = np.var([m.intensity for m in energy.timeline]) if energy.timeline else 0.5
        
        # Combine
        combined_variation = (structure_variety + energy_variance) / 2
        
        if combined_variation < 0.3:
            return IntensityLevel.LOW
        elif combined_variation < 0.6:
            return IntensityLevel.MEDIUM
        else:
            return IntensityLevel.HIGH
    
    def _detect_surprises(
        self,
        beat: BeatAnalysis,
        structure: StructureAnalysis,
        energy: EnergyAnalysis
    ) -> List[float]:
        """
        Detect moments of unexpected change (surprises)
        
        Returns:
            List of timestamps where surprises occur
        """
        surprises = []
        
        # Detect sudden energy changes
        if len(energy.timeline) > 1:
            for i in range(len(energy.timeline) - 1):
                current = energy.timeline[i]
                next_moment = energy.timeline[i + 1]
                
                # Large intensity jump
                intensity_jump = abs(next_moment.intensity - current.intensity)
                if intensity_jump > 0.3:
                    surprises.append(next_moment.time)
                
                # Large tension jump
                tension_jump = abs(next_moment.tension - current.tension)
                if tension_jump > 0.3:
                    surprises.append(next_moment.time)
        
        # Detect section changes (structural surprises)
        for section in structure.sections:
            if section.similarity_score < 0.5:  # New, unfamiliar section
                surprises.append(section.start_time)
        
        # Remove duplicates and sort
        surprises = sorted(list(set(surprises)))
        
        return surprises[:5]  # Return up to 5 most significant surprises
    
    def _determine_teaching_focus(
        self,
        beat: BeatAnalysis,
        structure: StructureAnalysis,
        energy: EnergyAnalysis,
        predictability: float,
        repetition_strength: float
    ) -> str:
        """
        Determine what aspect the learner should focus on first
        
        Returns:
            Teaching focus recommendation
        """
        # Decision tree based on characteristics
        
        # If beat is very regular and prominent, start there
        if beat.beat_regularity > 0.8 and beat.beat_density != IntensityLevel.LOW:
            return "rhythm_pattern"
        
        # If highly repetitive, focus on recognizing repetition
        if repetition_strength > 0.7:
            return "repetition_recognition"
        
        # If clear energy arc, focus on tension and release
        if energy.has_buildup and energy.has_release:
            return "tension_release"
        
        # If many sections, focus on structure
        if structure.total_sections >= 4:
            return "section_structure"
        
        # If unpredictable, focus on variation
        if predictability < 0.4:
            return "pattern_variation"
        
        # Default: start with overall structure
        return "overall_structure"
