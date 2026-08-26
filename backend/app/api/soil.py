import os
import uuid
import aiofiles
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.config import settings
from app.database.session import get_db
from app.models.user import User
from app.models.soil_report import SoilReport
from app.services.auth_service import get_current_user
from app.services.soil_service import parse_soil_file

router = APIRouter(prefix="/soil", tags=["Soil Report"])

ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png", "webp"}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

@router.post("/upload")
async def upload_soil_report(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    filename = file.filename
    ext = filename.split(".")[-1].lower() if "." in filename else ""

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type .{ext}. Only PDF, JPG, JPEG, and PNG files are supported."
        )

    # Read and validate size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="File size exceeds maximum 10MB limit.")

    unique_filename = f"soil_{current_user.id}_{uuid.uuid4().hex[:8]}.{ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as f:
        f.write(content)

    # Parse and extract soil parameters
    parsed_data = parse_soil_file(file_path, ext)

    # Save to database
    report = SoilReport(
        user_id=current_user.id,
        file_name=filename,
        file_path=file_path,
        file_type=ext,
        soil_type=parsed_data.get("soil_type", "Red Loam"),
        ph=parsed_data.get("ph", 6.8),
        ec=parsed_data.get("ec", 0.45),
        organic_carbon=parsed_data.get("organic_carbon", 0.65),
        nitrogen=parsed_data.get("nitrogen", 250.0),
        phosphorus=parsed_data.get("phosphorus", 18.0),
        potassium=parsed_data.get("potassium", 210.0),
        micronutrients=parsed_data.get("micronutrients", {}),
        raw_extracted_text=parsed_data.get("raw_text", "")
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    return {
        "report_id": report.id,
        "file_name": filename,
        "extracted_parameters": parsed_data,
        "message_en": "Soil report uploaded and analyzed successfully. You may verify and edit values if needed before predicting.",
        "message_ta": "மண் பரிசோதனை அறிக்கை வெற்றிகரமாக ஆய்வு செய்யப்பட்டது. மகசூல் கணிப்பதற்கு முன் மதிப்புகளை சரிபார்த்துக் கொள்ளலாம்."
    }

@router.get("/my-reports")
def get_my_soil_reports(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    reports = db.query(SoilReport).filter(SoilReport.user_id == current_user.id).order_by(SoilReport.created_at.desc()).all()
    return [
        {
            "id": r.id,
            "file_name": r.file_name,
            "soil_type": r.soil_type,
            "ph": r.ph,
            "nitrogen": r.nitrogen,
            "phosphorus": r.phosphorus,
            "potassium": r.potassium,
            "organic_carbon": r.organic_carbon,
            "ec": r.ec,
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M")
        }
        for r in reports
    ]
