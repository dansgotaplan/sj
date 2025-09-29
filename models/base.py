from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer
from config.database import getdb

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True

    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    @classmethod
    def getall(cls, skip: int = 0, limit: int = 100):
        with getdb() as session:
            results = session.query(cls).offset(skip).limit(limit).all()
            return [obj.to_dict() for obj in results]
    
    @classmethod
    def getbycode(cls, code: int):
        with getdb() as session:
            return session.query(cls).filter(cls.code == code).first()

    @classmethod
    def create(cls, **kwargs):
        with getdb() as session:
            obj = cls(**kwargs)
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj

    def update(self, **kwargs):
        with getdb() as session:
            obj = session.merge(self)
            for key, value in kwargs.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            session.commit()
            session.refresh(obj)
            return obj
    
    def delete(self):
        with getdb() as session:
            obj = session.merge(self)
            session.delete(obj)
            session.commit()
            return True
        
    def getcode(self):
        return str(self.code)