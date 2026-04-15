from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    language: Optional[str] = "en"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    language: str
    
    class Config:
        from_attributes = True

# Farm Schemas
class FarmCreate(BaseModel):
    name: str
    crop_type: str
    area: float
    planting_date: date
    location: Optional[str] = None

class FarmResponse(BaseModel):
    id: int
    name: str
    crop_type: str
    area: float
    planting_date: date
    location: Optional[str]
    
    class Config:
        from_attributes = True

# Disease Detection Schemas
class DiseaseDetectionResponse(BaseModel):
    id: int
    disease_name: str
    confidence: float
    treatment: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

# Fertilizer Log Schemas
class FertilizerLogCreate(BaseModel):
    farm_id: int
    date: date
    npk_ratio: str
    quantity_kg: float
    notes: Optional[str] = None

class FertilizerLogResponse(BaseModel):
    id: int
    date: date
    npk_ratio: str
    quantity_kg: float
    notes: Optional[str]
    
    class Config:
        from_attributes = True

# Soil Test Schemas
class SoilTestCreate(BaseModel):
    farm_id: int
    ph: float
    nitrogen: float
    phosphorus: float
    potassium: float
    date: date

class SoilTestResponse(BaseModel):
    id: int
    ph: float
    nitrogen: float
    phosphorus: float
    potassium: float
    date: date
    
    class Config:
        from_attributes = True

# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str