"""
Test the new modular architecture
Run with: python test_architecture.py
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from orchestrator.music_orchestrator import MusicOrchestrator


def test_orchestrator():
    """
    Test the orchestrator with a sample audio file
    """
    print("=" * 60)
    print("TESTING NEW MODULAR ARCHITECTURE")
    print("=" * 60)
    
    # You'll need a sample audio file - adjust path as needed
    audio_file = "uploads/test.mp3"  # Replace with actual file
    
    if not Path(audio_file).exists():
        print(f"❌ Test file not found: {audio_file}")
        print("   Please place a test audio file at this path")
        return False
    
    try:
        # Initialize orchestrator
        print("\n1️⃣  Initializing Orchestrator...")
        orchestrator = MusicOrchestrator()
        print("   ✅ All experts loaded")
        
        # Run analysis
        print(f"\n2️⃣  Analyzing: {audio_file}")
        print("-" * 60)
        music_state = orchestrator.analyze(audio_file)
        print("-" * 60)
        
        # Display results
        print("\n3️⃣  RESULTS:")
        print(f"\n   🥁 RHYTHM:")
        print(f"      BPM: {music_state.beat.bpm:.1f}")
        print(f"      Tempo: {music_state.beat.tempo_category.value}")
        print(f"      Regularity: {music_state.beat.beat_regularity:.2f}")
        print(f"      Time Signature: {music_state.beat.time_signature}")
        
        print(f"\n   🏗️  STRUCTURE:")
        print(f"      Sections: {music_state.structure.total_sections}")
        print(f"      Repetition: {music_state.structure.repetition_ratio:.2f}")
        print(f"      Pattern: {music_state.structure.pattern_type.value}")
        
        print(f"\n   ❤️  ENERGY:")
        print(f"      Overall: {music_state.energy.overall_energy.value}")
        print(f"      Buildup: {music_state.energy.has_buildup}")
        print(f"      Release: {music_state.energy.has_release}")
        print(f"      Arc: {music_state.energy.energy_arc}")
        
        print(f"\n   🧠 PATTERN LOGIC:")
        print(f"      Predictability: {music_state.pattern.predictability:.2f}")
        print(f"      Variation: {music_state.pattern.variation_level.value}")
        print(f"      Teaching Focus: {music_state.pattern.teaching_focus}")
        
        print(f"\n   🎯 HIGH-LEVEL:")
        print(f"      Primary: {music_state.primary_characteristic}")
        print(f"      Strategy: {music_state.learning_strategy}")
        print(f"      Complexity: {music_state.complexity_level.value}")
        
        print("\n✅ TEST PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_llm_service():
    """
    Test the LLM service (optional - requires model download)
    """
    print("\n" + "=" * 60)
    print("TESTING LOCAL LLM SERVICE")
    print("=" * 60)
    
    try:
        from services.local_llm_service import get_llm_service
        from orchestrator.music_orchestrator import MusicOrchestrator
        
        # Need a music state
        audio_file = "uploads/test.mp3"
        if not Path(audio_file).exists():
            print("⏭️  Skipping (no test file)")
            return True
        
        print("\n1️⃣  Getting MusicState from orchestrator...")
        orchestrator = MusicOrchestrator()
        music_state = orchestrator.analyze(audio_file)
        
        print("\n2️⃣  Loading LLM (may take a minute on first run)...")
        llm = get_llm_service(model_name="phi-2")
        
        print("\n3️⃣  Generating explanation...")
        explanation = llm.generate_explanation(music_state)
        
        print("\n📝 EXPLANATION:")
        print("-" * 60)
        print(explanation)
        print("-" * 60)
        
        print("\n✅ LLM TEST PASSED!")
        return True
        
    except Exception as e:
        print(f"\n⚠️  LLM TEST SKIPPED OR FAILED: {e}")
        print("   This is OK if you haven't downloaded the model yet")
        return False


if __name__ == "__main__":
    success = test_orchestrator()
    
    # LLM test is optional (requires model download)
    if success:
        try:
            test_llm_service()
        except KeyboardInterrupt:
            print("\n\n⏹️  LLM test cancelled by user")
