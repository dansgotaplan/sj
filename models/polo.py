from sqlalchemy import Column, String, Text, Date, DECIMAL, Boolean, CheckConstraint, Integer
from sqlalchemy.orm import relationship
from .base import BaseModel

class Polo(BaseModel):
    __tablename__ = 'polo'

    code = Column(Integer, primary_key=True, autoincrement=True)
    handle = Column(String(255), unique=True, nullable=False)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=False)
    inicio = Column(Date, nullable=False)
    fim = Column(Date, nullable=False)
    endereco = Column(String(500), nullable=False)
    latitude = Column(DECIMAL(8, 5), nullable=False)
    longitude = Column(DECIMAL(8, 5), nullable=False)
    ismultilocal = Column(Boolean, nullable=False, default=False)
    urlimagem = Column(String(255), nullable=False)

    exibicoes = relationship('Exibicao', back_populates='polo')

    __table_args__ = (
        CheckConstraint('(ismultilocal = 0 AND endereco IS NOT NULL AND latitude IS NOT NULL AND longitude IS NOT NULL) OR (ismultilocal = 1 AND endereco IS NULL AND latitude IS NULL AND longitude IS NULL)', name = 'check_multilocal'),
    )