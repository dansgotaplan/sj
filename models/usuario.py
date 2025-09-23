from sqlalchemy import Column, Integer, String, Boolean
from .base import BaseModel

class Usuario(BaseModel):
    __tablename__ = 'usuario'
    
    code = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    isadmin = Column(Boolean, nullable=False, default=False)
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False