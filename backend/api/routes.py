"""
API Routes for audio analysis and music interpretation
"""

from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
import uuid
from typing import Optional

from analysis.audio_analyzer import AudioAnalyzer
from services.llm_service import ExplanationGenerator

# Create router
analysis_router = APIRouter()

# Initialize services
audio_analyzer = AudioAnalyzer()
explanation_generator = ExplanationGenerator()

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
        
        print(f"📁 Saved file: {file_path}")
        
        # Analyze audio
        print("🎵 Starting audio analysis...")
        analysis_result = audio_analyzer.analyze(str(file_path))
        
        # Convert to dict
        analysis_dict = audio_analyzer.to_dict(analysis_result)
        
        # Generate explanations
        print("🤖 Generating explanations...")
        explanations = explanation_generator.generate_full_explanation(
            analysis_dict,
            user_level=user_level
        )
        
        # Combine results
        response_data = {
            "file_id": file_id,
            "filename": file.filename,
            "analysis": analysis_dict,
            "explanations": explanations,
            "user_level": user_level
        }
        
        print("✅ Analysis complete!")
        return JSONResponse(content=response_data)
        
    except Exception as e:
        # Cleanup on error
        if file_path.exists():
            file_path.unlink()
        
        print(f"❌ Error during analysis: {e}")
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
