from sqlalchemy import Column, String, Text, Date, Time, DECIMAL, Integer
from .base import BaseModel

class Evento(BaseModel):
    __tablename__ = 'evento'

    code = Column(Integer, primary_key=True, autoincrement=True)
    handle = Column(String(255), unique=True, nullable=False)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=False)
    inicio = Column(Date, nullable=False)
    fim = Column(Date)
    horario = Column(Time, nullable=False)
    endereco = Column(String(500), nullable=False)
    latitude = Column(DECIMAL(8, 5), nullable=False)
    longitude = Column(DECIMAL(8, 5), nullable=False)
    urlimagem = Column(String(1000), nullable=False)