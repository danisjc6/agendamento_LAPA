from pydantic import BaseModel
from typing import Optional
from datetime import date, time


class UsuarioBase(BaseModel):
    nome: str
    email: Optional[str] = None
    telefone: Optional[str] = None
    curso: Optional[str] = None


class UsuarioCreate(UsuarioBase):
    matricula: int


class UsuarioResponse(UsuarioBase):
    matricula: int

    class Config:
        orm_mode = True



class SalaBase(BaseModel):
    nome_sala: str
    tipo: Optional[str] = None
    capacidade: Optional[int] = None

class SalaResponse(SalaBase):
    id_sala: int

    class Config:
        from_attributes = True




class HorarioDisponibilidade(BaseModel):
    data: date
    hora_inicio: time
    hora_fim: time



class Sala(Base):
    __tablename__ = "Sala"

    id_sala = Column(Integer, primary_key=True, index=True)
    nome_sala = Column(String(50), unique=True, nullable=False)
    tipo = Column(String(50))
    capacidade = Column(Integer)

