from models.air_quality import Air_Quality
from calculate_aqi import calculate_aqi
from sqlalchemy import select
import codecs
import csv

def upload_air_quality_service(file, db):
    csvReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
    rows = []
    for row in csvReader:
        # stmt = select(air_quality).where(
        #   and_(air_quality.columns.date == row[date], air_quality.columns.city == row[city])
        
        # exists = db.execute(stmt).fetchall()

        # if exists:
        #     continue

        aqi_result, aqi_level_result = calculate_aqi(row["PM2.5"], row["NO2"], row["CO2"])

        record = Air_Quality(
            date= row["date"],
            city_name= row["city"],
            pm2_5= row["PM2.5"],
            no2= row["NO2"],
            co2= row["CO2"],
            aqi= aqi_result,
            aqi_level = aqi_level_result
        )
        rows.append(record)
    
    db.add_all(rows)
    db.commit()
    file.file.close()
    return {"message": f"Uploaded {len(rows)}"}


def get_air_quality(start_date, end_date, city, db):
    query = select(Air_Quality)

    query = query.where(Air_Quality.date >= start_date) if start_date else query

    query = query.where(Air_Quality.date <= end_date) if end_date else query

    query = query.where(Air_Quality.city == city) if city else query

    return db.execute(query).fetch_all()

def get_best(db):
    query = select(Air_Quality).order_by(Air_Quality.aqi.asc()).limit(3)
    return db.execute(query).fetch_all() 

def get_city_history(city , db):
    query = select(Air_Quality).where(Air_Quality.city == city)
    return db.execute(query).fetch_all() 

def get_city_avg(city, db):
    query = select(Air_Quality.city_name, db.func.avg(Air_Quality.aqi)).where(Air_Quality.city == city)
    return db.execute(query).fetch_all() 