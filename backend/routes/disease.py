from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from models import DiseaseDetection, Farm, User
from schemas import DiseaseDetectionResponse
from auth import verify_token
from services.ml_service import predictor
import json

router = APIRouter(prefix="/disease", tags=["Disease Detection"])
security = HTTPBearer()

# Load treatment data
with open('data/disease_treatments.json', 'r') as f:
    treatments = json.load(f)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user = db.query(User).filter(User.id == payload.get("id")).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user

@router.post("/detect")
async def detect_disease(
    file: UploadFile = File(...),
    farm_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload plant leaf image and get disease prediction
    """
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    # Read image bytes
    image_bytes = await file.read()
    
    # Get prediction
    result = predictor.predict(image_bytes)
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        )
    
    disease_name = result["disease"]
    confidence = result["confidence"]
    
    # Get treatment info
    treatment_info = treatments.get(disease_name, {
        "treatment": "Treatment information not available for this disease.",
        "prevention": "Please consult a local agricultural expert."
    })
    
    # Save to database if farm_id provided
    if farm_id:
        # Verify farm belongs to user
        farm = db.query(Farm).filter(
            Farm.id == farm_id,
            Farm.user_id == current_user.id
        ).first()
        
        if not farm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Farm not found"
            )
        
        detection = DiseaseDetection(
            farm_id=farm_id,
            disease_name=disease_name,
            confidence=confidence,
            treatment=treatment_info["treatment"]
        )
        db.add(detection)
        db.commit()
        db.refresh(detection)
    
    return {
        "disease": disease_name,
        "confidence": confidence,
        "treatment": treatment_info["treatment"],
        "prevention": treatment_info["prevention"],
        "top_3_predictions": result.get("top_3", [])
    }

@router.get("/history/{farm_id}")
def get_detection_history(
    farm_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get disease detection history for a farm
    """
    # Verify farm belongs to user
    farm = db.query(Farm).filter(
        Farm.id == farm_id,
        Farm.user_id == current_user.id
    ).first()
    
    if not farm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farm not found"
        )
    
    detections = db.query(DiseaseDetection).filter(
        DiseaseDetection.farm_id == farm_id
    ).order_by(DiseaseDetection.timestamp.desc()).all()
    
    return detections