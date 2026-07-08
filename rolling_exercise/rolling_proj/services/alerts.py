from models.alerts import Alerts
from sqlalchemy import select

def get_alerts(date, city, db):
    query = select(Alerts)

    query = query.where(Alerts.date == date) if date else query

    query = query.where(Alerts.city == city) if city else query

    results = db.execute(query).fetchall()
    return [row[0] for row in results]
