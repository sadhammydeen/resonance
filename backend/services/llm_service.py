"""
LLM Service for generating human-readable music explanations
Uses OpenAI API to translate technical analysis into accessible language
"""

from openai import OpenAI
from typing import Dict, Any, Optional
import json

from services.config import settings


class ExplanationGenerator:
    """
    Generates natural language explanations of music structure
    for learners who don't need to hear sound.
    """
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
        self.model = settings.OPENAI_MODEL
    
    def generate_full_explanation(
        self,
        analysis_data: Dict[str, Any],
        user_level: str = "beginner"
    ) -> Dict[str, str]:
        """
        Generate comprehensive explanations for all aspects of the music
        
        Args:
            analysis_data: Complete audio analysis result
            user_level: "beginner", "intermediate", or "advanced"
            
        Returns:
            Dictionary with explanation sections
        """
        
        if not self.client:
            return self._generate_fallback_explanation(analysis_data)
        
        try:
            # Create structured prompt
            prompt = self._build_explanation_prompt(analysis_data, user_level)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are a music education specialist helping deaf and neurodivergent learners understand music through visual and structural patterns, NOT sound.

Key principles:
- Never reference listening or hearing
- Use visual metaphors (footsteps, waves, heartbeat)
- Focus on patterns, repetition, structure
- Be encouraging and accessible
- Use simple, clear language"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            explanation_text = response.choices[0].message.content
            
            # Parse into sections
            return self._parse_explanation(explanation_text)
            
        except Exception as e:
            print(f"❌ LLM error: {e}")
            return self._generate_fallback_explanation(analysis_data)
    
    def _build_explanation_prompt(self, data: Dict[str, Any], level: str) -> str:
        """Build the prompt for LLM"""
        
        beat_info = data["beat_info"]
        sections = data["sections"]
        emotions = data["emotional_timeline"]
        
        prompt = f"""Explain this music to a {level} learner who experiences music WITHOUT SOUND.

**Music Data:**
- Tempo: {beat_info['bpm']:.1f} BPM ({self._tempo_description(beat_info['bpm'])})
- Total Beats: {beat_info['total_beats']}
- Time Signature: {beat_info['time_signature']}
- Duration: {data['duration']:.1f} seconds

**Structure Sections:**
{self._format_sections(sections)}

**Emotional Journey:**
{self._format_emotions(emotions)}

Provide explanations in these sections (use ### headers):

### Overview
Brief description of the overall structure and feeling

### Rhythm Pattern
Explain the beat pattern using visual metaphors (like footsteps, waves)

### Structure
How the sections connect and why repetition/variation matters

### Emotional Arc
The emotional journey from start to finish

### Learning Focus
What pattern should the learner focus on first?

Keep it simple, encouraging, and visual. No sound references."""
        
        return prompt
    
    def _tempo_description(self, bpm: float) -> str:
        """Convert BPM to descriptive speed"""
        if bpm < 60:
            return "very slow, like a slow walk"
        elif bpm < 90:
            return "slow, like a relaxed walk"
        elif bpm < 120:
            return "moderate, like a brisk walk"
        elif bpm < 150:
            return "fast, like a jog"
        else:
            return "very fast, like running"
    
    def _format_sections(self, sections: list) -> str:
        """Format sections for prompt"""
        lines = []
        for i, sec in enumerate(sections, 1):
            lines.append(
                f"{i}. {sec['name']} ({sec['start_time']:.1f}s - {sec['end_time']:.1f}s): {sec['characteristics']}"
            )
        return "\n".join(lines)
    
    def _format_emotions(self, emotions: list) -> str:
        """Format emotional timeline for prompt"""
        lines = []
        for emo in emotions:
            lines.append(
                f"- {emo['time']:.1f}s: {emo['label']} (energy: {emo['energy']:.2f}, tension: {emo['tension']:.2f})"
            )
        return "\n".join(lines)
    
    def _parse_explanation(self, text: str) -> Dict[str, str]:
        """Parse LLM response into structured sections"""
        
        sections = {
            "overview": "",
            "rhythm_pattern": "",
            "structure": "",
            "emotional_arc": "",
            "learning_focus": ""
        }
        
        # Split by headers
        parts = text.split("###")
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            lines = part.split("\n", 1)
            if len(lines) < 2:
                continue
            
            header = lines[0].strip().lower()
            content = lines[1].strip()
            
            if "overview" in header:
                sections["overview"] = content
            elif "rhythm" in header:
                sections["rhythm_pattern"] = content
            elif "structure" in header:
                sections["structure"] = content
            elif "emotion" in header:
                sections["emotional_arc"] = content
            elif "learning" in header or "focus" in header:
                sections["learning_focus"] = content
        
        return sections
    
    def _generate_fallback_explanation(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Generate basic explanations without LLM"""
        
        beat_info = data["beat_info"]
        bpm = beat_info["bpm"]
        
        return {
            "overview": f"This music has {beat_info['total_beats']} beats over {data['duration']:.1f} seconds, moving at {bpm:.0f} beats per minute.",
            
            "rhythm_pattern": f"The rhythm moves at {self._tempo_description(bpm)}. Think of it like {self._get_rhythm_metaphor(bpm)}.",
            
            "structure": f"The music is divided into {len(data['sections'])} main sections, each with its own character and purpose.",
            
            "emotional_arc": self._simple_emotion_arc(data["emotional_timeline"]),
            
            "learning_focus": "Start by following the beat pattern - it's the foundation of the music's structure."
        }
    
    def _get_rhythm_metaphor(self, bpm: float) -> str:
        """Get visual metaphor for tempo"""
        if bpm < 60:
            return "a slow, steady heartbeat at rest"
        elif bpm < 90:
            return "footsteps in a calm walk"
        elif bpm < 120:
            return "waves lapping at a beach"
        elif bpm < 150:
            return "a quick jog or energetic dance"
        else:
            return "rapid drumming or intense movement"
    
    def _simple_emotion_arc(self, emotions: list) -> str:
        """Create simple emotion arc description"""
        if not emotions:
            return "The emotional journey is steady throughout."
        
        labels = [e["label"] for e in emotions]
        
        if len(set(labels)) == 1:
            return f"The music maintains a {labels[0].lower()} feeling throughout."
        
        return f"The music moves from {labels[0].lower()} to {labels[-1].lower()}, with changes along the way."
