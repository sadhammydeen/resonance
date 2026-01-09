"""
Structure Expert
Detects sections, repetition, and musical structure using pattern analysis
"""

import librosa
import numpy as np
from typing import List

from schema.music_schema import (
    StructureAnalysis, 
    StructureSection, 
    PatternType
)


class StructureExpert:
    """
    Expert focused on musical structure and form
    Detects sections, repetition, and organizational patterns
    """
    
    def __init__(self, sample_rate: int = 22050, hop_length: int = 512):
        self.sr = sample_rate
        self.hop_length = hop_length
    
    def analyze(self, audio_path: str, duration: float) -> StructureAnalysis:
        """
        Extract structural information from audio
        
        Returns:
            StructureAnalysis with detected sections and patterns
        """
        # Load audio
        y, sr = librosa.load(audio_path, sr=self.sr)
        
        # Extract chroma features (harmonic content)
        chroma = librosa.feature.chroma_cqt(
            y=y, 
            sr=sr, 
            hop_length=self.hop_length
        )
        
        # Compute self-similarity matrix
        similarity_matrix = librosa.segment.recurrence_matrix(
            chroma,
            mode='affinity',
            metric='cosine'
        )
        
        # Detect section boundaries
        sections = self._detect_sections(y, sr, chroma, similarity_matrix)
        
        # Analyze repetition
        repetition_ratio = self._analyze_repetition(similarity_matrix)
        
        # Classify pattern type
        pattern_type = self._classify_pattern_type(sections, repetition_ratio)
        
        return StructureAnalysis(
            sections=sections,
            total_sections=len(sections),
            repetition_ratio=float(repetition_ratio),
            pattern_type=pattern_type
        )
    
    def _detect_sections(
        self, 
        y: np.ndarray, 
        sr: int, 
        chroma: np.ndarray,
        similarity_matrix: np.ndarray
    ) -> List[StructureSection]:
        """
        Detect section boundaries using segmentation
        """
        # Use agglomerative clustering to find sections
        # k=5 means try to find ~5 major sections
        boundaries_frames = librosa.segment.agglomerative(
            chroma, 
            k=5
        )
        
        # Convert to time
        boundaries_time = librosa.frames_to_time(
            boundaries_frames, 
            sr=sr, 
            hop_length=self.hop_length
        )
        
        # Create sections with analysis
        sections = []
        section_labels = ["Intro", "Verse", "Build", "Chorus", "Bridge", "Outro"]
        
        for i in range(len(boundaries_time) - 1):
            start = boundaries_time[i]
            end = boundaries_time[i + 1]
            duration = end - start
            
            # Extract features for this section
            start_frame = int(start * sr / self.hop_length)
            end_frame = int(end * sr / self.hop_length)
            
            # Ensure valid frame range
            start_frame = max(0, min(start_frame, chroma.shape[1] - 1))
            end_frame = max(start_frame + 1, min(end_frame, chroma.shape[1]))
            
            section_chroma = chroma[:, start_frame:end_frame]
            
            # Calculate similarity to other sections
            similarity_score = self._calculate_section_similarity(
                section_chroma, 
                chroma, 
                start_frame, 
                end_frame
            )
            
            # Count how many times this pattern repeats
            repetition_count = self._count_repetitions(
                section_chroma, 
                chroma
            )
            
            # Assign label
            label = section_labels[min(i, len(section_labels) - 1)]
            
            sections.append(StructureSection(
                name=label,
                start_time=float(start),
                end_time=float(end),
                duration=float(duration),
                repetition_count=repetition_count,
                similarity_score=float(similarity_score)
            ))
        
        return sections
    
    def _analyze_repetition(self, similarity_matrix: np.ndarray) -> float:
        """
        Analyze how much the music repeats
        
        Returns:
            0.0 (no repetition) to 1.0 (highly repetitive)
        """
        # Look at off-diagonal elements (similarity between different time points)
        # High off-diagonal values = high repetition
        
        n = similarity_matrix.shape[0]
        if n < 2:
            return 0.5
        
        # Mask out main diagonal
        mask = ~np.eye(n, dtype=bool)
        off_diagonal = similarity_matrix[mask]
        
        # Average similarity (excluding self-similarity)
        repetition_ratio = np.mean(off_diagonal)
        
        return float(repetition_ratio)
    
    def _classify_pattern_type(
        self, 
        sections: List[StructureSection], 
        repetition_ratio: float
    ) -> PatternType:
        """
        Classify the overall pattern type
        """
        # Calculate variation in section durations
        durations = [s.duration for s in sections]
        if len(durations) < 2:
            return PatternType.VARIED
        
        duration_std = np.std(durations)
        duration_mean = np.mean(durations)
        
        if duration_mean == 0:
            return PatternType.VARIED
        
        variation_coefficient = duration_std / duration_mean
        
        # Classify based on repetition and variation
        if repetition_ratio > 0.7 and variation_coefficient < 0.3:
            return PatternType.REPETITIVE
        elif repetition_ratio < 0.3 and variation_coefficient > 0.5:
            return PatternType.CHAOTIC
        elif repetition_ratio > 0.5:
            return PatternType.EVOLVING
        else:
            return PatternType.VARIED
    
    def _calculate_section_similarity(
        self,
        section_chroma: np.ndarray,
        full_chroma: np.ndarray,
        start_frame: int,
        end_frame: int
    ) -> float:
        """
        Calculate how similar this section is to other parts
        """
        if section_chroma.shape[1] == 0:
            return 0.5
        
        # Average chroma for this section
        section_avg = np.mean(section_chroma, axis=1, keepdims=True)
        
        # Compare to entire piece
        similarities = []
        window_size = section_chroma.shape[1]
        
        for i in range(0, full_chroma.shape[1] - window_size, window_size):
            # Skip self
            if i >= start_frame and i < end_frame:
                continue
            
            window = full_chroma[:, i:i+window_size]
            if window.shape[1] == 0:
                continue
            
            window_avg = np.mean(window, axis=1, keepdims=True)
            
            # Cosine similarity
            sim = np.dot(section_avg.T, window_avg) / (
                np.linalg.norm(section_avg) * np.linalg.norm(window_avg) + 1e-8
            )
            similarities.append(float(sim[0, 0]))
        
        if not similarities:
            return 0.5
        
        return np.mean(similarities)
    
    def _count_repetitions(
        self,
        section_chroma: np.ndarray,
        full_chroma: np.ndarray,
        threshold: float = 0.7
    ) -> int:
        """
        Count how many times this section pattern repeats
        """
        if section_chroma.shape[1] == 0:
            return 1
        
        section_avg = np.mean(section_chroma, axis=1, keepdims=True)
        window_size = section_chroma.shape[1]
        
        repetitions = 1  # Count itself
        
        for i in range(0, full_chroma.shape[1] - window_size, window_size // 2):
            window = full_chroma[:, i:i+window_size]
            if window.shape[1] < window_size:
                continue
            
            window_avg = np.mean(window, axis=1, keepdims=True)
            
            # Cosine similarity
            sim = np.dot(section_avg.T, window_avg) / (
                np.linalg.norm(section_avg) * np.linalg.norm(window_avg) + 1e-8
            )
            
            if float(sim[0, 0]) > threshold:
                repetitions += 1
        
        return min(repetitions, 10)  # Cap at 10 for sanity
