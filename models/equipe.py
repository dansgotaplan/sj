from sqlalchemy import Column, Integer, String
from .base import BaseModel

class Equipe(BaseModel):
    __tablename__ = 'equipe'
    
    code = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    turma = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    ano = Column(String(50), nullable=False)
    urlimagem = Column(String(255))