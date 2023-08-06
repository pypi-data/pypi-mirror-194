from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from neer.base import PrimaryBase

class InpTimeseriesBackTesting(PrimaryBase):
    __tablename__ = 'inp_timeseries_back_testing'
    __table_args__ = {'schema': 'timeseries'}
    
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    project_id = Column(INTEGER, nullable=False, autoincrement=False)
    name = Column(TEXT, nullable=False, autoincrement=False)
    description = Column(TEXT, autoincrement=False)
    file = Column(TEXT, autoincrement=False)
    created_at = Column(TIMESTAMP, nullable=False, autoincrement=False)
    updated_at = Column(TIMESTAMP, autoincrement=False)
