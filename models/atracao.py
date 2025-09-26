from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class Atracao(BaseModel):
    __tablename__ = 'atracao'

    code = Column(Integer, primary_key=True, autoincrement=True)
    handle = Column(String(255), unique=True, nullable=False)
    ordem = Column(Integer)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=False)
    principal = Column(Boolean, nullable=False)
    urlimagem = Column(String(255), nullable=False)
    
    exibicoes = relationship('Exibicao', secondary='atracaoexibicao', back_populates='atracoes')
    tags = relationship('Tag', secondary='atracaotags', back_populates='atracoes')