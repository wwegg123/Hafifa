from fastapi import APIRouter, Depends
from database.connection import get_db
from sqlalchemy.orm import Session
from models.alerts import Alerts_Response
import services.alerts as alert_services


router = APIRouter(tags=["alerts"])

@router.get("/alerts")
async def get_alerts(date: str | None = None, city: str | None = None, db:Session = Depends(get_db)) -> list[Alerts_Response]:
    return alert_services.get_alerts(date, city, db)