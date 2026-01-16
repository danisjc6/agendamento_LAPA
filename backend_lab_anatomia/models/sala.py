from sqlalchemy import Column, Integer, String
from models.base import Base

class Sala(Base):
    __tablename__ = "Sala"

    id_sala = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome_sala = Column(String(50), unique=True, nullable=False)
    tipo = Column(String(50))
    capacidade = Column(Integer)
