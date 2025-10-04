from sqlalchemy import Column, Integer, String, Text, Boolean, CheckConstraint
from .base import BaseModel

class Pessoa(BaseModel):
    __tablename__ = 'pessoa'
    
    code = Column(Integer, primary_key=True, autoincrement=True)
    handle = Column(String(255), unique=True, nullable=False)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=False)
    obras = Column(String(500), nullable=False)
    nascido = Column(Integer, nullable=False)
    morte = Column(Integer)
    ishomenageado = Column(Boolean, nullable=False, default=False)
    anohomenagem = Column(Integer)
    urlimagem = Column(String(1000), nullable=False)
    
    __table_args__ = (
        CheckConstraint('morte > nascido', name='chk_data'),
    )