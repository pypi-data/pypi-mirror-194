from sqlalchemy import Column, Sequence
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID, TIMESTAMP, TIME, JSONB, ENUM
from sqlalchemy.types import VARCHAR, BIGINT, DATE, INTEGER, NUMERIC, BOOLEAN, TEXT
from neer.base import PrimaryBase

class Features(PrimaryBase):
    __tablename__ = 'features'
    __table_args__ = {'schema': 'cswr'}
    
    id = Column(UUID, primary_key=True, autoincrement=False)
    fid = Column(INTEGER, nullable=False, autoincrement=False)
    service = Column(TEXT, nullable=False, autoincrement=False)
    layer = Column(TEXT, nullable=False, autoincrement=False)
    geometry = Column(TEXT, autoincrement=False)
    properties = Column(JSONB, autoincrement=False)
    created_at = Column(TIMESTAMP, nullable=False, autoincrement=False)
    category = Column(ENUM, autoincrement=False)
