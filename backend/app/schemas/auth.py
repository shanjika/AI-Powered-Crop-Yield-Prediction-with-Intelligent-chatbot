from pydantic import BaseModel, Field
from typing import Optional

class UserSignup(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    mobile_number: str = Field(..., min_length=10, max_length=15)
    email: Optional[str] = None
    password: str = Field(..., min_length=6)
    preferred_language: str = Field("ta", pattern="^(ta|en)$")
    district_id: Optional[int] = None
    taluk_id: Optional[int] = None

class UserLogin(BaseModel):
    username: str  # Mobile number or email
    password: str

class UserOut(BaseModel):
    id: int
    full_name: str
    mobile_number: str
    email: Optional[str] = None
    preferred_language: str
    district_id: Optional[int] = None
    taluk_id: Optional[int] = None
    district_name: Optional[str] = None
    taluk_name: Optional[str] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
