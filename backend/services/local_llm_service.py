"""
Local LLM Service
Uses small HuggingFace model for explanation generation
NO analysis - only natural language generation from structured data
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from typing import Optional
import logging

from schema.music_schema import MusicState, ExplanationContext

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LocalLLMService:
    """
    Service for generating explanations using local HuggingFace models
    Uses small models (1-3B parameters) that can run on consumer hardware
    """
    
    # Recommended models (sorted by quality/size tradeoff)
    RECOMMENDED_MODELS = {
        "phi-2": "microsoft/phi-2",  # 2.7B, excellent quality
        "tinyllama": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",  # 1.1B, fast
        "flan-t5-base": "google/flan-t5-base",  # 250M, very fast
    }
    
    def __init__(
        self, 
        model_name: str = "phi-2",
        device: Optional[str] = None,
        max_length: int = 300
    ):
        """
        Initialize local LLM
        
        Args:
            model_name: Key from RECOMMENDED_MODELS or full HuggingFace model ID
            device: "cuda", "cpu", or None (auto-detect)
            max_length: Maximum tokens for explanation
        """
        self.max_length = max_length
        
        # Get model ID
        self.model_id = self.RECOMMENDED_MODELS.get(model_name, model_name)
        
        # Auto-detect device
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
        
        logger.info(f"🤖 Loading model: {self.model_id}")
        logger.info(f"   Device: {self.device}")
        
        # Load model and tokenizer
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
                trust_remote_code=True  # Required for some models like Phi-2
            )
            
            if self.device == "cpu":
                self.model = self.model.to(self.device)
            
            # Create generation pipeline
            self.pipe = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_new_tokens=max_length,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                device=0 if self.device == "cuda" else -1
            )
            
            logger.info("✅ Model loaded successfully!")
            
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            raise
    
    def generate_explanation(self, music_state: MusicState) -> str:
        """
        Generate accessible explanation from MusicState
        
        Args:
            music_state: Complete analysis from orchestrator
            
        Returns:
            Natural language explanation (no sound references)
        """
        # Convert to simplified context
        context = self._create_explanation_context(music_state)
        
        # Build prompt
        prompt = self._build_prompt(context)
        
        # Generate explanation
        try:
            logger.info("🎨 Generating explanation...")
            result = self.pipe(prompt)[0]['generated_text']
            
            # Extract only the generated part (remove prompt)
            explanation = result[len(prompt):].strip()
            
            # Post-process to ensure quality
            explanation = self._post_process(explanation)
            
            logger.info("✅ Explanation generated!")
            return explanation
            
        except Exception as e:
            logger.error(f"❌ Generation failed: {e}")
            return self._fallback_explanation(context)
    
    def _create_explanation_context(self, state: MusicState) -> ExplanationContext:
        """
        Convert full MusicState to simplified ExplanationContext
        This is what the LLM actually sees
        """
        # Simplify tempo
        tempo_bucket = state.beat.tempo_category.value
        
        # Simplify energy
        energy_bucket = state.energy.overall_energy.value
        
        # Simplify structure
        if state.structure.repetition_ratio > 0.7:
            structure_bucket = "highly_repetitive"
        elif state.structure.repetition_ratio > 0.4:
            structure_bucket = "moderately_varied"
        else:
            structure_bucket = "constantly_changing"
        
        # Simplify pattern
        if state.pattern.predictability > 0.7:
            pattern_bucket = "predictable"
        elif state.pattern.predictability > 0.4:
            pattern_bucket = "somewhat_predictable"
        else:
            pattern_bucket = "surprising"
        
        return ExplanationContext(
            tempo=tempo_bucket,
            energy=energy_bucket,
            structure=structure_bucket,
            pattern=pattern_bucket,
            primary_focus=state.primary_characteristic,
            teaching_strategy=state.learning_strategy,
            complexity=state.complexity_level.value
        )
    
    def _build_prompt(self, context: ExplanationContext) -> str:
        """
        Build prompt for explanation generation
        Critical: NO sound references, use visual/tactile metaphors
        """
        prompt = f"""You are explaining music to someone who cannot hear. Use only visual, tactile, or physical metaphors.

Music Analysis:
- Tempo: {context.tempo}
- Energy: {context.energy}
- Structure: {context.structure}
- Patterns: {context.pattern}
- Focus: {context.primary_focus}

Teaching Strategy: {context.teaching_strategy}

Generate a short, accessible explanation using:
- Visual metaphors (waves, colors, shapes)
- Physical sensations (tension, release, weight)
- Patterns and rhythms (breathing, heartbeat, walking)

NO sound words. Keep it under 150 words.

Explanation:"""
        
        return prompt
    
    def _post_process(self, text: str) -> str:
        """
        Clean up generated text
        """
        # Remove incomplete sentences
        sentences = text.split('.')
        complete_sentences = [s.strip() + '.' for s in sentences if len(s.strip()) > 10]
        
        # Take first few complete sentences
        result = ' '.join(complete_sentences[:4])
        
        # Remove sound-related words (safety check)
        sound_words = ['sound', 'hear', 'listen', 'audio', 'noise', 'loud', 'quiet', 'silent']
        for word in sound_words:
            result = result.replace(word, '[sensation]')
        
        return result
    
    def _fallback_explanation(self, context: ExplanationContext) -> str:
        """
        Fallback explanation if LLM fails
        Template-based, always works
        """
        templates = {
            "rhythm_focused": "This music has a strong, steady pulse - like a heartbeat you can feel. {energy_desc} {structure_desc}",
            "repetition_driven": "Patterns repeat consistently, creating familiarity - like waves returning to shore. {energy_desc}",
            "energy_driven": "Energy flows through the piece like a wave - building tension, then releasing. {pattern_desc}",
            "structure_complex": "The music is organized into distinct sections, each with its own character. {energy_desc}",
            "balanced": "This piece balances rhythm, energy, and structure. {strategy}"
        }
        
        template = templates.get(context.primary_focus, templates["balanced"])
        
        # Fill in energy description
        energy_map = {
            "low": "It stays calm and relaxed throughout.",
            "medium": "Energy stays moderate, creating comfortable tension.",
            "high": "Intense energy keeps things dynamic."
        }
        
        # Fill in structure description
        structure_map = {
            "highly_repetitive": "The same patterns return again and again.",
            "moderately_varied": "Patterns evolve while maintaining continuity.",
            "constantly_changing": "Each moment brings something new."
        }
        
        # Fill in pattern description
        pattern_map = {
            "predictable": "You can anticipate what comes next.",
            "somewhat_predictable": "Some surprises break the expected flow.",
            "surprising": "Unexpected changes keep you engaged."
        }
        
        return template.format(
            energy_desc=energy_map.get(context.energy, ""),
            structure_desc=structure_map.get(context.structure, ""),
            pattern_desc=pattern_map.get(context.pattern, ""),
            strategy=context.teaching_strategy
        )


# Singleton instance
_llm_service: Optional[LocalLLMService] = None


def get_llm_service(
    model_name: str = "phi-2",
    force_reload: bool = False
) -> LocalLLMService:
    """
    Get or create LLM service singleton
    Model is loaded once and reused
    
    Args:
        model_name: Model to use (phi-2, tinyllama, flan-t5-base)
        force_reload: Force reload model (for testing)
    """
    global _llm_service
    
    if _llm_service is None or force_reload:
        _llm_service = LocalLLMService(model_name=model_name)
    
    return _llm_service
