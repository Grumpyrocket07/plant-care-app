from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    name = Column(String)
    language = Column(String, default="en")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    farms = relationship("Farm", back_populates="owner")

class Farm(Base):
    __tablename__ = "farms"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    crop_type = Column(String)
    area = Column(Float)
    planting_date = Column(Date)
    location = Column(String, nullable=True)
    
    owner = relationship("User", back_populates="farms")
    disease_detections = relationship("DiseaseDetection", back_populates="farm")
    fertilizer_logs = relationship("FertilizerLog", back_populates="farm")
    soil_tests = relationship("SoilTest", back_populates="farm")

class DiseaseDetection(Base):
    __tablename__ = "disease_detections"
    
    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"))
    disease_name = Column(String)
    confidence = Column(Float)
    treatment = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    farm = relationship("Farm", back_populates="disease_detections")

class FertilizerLog(Base):
    __tablename__ = "fertilizer_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"))
    date = Column(Date)
    npk_ratio = Column(String)
    quantity_kg = Column(Float)
    notes = Column(String, nullable=True)
    
    farm = relationship("Farm", back_populates="fertilizer_logs")

class SoilTest(Base):
    __tablename__ = "soil_tests"
    
    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"))
    ph = Column(Float)
    nitrogen = Column(Float)
    phosphorus = Column(Float)
    potassium = Column(Float)
    date = Column(Date)
    
    farm = relationship("Farm", back_populates="soil_tests")