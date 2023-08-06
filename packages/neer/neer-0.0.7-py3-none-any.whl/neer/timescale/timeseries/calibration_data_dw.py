from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from neer.base import PrimaryBase

class CalibrationDataDw(PrimaryBase):
    __tablename__ = 'calibration_data_dw'
    __table_args__ = {'schema': 'timeseries'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    calibration_type = Column(TEXT, nullable=False, autoincrement=False)
    object_name = Column(TEXT, nullable=False, autoincrement=False)
    date = Column(DATE, autoincrement=False)
    time = Column(TIME, autoincrement=False)
    value = Column(NUMERIC, nullable=False, autoincrement=False)
    created_at = Column(TIMESTAMP, nullable=False, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
