from datetime import datetime
from models.air_quality import Air_Quality
from models.alerts import Alerts
from services.calculate_aqi import calculate_aqi
from sqlalchemy import select
import codecs
import csv

def check_if_record_exists(row, db):
    query = select(Air_Quality)
    query = query.where(Air_Quality.date == row["date"])
    query = query.where(Air_Quality.city == row["city"])
    results = db.execute(query).fetchall()
    return len(results) > 0

def validate_data(row, db):
    if(check_if_record_exists(row,db)):
        print(f"{datetime.now()} Duplicate row: {row}\nData for city at that date has already been inserted")
        return False
    elif(not row["PM2.5"].isnumeric() or not row["NO2"].isnumeric() or not row["CO2"].isnumeric()):
        print(f"{datetime.now()}invalid row: {row}\nCheck for missing/corrupt values")
        return False
    return True

def convert_row_to_air_quality(row, aqi_result, aqi_level_result):
    return Air_Quality(
        date= row["date"],
        city_name= row["city"],
        pm2_5= row["PM2.5"],
        no2= row["NO2"],
        co2= row["CO2"],
        aqi= aqi_result,
        aqi_level = aqi_level_result
    )

def upload_air_quality_service(file, db):
    csvReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
    aqi_rows = []
    alert_rows = []
    for row in csvReader:
        if(not validate_data(row, db)):
            continue
            
        aqi_result, aqi_level_result = calculate_aqi(int(row["PM2.5"]), int(row["NO2"]), int(row["CO2"]))
        record = convert_row_to_air_quality(row, aqi_result, aqi_level_result)
        
        aqi_rows.append(record)
        if aqi_result > 300 :
            alert_rows.append(Alerts(date= row["date"], city_name= row["city"], aqi= aqi_result))
    
    db.add_all(aqi_rows)
    db.add_all(alert_rows)
    db.commit()
    file.file.close()
    return {"message": f"Uploaded {len(aqi_rows)} to air_quality | Uploaded ({len(alert_rows)}) to alerts"}


def get_air_quality(start_date, end_date, city, db):
    query = select(Air_Quality)

    query = query.where(Air_Quality.date >= start_date) if start_date else query

    query = query.where(Air_Quality.date <= end_date) if end_date else query

    query = query.where(Air_Quality.city == city) if city else query
    results = db.execute(query).fetchall()
    return [row[0] for row in results]

def get_best(db):
    query = select(Air_Quality).order_by(Air_Quality.aqi.asc()).limit(3)
    results = db.execute(query).fetchall()
    return [row[0] for row in results]

def get_city_history(city , db):
    query = select(Air_Quality).where(Air_Quality.city == city)
    results = db.execute(query).fetchall()
    return [row[0] for row in results] 

def get_city_avg(city, db):
    query = select(Air_Quality.city_name, db.func.avg(Air_Quality.aqi)).where(Air_Quality.city == city)
    results = db.execute(query).fetchall()
    return [row[0] for row in results]