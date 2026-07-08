from uuid import uuid4
from unittest.mock import patch

from datetime import date
from fastapi import status
from fastapi.testclient import TestClient
import pytest

from database.connection import get_db
from main import app
from models.air_quality import Air_Quality

# Creates a mock app
client = TestClient(app)

ID = uuid4()
DATE = date.today()
CITY_NAME = "test_city"
PM2_5 = 1
NO2 = 1
CO2 = 1
AQI = 1
AQI_LEVEL = "test_levevl"

# Makes it run before every test
@pytest.fixture(autouse=True)
def override_db_dependency():
    def fake_get_db():
        yield None

    app.dependency_overrides[get_db] = fake_get_db
    yield
    app.dependency_overrides.clear()


# Tests the "/" path
def test_get_air_quality():
    with patch(
        "services.air_quality.get_air_quality",
        return_value=[
            Air_Quality(
                id = ID,
                date = DATE,
                city_name = CITY_NAME,
                pm2_5 = PM2_5,
                no2 = NO2,
                co2 = CO2,
                aqi = AQI,
                aqi_level = AQI_LEVEL
            )
        ],
    ):
        response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1