from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import BaseModel

class Tag(BaseModel):
    __tablename__ = 'tag'
    
    code = Column(Integer, primary_key=True, autoincrement=True)
    handle = Column(String(255), unique=True, nullable=False)
    nome = Column(String(255), nullable=False)
    
    # Relações
    locais = relationship('Locais', secondary='locaistags', back_populates='tags')
    atracoes = relationship('Atracao', secondary='atracaotags', back_populates='tags')