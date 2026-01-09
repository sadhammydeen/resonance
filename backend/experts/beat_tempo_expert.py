"""
Beat & Tempo Expert
Analyzes rhythm, tempo, and beat patterns using signal processing (DSP)
"""

import librosa
import numpy as np
from typing import Tuple

from schema.music_schema import BeatAnalysis, TempoCategory, IntensityLevel


class BeatTempoExpert:
    """
    Expert focused on rhythmic analysis
    Uses DSP (no ML) for precise, reproducible results
    """
    
    def __init__(self, sample_rate: int = 22050, hop_length: int = 512):
        self.sr = sample_rate
        self.hop_length = hop_length
    
    def analyze(self, audio_path: str) -> BeatAnalysis:
        """
        Extract beat and tempo information from audio
        
        Returns:
            BeatAnalysis with all rhythm metrics
        """
        # Load audio
        y, sr = librosa.load(audio_path, sr=self.sr)
        
        # Extract tempo and beats
        tempo, beat_frames = librosa.beat.beat_track(
            y=y, 
            sr=sr, 
            hop_length=self.hop_length,
            units='frames'
        )
        
        # Convert beat frames to time
        beat_times = librosa.frames_to_time(
            beat_frames, 
            sr=sr, 
            hop_length=self.hop_length
        )
        
        # Analyze beat regularity
        beat_regularity = self._calculate_beat_regularity(beat_times)
        
        # Categorize tempo
        tempo_category = self._categorize_tempo(tempo)
        
        # Calculate beat density
        beat_density = self._calculate_beat_density(beat_times, y, sr)
        
        # Estimate time signature (simple heuristic)
        time_signature = self._estimate_time_signature(tempo, beat_times)
        
        return BeatAnalysis(
            bpm=float(tempo),
            tempo_category=tempo_category,
            beat_times=beat_times.tolist(),
            beat_regularity=float(beat_regularity),
            beat_density=beat_density,
            total_beats=len(beat_times),
            time_signature=time_signature
        )
    
    def _calculate_beat_regularity(self, beat_times: np.ndarray) -> float:
        """
        Calculate how regular/steady the beat is
        
        Returns:
            0.0 (very irregular) to 1.0 (perfectly steady)
        """
        if len(beat_times) < 3:
            return 0.5  # Not enough data
        
        # Calculate intervals between beats
        intervals = np.diff(beat_times)
        
        # Calculate coefficient of variation (lower = more regular)
        mean_interval = np.mean(intervals)
        std_interval = np.std(intervals)
        
        if mean_interval == 0:
            return 0.5
        
        cv = std_interval / mean_interval
        
        # Convert to 0-1 scale (lower CV = higher regularity)
        # CV of 0.1 or less = very regular (0.9+)
        # CV of 0.3 or more = irregular (0.5 or less)
        regularity = max(0.0, min(1.0, 1.0 - (cv / 0.3)))
        
        return regularity
    
    def _categorize_tempo(self, bpm: float) -> TempoCategory:
        """
        Convert BPM to human-readable tempo category
        """
        if bpm < 60:
            return TempoCategory.VERY_SLOW
        elif bpm < 90:
            return TempoCategory.SLOW
        elif bpm < 120:
            return TempoCategory.MODERATE
        elif bpm < 150:
            return TempoCategory.FAST
        else:
            return TempoCategory.VERY_FAST
    
    def _calculate_beat_density(
        self, 
        beat_times: np.ndarray, 
        y: np.ndarray, 
        sr: int
    ) -> IntensityLevel:
        """
        Calculate how "dense" the rhythm is
        Looks at onset density (how many sound events per beat)
        """
        # Detect onsets (sound events)
        onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=self.hop_length)
        onset_frames = librosa.onset.onset_detect(
            onset_envelope=onset_env,
            sr=sr,
            hop_length=self.hop_length,
            backtrack=True
        )
        onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=self.hop_length)
        
        # Calculate onsets per beat
        if len(beat_times) < 2:
            return IntensityLevel.MEDIUM
        
        duration = beat_times[-1] - beat_times[0]
        onsets_per_second = len(onset_times) / duration if duration > 0 else 0
        
        # Categorize density
        if onsets_per_second < 3:
            return IntensityLevel.LOW
        elif onsets_per_second < 6:
            return IntensityLevel.MEDIUM
        else:
            return IntensityLevel.HIGH
    
    def _estimate_time_signature(self, tempo: float, beat_times: np.ndarray) -> str:
        """
        Simple time signature estimation
        More sophisticated methods would use onset patterns
        """
        # This is a simplified heuristic
        # Real implementation would analyze onset patterns
        
        if tempo < 100:
            # Slower songs often in 3/4 or 6/8
            return "3/4"
        else:
            # Most songs in 4/4
            return "4/4"
