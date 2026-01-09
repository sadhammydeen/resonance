"""
Audio Analysis Engine
Extracts rhythm, structure, and emotional features from audio files
"""

import librosa
import numpy as np
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, asdict
import warnings

warnings.filterwarnings('ignore')


@dataclass
class BeatInfo:
    """Beat and tempo information"""
    bpm: float
    beat_times: List[float]
    time_signature: str
    total_beats: int


@dataclass
class StructureSection:
    """Musical section information"""
    name: str
    start_time: float
    end_time: float
    duration: float
    characteristics: str


@dataclass
class EmotionalFeature:
    """Emotional characteristics at a time point"""
    time: float
    energy: float  # 0-1: calm to energetic
    intensity: float  # 0-1: soft to loud
    tension: float  # 0-1: relaxed to tense
    label: str  # Human-readable emotion


@dataclass
class AudioAnalysisResult:
    """Complete analysis result"""
    beat_info: BeatInfo
    sections: List[StructureSection]
    emotional_timeline: List[EmotionalFeature]
    duration: float
    sample_rate: int


class AudioAnalyzer:
    """
    Analyzes audio files to extract rhythm, structure, and emotional features
    without requiring the listener to hear sound.
    """
    
    def __init__(self, sample_rate: int = 22050, hop_length: int = 512):
        self.sr = sample_rate
        self.hop_length = hop_length
    
    def analyze(self, audio_path: str) -> AudioAnalysisResult:
        """
        Complete audio analysis pipeline
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            AudioAnalysisResult with all extracted features
        """
        print(f"🎵 Loading audio: {audio_path}")
        y, sr = librosa.load(audio_path, sr=self.sr)
        duration = librosa.get_duration(y=y, sr=sr)
        
        print("🥁 Extracting beat patterns...")
        beat_info = self._extract_beats(y, sr)
        
        print("🏗️ Analyzing structure...")
        sections = self._extract_structure(y, sr, beat_info)
        
        print("❤️ Mapping emotional arc...")
        emotional_timeline = self._extract_emotions(y, sr, duration)
        
        return AudioAnalysisResult(
            beat_info=beat_info,
            sections=sections,
            emotional_timeline=emotional_timeline,
            duration=duration,
            sample_rate=sr
        )
    
    def _extract_beats(self, y: np.ndarray, sr: int) -> BeatInfo:
        """Extract beat and tempo patterns"""
        
        # Estimate tempo (BPM)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, hop_length=self.hop_length)
        
        # Convert beat frames to time
        beat_times = librosa.frames_to_time(beat_frames, sr=sr, hop_length=self.hop_length)
        
        # Estimate time signature (simple heuristic)
        # Check if beats cluster in groups of 3 or 4
        if len(beat_times) > 4:
            intervals = np.diff(beat_times)
            avg_interval = np.mean(intervals)
            # Simple 4/4 vs 3/4 detection
            time_sig = "4/4" if tempo > 100 else "3/4"
        else:
            time_sig = "4/4"
        
        return BeatInfo(
            bpm=float(tempo),
            beat_times=beat_times.tolist(),
            time_signature=time_sig,
            total_beats=len(beat_times)
        )
    
    def _extract_structure(self, y: np.ndarray, sr: int, beat_info: BeatInfo) -> List[StructureSection]:
        """
        Detect structural sections based on repetition and change
        """
        
        # Compute chromagram for harmonic analysis
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=self.hop_length)
        
        # Compute self-similarity matrix
        similarity = librosa.segment.recurrence_matrix(
            chroma,
            mode='affinity',
            metric='cosine'
        )
        
        # Detect boundaries
        boundaries_frames = librosa.segment.agglomerative(chroma, k=5)
        boundaries_time = librosa.frames_to_time(boundaries_frames, sr=sr, hop_length=self.hop_length)
        
        # Create sections with labels
        sections = []
        section_labels = ["Intro", "Verse", "Build", "Chorus", "Bridge", "Outro"]
        
        for i in range(len(boundaries_time) - 1):
            start = boundaries_time[i]
            end = boundaries_time[i + 1]
            duration = end - start
            
            # Analyze characteristics of this section
            start_frame = int(start * sr / self.hop_length)
            end_frame = int(end * sr / self.hop_length)
            section_chroma = chroma[:, start_frame:end_frame]
            
            # Determine characteristics
            energy = np.mean(section_chroma)
            variation = np.std(section_chroma)
            
            if energy > 0.5 and variation > 0.3:
                char = "High energy, dynamic"
            elif energy < 0.3:
                char = "Calm, minimal"
            else:
                char = "Moderate, steady"
            
            label = section_labels[min(i, len(section_labels) - 1)]
            
            sections.append(StructureSection(
                name=label,
                start_time=float(start),
                end_time=float(end),
                duration=float(duration),
                characteristics=char
            ))
        
        return sections
    
    def _extract_emotions(self, y: np.ndarray, sr: int, duration: float) -> List[EmotionalFeature]:
        """
        Map audio features to emotional characteristics over time
        """
        
        # Divide into segments (every 5 seconds)
        segment_duration = 5.0
        num_segments = int(np.ceil(duration / segment_duration))
        
        emotional_timeline = []
        
        for i in range(num_segments):
            start_time = i * segment_duration
            end_time = min((i + 1) * segment_duration, duration)
            
            # Extract segment
            start_sample = int(start_time * sr)
            end_sample = int(end_time * sr)
            segment = y[start_sample:end_sample]
            
            if len(segment) == 0:
                continue
            
            # Extract features
            # Energy: RMS energy
            rms = librosa.feature.rms(y=segment)[0]
            energy_val = float(np.mean(rms))
            
            # Intensity: Loudness
            loudness = librosa.amplitude_to_db(rms, ref=np.max)
            intensity_val = float(np.clip((np.mean(loudness) + 60) / 60, 0, 1))
            
            # Tension: Spectral centroid (brightness)
            centroid = librosa.feature.spectral_centroid(y=segment, sr=sr)[0]
            tension_val = float(np.clip(np.mean(centroid) / 4000, 0, 1))
            
            # Map to emotion label
            label = self._map_to_emotion(energy_val, intensity_val, tension_val)
            
            emotional_timeline.append(EmotionalFeature(
                time=start_time,
                energy=energy_val,
                intensity=intensity_val,
                tension=tension_val,
                label=label
            ))
        
        return emotional_timeline
    
    def _map_to_emotion(self, energy: float, intensity: float, tension: float) -> str:
        """Map numerical features to emotion labels"""
        
        avg = (energy + intensity + tension) / 3
        
        if avg < 0.3:
            if tension < 0.3:
                return "Calm & Peaceful"
            else:
                return "Tense & Quiet"
        elif avg < 0.6:
            if tension < 0.4:
                return "Moderate & Steady"
            else:
                return "Building Anticipation"
        else:
            if tension > 0.6:
                return "Intense & Climactic"
            else:
                return "Energetic & Joyful"
    
    def to_dict(self, result: AudioAnalysisResult) -> Dict[str, Any]:
        """Convert analysis result to dictionary for JSON serialization"""
        return {
            "duration": result.duration,
            "sample_rate": result.sample_rate,
            "beat_info": asdict(result.beat_info),
            "sections": [asdict(s) for s in result.sections],
            "emotional_timeline": [asdict(e) for e in result.emotional_timeline]
        }
