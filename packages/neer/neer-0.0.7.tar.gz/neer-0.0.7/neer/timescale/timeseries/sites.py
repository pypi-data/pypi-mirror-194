from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME, JSON
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from neer.base import PrimaryBase

class Sites(PrimaryBase):
    __tablename__ = 'sites'
    __table_args__ = {'schema': 'timeseries'}
    
    id = Column(UUID, primary_key=True, autoincrement=False)
    name = Column(TEXT, autoincrement=False)
    description = Column(TEXT, autoincrement=False)
    facility_id = Column(TEXT, autoincrement=False)
    created_at = Column(TIMESTAMP, nullable=False, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
    meta = Column('metadata', JSON, autoincrement=False)
    tags = Column(JSON, autoincrement=False)
    team_id = Column(INTEGER, nullable=False, autoincrement=False)
    latitude = Column(NUMERIC, autoincrement=False)
    longitude = Column(NUMERIC, autoincrement=False)
