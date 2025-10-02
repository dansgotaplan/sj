from sqlalchemy import Column, Integer, ForeignKey
from .base import BaseModel

class LocaisTags(BaseModel):
    __tablename__ = 'locaistags'
    
    fklocal = Column(Integer, ForeignKey('locais.code'), primary_key=True)
    fktag = Column(Integer, ForeignKey('tag.code'), primary_key=True)
