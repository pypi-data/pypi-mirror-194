from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME, JSON
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from neer.base import PrimaryBase

class SiteSensors(PrimaryBase):
    __tablename__ = 'site_sensors'
    __table_args__ = {'schema': 'timeseries'}
    
    id = Column(UUID, primary_key=True, autoincrement=False)
    site_id = Column(UUID, nullable=False, autoincrement=False)
    name = Column(TEXT, autoincrement=False)
    description = Column(TEXT, autoincrement=False)
    connection = Column(TEXT, autoincrement=False)
    type = Column(TEXT, nullable=False, autoincrement=False)
    style = Column(TEXT, autoincrement=False)
    system = Column(TEXT, autoincrement=False)
    label = Column(TEXT, autoincrement=False)
    units = Column(TEXT, autoincrement=False)
    installed_at = Column(TIMESTAMP, autoincrement=False)
    repaired_at = Column(TIMESTAMP, autoincrement=False)
    removed_at = Column(TIMESTAMP, autoincrement=False)
    created_at = Column(TIMESTAMP, nullable=False, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
    meta = Column('metadata', JSON, autoincrement=False)
    tags = Column(JSON, autoincrement=False)
    virtual = Column(BOOLEAN, nullable=False, autoincrement=False)
    latitude = Column(NUMERIC, autoincrement=False)
    longitude = Column(NUMERIC, autoincrement=False)
