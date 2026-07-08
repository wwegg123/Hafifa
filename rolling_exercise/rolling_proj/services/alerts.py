from models.alerts import Alerts
from calculate_aqi import calculate_aqi
from sqlalchemy import select, func
import codecs
import csv

def get_alerts(date, city, db):
    query = select(Alerts)

    query = query.where(Alerts.date == date) if date else query

    query = query.where(Alerts.city == city) if city else query

    return db.execute(query).fetch_all()
