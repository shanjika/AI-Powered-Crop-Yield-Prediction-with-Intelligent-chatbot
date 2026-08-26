from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.models.location import District, Taluk
from app.schemas.auth import UserSignup, UserLogin, UserOut, Token
from app.services.auth_service import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=Token)
def signup(user_in: UserSignup, db: Session = Depends(get_db)):
    # Check mobile number uniqueness
    existing_phone = db.query(User).filter(User.mobile_number == user_in.mobile_number).first()
    if existing_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mobile number is already registered. Please login instead."
        )

    # Check email uniqueness if provided
    if user_in.email:
        existing_email = db.query(User).filter(User.email == user_in.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email address is already registered."
            )

    user = User(
        full_name=user_in.full_name,
        mobile_number=user_in.mobile_number,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        preferred_language=user_in.preferred_language,
        district_id=user_in.district_id,
        taluk_id=user_in.taluk_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id)})
    
    district_name = user.district.name_en if user.district else None
    taluk_name = user.taluk.name_en if user.taluk else None

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserOut(
            id=user.id,
            full_name=user.full_name,
            mobile_number=user.mobile_number,
            email=user.email,
            preferred_language=user.preferred_language,
            district_id=user.district_id,
            taluk_id=user.taluk_id,
            district_name=district_name,
            taluk_name=taluk_name
        )
    }

@router.post("/login", response_model=Token)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    # Accept mobile number or email
    user = db.query(User).filter(
        (User.mobile_number == login_data.username) | (User.email == login_data.username)
    ).first()

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid mobile number/email or password."
        )

    token = create_access_token({"sub": str(user.id)})
    district_name = user.district.name_en if user.district else None
    taluk_name = user.taluk.name_en if user.taluk else None

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserOut(
            id=user.id,
            full_name=user.full_name,
            mobile_number=user.mobile_number,
            email=user.email,
            preferred_language=user.preferred_language,
            district_id=user.district_id,
            taluk_id=user.taluk_id,
            district_name=district_name,
            taluk_name=taluk_name
        )
    }

@router.get("/me", response_model=UserOut)
def get_profile(current_user: User = Depends(get_current_user)):
    district_name = current_user.district.name_en if current_user.district else None
    taluk_name = current_user.taluk.name_en if current_user.taluk else None

    return UserOut(
        id=current_user.id,
        full_name=current_user.full_name,
        mobile_number=current_user.mobile_number,
        email=current_user.email,
        preferred_language=current_user.preferred_language,
        district_id=current_user.district_id,
        taluk_id=current_user.taluk_id,
        district_name=district_name,
        taluk_name=taluk_name
    )

@router.put("/profile", response_model=UserOut)
def update_profile(
    full_name: str,
    preferred_language: str,
    district_id: int = None,
    taluk_id: int = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user.full_name = full_name
    current_user.preferred_language = preferred_language
    if district_id:
        current_user.district_id = district_id
    if taluk_id:
        current_user.taluk_id = taluk_id
    db.commit()
    db.refresh(current_user)

    district_name = current_user.district.name_en if current_user.district else None
    taluk_name = current_user.taluk.name_en if current_user.taluk else None

    return UserOut(
        id=current_user.id,
        full_name=current_user.full_name,
        mobile_number=current_user.mobile_number,
        email=current_user.email,
        preferred_language=current_user.preferred_language,
        district_id=current_user.district_id,
        taluk_id=current_user.taluk_id,
        district_name=district_name,
        taluk_name=taluk_name
    )
