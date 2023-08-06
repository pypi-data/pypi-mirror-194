from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME, JSON
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from neer.base import PrimaryBase

class Forecasts(PrimaryBase):
    __tablename__ = 'forecasts'
    __table_args__ = {'schema': 'timeseries'}
    
    type = Column(TEXT, primary_key=True, autoincrement=False)
    latitude = Column(NUMERIC, primary_key=True, autoincrement=False)
    longitude = Column(NUMERIC, primary_key=True, autoincrement=False)
    site_id = Column(UUID, autoincrement=False)
    timezone = Column(TEXT, autoincrement=False)
    timezone_offset = Column(INTEGER, autoincrement=False)
    sunrise = Column(TIMESTAMP, autoincrement=False)
    sunset = Column(TIMESTAMP, autoincrement=False)
    moonrise = Column(TIMESTAMP, autoincrement=False)
    moonset = Column(TIMESTAMP, autoincrement=False)
    moon_phase = Column(NUMERIC, autoincrement=False)
    temperature = Column(NUMERIC, autoincrement=False)
    temperature_morning = Column(NUMERIC, autoincrement=False)
    temperature_day = Column(NUMERIC, autoincrement=False)
    temperature_evening = Column(NUMERIC, autoincrement=False)
    temperature_night = Column(NUMERIC, autoincrement=False)
    temperature_min = Column(NUMERIC, autoincrement=False)
    temperature_max = Column(NUMERIC, autoincrement=False)
    feels_like = Column(NUMERIC, autoincrement=False)
    feels_like_morning = Column(NUMERIC, autoincrement=False)
    feels_like_day = Column(NUMERIC, autoincrement=False)
    feels_like_evening = Column(NUMERIC, autoincrement=False)
    feels_like_night = Column(NUMERIC, autoincrement=False)
    pressure = Column(NUMERIC, autoincrement=False)
    humidity = Column(NUMERIC, autoincrement=False)
    dew_point = Column(NUMERIC, autoincrement=False)
    uv_index = Column(NUMERIC, autoincrement=False)
    clouds = Column(NUMERIC, autoincrement=False)
    visibility = Column(NUMERIC, autoincrement=False)
    wind_speed = Column(NUMERIC, autoincrement=False)
    wind_direction = Column(NUMERIC, autoincrement=False)
    wind_gust = Column(NUMERIC, autoincrement=False)
    probability_of_precipitation = Column(NUMERIC, autoincrement=False)
    precipitation = Column(NUMERIC, autoincrement=False)
    rain = Column(NUMERIC, autoincrement=False)
    snow = Column(NUMERIC, autoincrement=False)
    weather = Column(JSON, autoincrement=False)
    forecasted_at = Column(TIMESTAMP, primary_key=True, autoincrement=False)
    created_at = Column(TIMESTAMP, primary_key=True, autoincrement=False)
