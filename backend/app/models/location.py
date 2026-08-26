from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base

class District(Base):
    __tablename__ = "districts"

    id = Column(Integer, primary_key=True, index=True)
    name_en = Column(String(100), unique=True, index=True, nullable=False)
    name_ta = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    taluks = relationship("Taluk", back_populates="district", cascade="all, delete-orphan")
    users = relationship("User", back_populates="district")
    predictions = relationship("Prediction", back_populates="district")

class Taluk(Base):
    __tablename__ = "taluks"

    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=False, index=True)
    name_en = Column(String(100), nullable=False)
    name_ta = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    district = relationship("District", back_populates="taluks")
    users = relationship("User", back_populates="taluk")
    predictions = relationship("Prediction", back_populates="taluk")
