from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from models.air_quality import Air_Quality_Response
import services.air_quality as aq_services
from database.connection import get_db

router = APIRouter(tags=["air-quality"])

@router.post("/")
async def upload_air_quality(file: UploadFile = File(...), db:Session = Depends(get_db)):
    return aq_services.upload_air_quality_service(file, db)

@router.get("/")
async def get_air_quality(start_date: str | None = None, end_date: str | None = None, 
                          city: str | None = None, db:Session = Depends(get_db)) -> list[Air_Quality_Response]:
    return aq_services.get_air_quality(start_date, end_date, city, db)

@router.get("/best")
async def get_best(db:Session = Depends(get_db)) -> list[Air_Quality_Response]:
    return aq_services.get_best(db)

@router.get("/{city}/history")
async def get_city_history(db:Session = Depends(get_db)) -> list[Air_Quality_Response]:
    return aq_services.get_city_history(db)

@router.get("/{city}/avg")
async def get_city_avg(db:Session = Depends(get_db)) -> list[Air_Quality_Response]:
    return aq_services.get_city_avg(db)