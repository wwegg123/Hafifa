from fastapi import APIRouter

router = APIRouter(tags=["alerts"])

@router.get("/alerts")
async def get_alerts(date: str | None = None, city: str | None = None):
    return 