from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.models.prediction import Prediction
from app.models.chatbot import ChatSession, ChatMessage
from app.services.auth_service import get_current_user
from app.services.chatbot_service import generate_chatbot_response

router = APIRouter(prefix="/chat", tags=["AI Chatbot"])

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    session_id: Optional[int] = None
    prediction_id: Optional[int] = None

class ChatResponse(BaseModel):
    session_id: int
    sender: str
    message: str
    language: str
    is_refusal: bool

@router.post("/general", response_model=ChatResponse)
async def general_farmer_chat(
    req: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Retrieve or create general chat session
    session = None
    if req.session_id:
        session = db.query(ChatSession).filter(
            ChatSession.id == req.session_id,
            ChatSession.user_id == current_user.id
        ).first()

    if not session:
        session = ChatSession(user_id=current_user.id, session_type="general")
        db.add(session)
        db.commit()
        db.refresh(session)

    # Save user message
    user_msg = ChatMessage(
        session_id=session.id,
        sender="user",
        message=req.message
    )
    db.add(user_msg)
    db.commit()

    # Generate AI response
    ai_result = await generate_chatbot_response(query=req.message)

    # Save AI response
    ai_msg = ChatMessage(
        session_id=session.id,
        sender="ai",
        language=ai_result["language"],
        message=ai_result["response"]
    )
    db.add(ai_msg)
    db.commit()

    return ChatResponse(
        session_id=session.id,
        sender="ai",
        message=ai_result["response"],
        language=ai_result["language"],
        is_refusal=ai_result["is_refusal"]
    )

@router.post("/prediction", response_model=ChatResponse)
async def prediction_specific_chat(
    req: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not req.prediction_id:
        raise HTTPException(status_code=400, detail="prediction_id is required for prediction assistant.")

    prediction = db.query(Prediction).filter(
        Prediction.id == req.prediction_id,
        Prediction.user_id == current_user.id
    ).first()

    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction record not found.")

    # Retrieve or create session
    session = None
    if req.session_id:
        session = db.query(ChatSession).filter(
            ChatSession.id == req.session_id,
            ChatSession.user_id == current_user.id
        ).first()

    if not session:
        session = ChatSession(
            user_id=current_user.id,
            session_type="prediction",
            prediction_id=prediction.id
        )
        db.add(session)
        db.commit()
        db.refresh(session)

    # Save user message
    user_msg = ChatMessage(
        session_id=session.id,
        sender="user",
        message=req.message
    )
    db.add(user_msg)
    db.commit()

    # Build farm context
    crop = prediction.crop
    farm_context = {
        "crop": crop.name_en,
        "crop_ta": crop.name_ta,
        "district": prediction.district.name_en,
        "taluk": prediction.taluk.name_en if prediction.taluk else "",
        "pattam": prediction.pattam,
        "land_area_acres": prediction.land_area_acres,
        "predicted_yield_per_acre": prediction.predicted_yield_per_acre,
        "total_production_kg": prediction.total_production_kg,
        "soil_ph": prediction.soil_ph,
        "soil_n": prediction.soil_n,
        "soil_p": prediction.soil_p,
        "soil_k": prediction.soil_k,
        "temperature": prediction.temperature,
        "rainfall_mm": prediction.rainfall_mm,
        "weather_condition": prediction.weather_condition,
        "factors_summary": prediction.factors_summary
    }

    # Generate response
    ai_result = await generate_chatbot_response(query=req.message, context=farm_context)

    # Save AI message
    ai_msg = ChatMessage(
        session_id=session.id,
        sender="ai",
        language=ai_result["language"],
        message=ai_result["response"]
    )
    db.add(ai_msg)
    db.commit()

    return ChatResponse(
        session_id=session.id,
        sender="ai",
        message=ai_result["response"],
        language=ai_result["language"],
        is_refusal=ai_result["is_refusal"]
    )

@router.get("/history/{session_id}")
def get_chat_history(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found.")

    return [
        {
            "id": m.id,
            "sender": m.sender,
            "message": m.message,
            "language": m.language,
            "timestamp": m.timestamp.strftime("%Y-%m-%d %H:%M")
        }
        for m in session.messages
    ]
