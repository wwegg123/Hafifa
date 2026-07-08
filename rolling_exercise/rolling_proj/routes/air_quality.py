from fastapi import APIRouter, UploadFile, File

router = APIRouter(tags=["air-quality"])

@router.post("/")
async def upload_air_quality(file: UploadFile = File(...)):
    return

@router.get("/")
async def get_air_quality(start_date: str | None = None, end_date: str | None = None, city: str | None = None):
    return 

@router.get("/best")
async def get_best():
    return 

@router.get("/{city}/history")
async def get_city_history():
    return 

@router.get("/{city}/avg")
async def get_city_avg():
    return 