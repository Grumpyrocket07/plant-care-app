from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from database import engine, Base
from routes.auth import router as auth_router
from routes.farms import router as farms_router
from routes.disease import router as disease_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Plant Care App API",
    description="API for plant disease detection and farm management",
    version="1.0.0"
)

# Security scheme for Swagger UI
security = HTTPBearer()

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(farms_router)
app.include_router(disease_router)

@app.get("/")
def root():
    return {"message": "Plant Care App API is running with Disease Detection! 🌱"}