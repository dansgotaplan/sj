from sqlalchemy import Column, String, Text, Time, DECIMAL, CheckConstraint, Integer
from sqlalchemy.orm import relationship, joinedload
from .base import BaseModel
from config.database import getdb

class Locais(BaseModel):
    __tablename__ = 'locais'

    code = Column(Integer, primary_key=True, autoincrement=True)
    handle = Column(String(255), unique=True, nullable=False)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=False)
    dias = Column(String(255))
    inicio = Column(Time, nullable=False)
    fim = Column(Time, nullable=False)
    endereco = Column(String(500), nullable=False)
    latitude = Column(DECIMAL(8, 5), nullable=False)
    longitude = Column(DECIMAL(8, 5), nullable=False)
    urlimage = Column(String(1000), nullable=False)
    urlicone = Column(String(1000), nullable=False)

    tags = relationship('Tag', secondary='locaistags', back_populates='locais')

    __table_args__ = (
        CheckConstraint('fim > inicio', name='checkdata'),
    )

    @classmethod
    def getall_with_rel(cls):
        with getdb() as session:
            locais = session.query(cls).options(joinedload(cls.tags)).all()
            for local in locais:
                # garante que as tags estão carregadas
                local.tags
            # transforma para exibição e POST
            result = []
            for local in locais:
                result.append({
                    "code": local.code,
                    "handle": local.handle,
                    "nome": local.nome,
                    "descricao": local.descricao,
                    "dias": local.dias,
                    "inicio": str(local.inicio),
                    "fim": str(local.fim),
                    "endereco": local.endereco,
                    "latitude": float(local.latitude),
                    "longitude": float(local.longitude),
                    "urlimage": local.urlimage,
                    "urlicone": local.urlicone,
                    # códigos para JS/POST
                    "tags": [t.code for t in local.tags],
                    # nomes para exibição
                    "tags_names": [t.nome for t in local.tags]
                })
            return result
