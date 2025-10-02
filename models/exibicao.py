from sqlalchemy import Column, String, Integer, ForeignKey, Date, Time, DECIMAL
from sqlalchemy.orm import relationship
from .base import BaseModel

class Exibicao(BaseModel):
    __tablename__ = 'exibicao'

    code = Column(Integer, primary_key=True, autoincrement=True)
    ordem = Column(Integer)
    fk = Column(Integer, ForeignKey('polo.code'), nullable=False)
    dia = Column(Date, nullable=False)
    horario = Column(Time, nullable=False)
    endereco = Column(String(500), nullable=False)
    latitude = Column(DECIMAL(8, 5), nullable=False)
    longitude = Column(DECIMAL(8,5), nullable= False)

    polo = relationship('Polo', back_populates='exibicoes')
    atracoes = relationship('Atracao', secondary='atracaoexibicao', back_populates='exibicoes')
