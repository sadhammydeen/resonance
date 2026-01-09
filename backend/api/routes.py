"""
API Routes for audio analysis and music interpretation
NEW ARCHITECTURE: Uses expert system + local LLM
"""

from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
import uuid
from typing import Optional
import logging

from orchestrator.music_orchestrator import MusicOrchestrator
from services.local_llm_service import get_llm_service

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
analysis_router = APIRouter()

# Initialize orchestrator (expert system coordinator)
orchestrator = MusicOrchestrator()

# LLM service (lazy-loaded on first request)
llm_service = None

# Upload directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@analysis_router.post("/analyze")
async def analyze_audio(
    file: UploadFile = File(...),
    user_level: str = Form("beginner")
):
    """
    Analyze uploaded audio file and generate visual interpretations
    
    Args:
        file: Audio file (MP3, WAV, M4A)
        user_level: Learning level (beginner, intermediate, advanced)
        
    Returns:
        Complete analysis with rhythm maps, emotion timeline, and explanations
    """
    
    # Validate file extension
    file_ext = file.filename.split(".")[-1].lower()
    allowed_extensions = ["mp3", "wav", "m4a"]
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not supported. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Save uploaded file
    file_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{file_id}.{file_ext}"
    
    try:
        # Save file
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"📁 Saved file: {file_path}")
        
        # === NEW ARCHITECTURE ===
        # Step 1: Orchestrator coordinates all experts
        logger.info("🎵 Starting expert analysis...")
        music_state = orchestrator.analyze(str(file_path))
        
        # Step 2: Get LLM service (lazy-loaded)
        global llm_service
        if llm_service is None:
            logger.info("🤖 Loading LLM (first request only)...")
            llm_service = get_llm_service(model_name="phi-2")
        
        # Step 3: Generate explanation using local LLM
        logger.info("🎨 Generating explanation...")
        explanation = llm_service.generate_explanation(music_state)
        
        # Step 4: Convert to API response format
        response_data = {
            "file_id": file_id,
            "filename": file.filename,
            "analysis": {
                # Beat & Tempo
                "rhythm": {
                    "bpm": music_state.beat.bpm,
                    "tempo_category": music_state.beat.tempo_category.value,
                    "regularity": music_state.beat.beat_regularity,
                    "density": music_state.beat.beat_density.value,
                    "time_signature": music_state.beat.time_signature,
                    "beat_positions": music_state.beat.beat_positions[:20]  # First 20 beats
                },
                
                # Structure
                "structure": {
                    "total_sections": music_state.structure.total_sections,
                    "repetition_ratio": music_state.structure.repetition_ratio,
                    "pattern_type": music_state.structure.pattern_type.value,
                    "sections": [
                        {
                            "start": s.start_time,
                            "end": s.end_time,
                            "similarity": s.similarity_score
                        }
                        for s in music_state.structure.sections
                    ]
                },
                
                # Energy
                "energy": {
                    "overall": music_state.energy.overall_energy.value,
                    "has_buildup": music_state.energy.has_buildup,
                    "has_release": music_state.energy.has_release,
                    "arc": music_state.energy.energy_arc,
                    "timeline": [
                        {
                            "time": m.time,
                            "level": m.energy_level.value,
                            "intensity": m.intensity,
                            "tension": m.tension
                        }
                        for m in music_state.energy.timeline
                    ]
                },
                
                # Pattern Logic
                "pattern": {
                    "predictability": music_state.pattern.predictability,
                    "variation": music_state.pattern.variation_level.value,
                    "repetition_strength": music_state.pattern.repetition_strength,
                    "surprise_moments": music_state.pattern.surprise_moments,
                    "teaching_focus": music_state.pattern.teaching_focus
                },
                
                # High-Level Insights
                "insights": {
                    "primary_characteristic": music_state.primary_characteristic,
                    "learning_strategy": music_state.learning_strategy,
                    "complexity": music_state.complexity_level.value
                }
            },
            
            "explanation": explanation,
            "user_level": user_level
        }
        
        logger.info("✅ Analysis complete!")
        return JSONResponse(content=response_data)
        
    except Exception as e:
        # Cleanup on error
        if file_path.exists():
            file_path.unlink()
        
        logger.error(f"❌ Error during analysis: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing audio: {str(e)}"
        )
    
    finally:
        # Optional: cleanup uploaded file after analysis
        # Uncomment to delete files immediately after processing
        # if file_path.exists():
        #     file_path.unlink()
        pass


@analysis_router.post("/feedback")
async def submit_feedback(
    file_id: str = Form(...),
    understanding: str = Form(...),
    comment: Optional[str] = Form(None)
):
    """
    Collect user feedback for adaptive learning
    
    Args:
        file_id: ID of analyzed file
        understanding: "yes", "somewhat", "no"
        comment: Optional user comment
        
    Returns:
        Confirmation and adapted explanation if needed
    """
    
    # Validate understanding value
    if understanding not in ["yes", "somewhat", "no"]:
        raise HTTPException(
            status_code=400,
            detail="understanding must be 'yes', 'somewhat', or 'no'"
        )
    
    # Store feedback (in a real app, save to database)
    feedback_data = {
        "file_id": file_id,
        "understanding": understanding,
        "comment": comment
    }
    
    # Adaptive response
    response = {
        "feedback_received": True,
        "file_id": file_id
    }
    
    if understanding == "no":
        response["suggestion"] = {
            "message": "Let's try a different approach!",
            "next_steps": [
                "Focus on just the beat pattern first",
                "Use more visual metaphors",
                "Break down into smaller sections"
            ]
        }
    elif understanding == "somewhat":
        response["suggestion"] = {
            "message": "You're on the right track!",
            "next_steps": [
                "Review the emotion timeline",
                "Compare repeated sections",
                "Practice identifying patterns"
            ]
        }
    else:
        response["suggestion"] = {
            "message": "Excellent! Ready for the next challenge?",
            "next_steps": [
                "Try analyzing a more complex song",
                "Focus on structural variations",
                "Explore advanced patterns"
            ]
        }
    
    return JSONResponse(content=response)


@analysis_router.get("/history")
async def get_analysis_history():
    """
    Get list of previously analyzed files
    
    Returns:
        List of file IDs and metadata
    """
    
    # In MVP, just list uploaded files
    files = list(UPLOAD_DIR.glob("*"))
    
    history = []
    for file in files:
        history.append({
            "file_id": file.stem,
            "extension": file.suffix,
            "size_mb": file.stat().st_size / (1024 * 1024)
        })
    
    return JSONResponse(content={"history": history, "count": len(history)})
