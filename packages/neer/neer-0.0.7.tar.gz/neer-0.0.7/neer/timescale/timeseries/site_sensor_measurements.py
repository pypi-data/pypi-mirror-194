from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from neer.base import PrimaryBase

class SiteSensorMeasurements(PrimaryBase):
    __tablename__ = 'site_sensor_measurements'
    __table_args__ = {'schema': 'timeseries'}
    
    sensor_id = Column(UUID, primary_key=True, autoincrement=False)
    status = Column(TEXT, nullable=False, autoincrement=False)
    message = Column(TEXT, autoincrement=False)
    value = Column(NUMERIC, autoincrement=False)
    read_at = Column(TIMESTAMP, primary_key=True, autoincrement=False)
    created_at = Column(TIMESTAMP, nullable=False, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
