from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME, JSON
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from neer.base import PrimaryBase

class HistoricalWeather(PrimaryBase):
    __tablename__ = 'historical_weather'
    __table_args__ = {'schema': 'timeseries'}
    
    site_id = Column(TEXT, autoincrement=False)
    latitude = Column(NUMERIC, nullable=False, autoincrement=False)
    longitude = Column(NUMERIC, nullable=False, autoincrement=False)
    timezone = Column(TEXT, autoincrement=False)
    timezone_offset = Column(INTEGER, autoincrement=False)
    feels_like = Column(NUMERIC, autoincrement=False)
    pressure = Column(NUMERIC, autoincrement=False)
    humidity = Column(NUMERIC, autoincrement=False)
    wind_speed = Column(NUMERIC, autoincrement=False)
    wind_direction = Column(NUMERIC, autoincrement=False)
    rain = Column(NUMERIC, autoincrement=False)
    snow = Column(NUMERIC, autoincrement=False)
    weather = Column(JSON, autoincrement=False)
    read_at = Column(TIMESTAMP, nullable=False, autoincrement=False)
    created_at = Column(TIMESTAMP, nullable=False, autoincrement=False)
    temperature = Column(NUMERIC, autoincrement=False)
    id = Column(INTEGER, primary_key=True, autoincrement=True)
