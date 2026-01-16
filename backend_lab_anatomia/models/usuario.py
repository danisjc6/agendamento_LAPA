from sqlalchemy import Column, Integer, String
from models.base import Base

class Usuario(Base):
    __tablename__ = "Usuario"

    matricula = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100))
    telefone = Column(String(20))
    curso = Column(String(50))


