from sqlalchemy import Column, Integer, String, Text
from app.database.session import Base

class Pattam(Base):
    __tablename__ = "pattams"

    id = Column(Integer, primary_key=True, index=True)
    name_en = Column(String(100), unique=True, index=True, nullable=False)
    name_ta = Column(String(100), nullable=False)
    months_en = Column(String(100), nullable=False)  # e.g., "June - July / Aadi"
    months_ta = Column(String(100), nullable=False)  # e.g., "ஜூன் - ஜூலை / ஆடி"
    description_en = Column(Text, nullable=False)
    description_ta = Column(Text, nullable=False)
    recommended_crops_en = Column(Text, nullable=False)
    recommended_crops_ta = Column(Text, nullable=False)
