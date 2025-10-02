from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import joinedload
from config.database import getdb

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    @classmethod
    def getall_dict(cls, skip: int = 0, limit: int = 100):
        with getdb() as session:
            results = session.query(cls).offset(skip).limit(limit).all()
            return [obj.to_dict() for obj in results]

    @classmethod
    def getall_with_rel(cls, skip: int = 0, limit: int = 100):
        with getdb() as session:
            query = session.query(cls).offset(skip).limit(limit)
            # Carregamento de relacionamento específico
            if cls.__name__ == "Exibicao":
                query = query.options(joinedload(cls.polo))
            results = query.all()
            final = []
            for obj in results:
                if hasattr(obj, 'to_dict_with_rel'):
                    final.append(obj.to_dict_with_rel())
                else:
                    d = obj.to_dict()
                    if cls.__name__ == "Exibicao":
                        d['polo'] = obj.polo.to_dict() if obj.polo else None
                    final.append(d)
            return final

    @classmethod
    def create(cls, **kwargs):
        with getdb() as session:
            obj = cls(**kwargs)
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj
