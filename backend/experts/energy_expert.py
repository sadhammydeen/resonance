"""
Energy Expert
Analyzes energy levels, tension, and emotional dynamics WITHOUT subjective labels
"""

import librosa
import numpy as np
from typing import List

from schema.music_schema import (
    EnergyAnalysis,
    EnergyMoment,
    EnergyLevel,
    IntensityLevel
)


class EnergyExpert:
    """
    Expert focused on energy and tension dynamics
    Uses objective acoustic features, not subjective emotion labels
    """
    
    def __init__(self, sample_rate: int = 22050, hop_length: int = 512):
        self.sr = sample_rate
        self.hop_length = hop_length
        self.segment_duration = 5.0  # Analyze in 5-second windows
    
    def analyze(self, audio_path: str, duration: float) -> EnergyAnalysis:
        """
        Extract energy and tension information from audio
        
        Returns:
            EnergyAnalysis with energy timeline and characteristics
        """
        # Load audio
        y, sr = librosa.load(audio_path, sr=self.sr)
        
        # Build energy timeline
        timeline = self._build_energy_timeline(y, sr, duration)
        
        # Analyze overall energy
        overall_energy = self._calculate_overall_energy(timeline)
        
        # Detect buildup and release patterns
        has_buildup, has_release = self._detect_tension_patterns(timeline)
        
        # Classify energy arc (shape over time)
        energy_arc = self._classify_energy_arc(timeline)
        
        return EnergyAnalysis(
            timeline=timeline,
            overall_energy=overall_energy,
            has_buildup=has_buildup,
            has_release=has_release,
            energy_arc=energy_arc
        )
    
    def _build_energy_timeline(
        self, 
        y: np.ndarray, 
        sr: int, 
        duration: float
    ) -> List[EnergyMoment]:
        """
        Build timeline of energy states
        """
        num_segments = int(np.ceil(duration / self.segment_duration))
        timeline = []
        
        for i in range(num_segments):
            start_time = i * self.segment_duration
            end_time = min((i + 1) * self.segment_duration, duration)
            
            # Extract segment
            start_sample = int(start_time * sr)
            end_sample = int(end_time * sr)
            segment = y[start_sample:end_sample]
            
            if len(segment) == 0:
                continue
            
            # Calculate objective metrics
            intensity = self._calculate_intensity(segment)
            tension = self._calculate_tension(segment, sr)
            
            # Map to energy level
            energy_level = self._map_to_energy_level(intensity, tension)
            
            timeline.append(EnergyMoment(
                time=start_time,
                energy_level=energy_level,
                tension=float(tension),
                intensity=float(intensity)
            ))
        
        return timeline
    
    def _calculate_intensity(self, segment: np.ndarray) -> float:
        """
        Calculate intensity using RMS energy and loudness
        
        Returns:
            0.0 (quiet) to 1.0 (loud)
        """
        # RMS energy
        rms = librosa.feature.rms(y=segment)[0]
        
        # Convert to dB and normalize
        loudness = librosa.amplitude_to_db(rms, ref=np.max)
        
        # Normalize to 0-1 range
        # Typical range: -60 dB (quiet) to 0 dB (loud)
        normalized = np.clip((np.mean(loudness) + 60) / 60, 0, 1)
        
        return float(normalized)
    
    def _calculate_tension(self, segment: np.ndarray, sr: int) -> float:
        """
        Calculate tension using spectral features
        Higher frequencies and dissonance = more tension
        
        Returns:
            0.0 (relaxed) to 1.0 (tense)
        """
        # Spectral centroid (brightness)
        # Higher centroid = brighter, more tense sound
        centroid = librosa.feature.spectral_centroid(y=segment, sr=sr)[0]
        
        # Normalize to 0-1 range
        # Typical range: 0-4000 Hz for most music
        centroid_norm = np.clip(np.mean(centroid) / 4000, 0, 1)
        
        # Spectral rolloff (where most energy is)
        rolloff = librosa.feature.spectral_rolloff(y=segment, sr=sr)[0]
        rolloff_norm = np.clip(np.mean(rolloff) / 8000, 0, 1)
        
        # Zero crossing rate (roughness)
        zcr = librosa.feature.zero_crossing_rate(segment)[0]
        zcr_norm = np.clip(np.mean(zcr) * 10, 0, 1)
        
        # Combine metrics (weighted average)
        tension = (
            0.4 * centroid_norm +
            0.3 * rolloff_norm +
            0.3 * zcr_norm
        )
        
        return float(tension)
    
    def _map_to_energy_level(self, intensity: float, tension: float) -> EnergyLevel:
        """
        Map intensity and tension to energy level
        """
        # Calculate combined energy
        combined = (intensity + tension) / 2
        
        # Look at trend (increasing/decreasing)
        # For now, use thresholds
        
        if combined < 0.3:
            if tension < 0.3:
                return EnergyLevel.CALM
            else:
                return EnergyLevel.BUILDING
        elif combined < 0.6:
            return EnergyLevel.BUILDING
        else:
            if tension > 0.7:
                return EnergyLevel.INTENSE
            else:
                return EnergyLevel.RELEASING
    
    def _calculate_overall_energy(self, timeline: List[EnergyMoment]) -> IntensityLevel:
        """
        Calculate overall energy level across the piece
        """
        if not timeline:
            return IntensityLevel.MEDIUM
        
        avg_intensity = np.mean([m.intensity for m in timeline])
        
        if avg_intensity < 0.3:
            return IntensityLevel.LOW
        elif avg_intensity < 0.6:
            return IntensityLevel.MEDIUM
        else:
            return IntensityLevel.HIGH
    
    def _detect_tension_patterns(
        self, 
        timeline: List[EnergyMoment]
    ) -> tuple[bool, bool]:
        """
        Detect buildup (ascending tension) and release (descending tension)
        
        Returns:
            (has_buildup, has_release)
        """
        if len(timeline) < 3:
            return False, False
        
        tensions = [m.tension for m in timeline]
        
        # Look for sustained increases (buildup)
        has_buildup = False
        for i in range(len(tensions) - 2):
            if tensions[i] < tensions[i+1] < tensions[i+2]:
                # Found ascending pattern
                increase = tensions[i+2] - tensions[i]
                if increase > 0.2:  # Significant increase
                    has_buildup = True
                    break
        
        # Look for sustained decreases (release)
        has_release = False
        for i in range(len(tensions) - 2):
            if tensions[i] > tensions[i+1] > tensions[i+2]:
                # Found descending pattern
                decrease = tensions[i] - tensions[i+2]
                if decrease > 0.2:  # Significant decrease
                    has_release = True
                    break
        
        return has_buildup, has_release
    
    def _classify_energy_arc(self, timeline: List[EnergyMoment]) -> str:
        """
        Classify the overall shape of the energy journey
        
        Returns:
            "stable", "ascending", "descending", or "wave"
        """
        if len(timeline) < 3:
            return "stable"
        
        intensities = [m.intensity for m in timeline]
        
        # Calculate trend
        start_avg = np.mean(intensities[:len(intensities)//3])
        end_avg = np.mean(intensities[-len(intensities)//3:])
        
        diff = end_avg - start_avg
        
        # Calculate variance (how much it changes)
        variance = np.var(intensities)
        
        if variance < 0.05:
            return "stable"
        elif diff > 0.15:
            return "ascending"
        elif diff < -0.15:
            return "descending"
        else:
            return "wave"
