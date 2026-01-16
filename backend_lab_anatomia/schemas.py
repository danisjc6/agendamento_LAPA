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
    nome: str
    capacidade: Optional[int] = None
    descricao: Optional[str] = None

class SalaCreate(SalaBase):
    pass

class SalaResponse(SalaBase):
    id_sala: int

    class Config:
        orm_mode = True



class AgendamentoBase(BaseModel):
    data: date
    hora_inicio: time
    hora_fim: time

class AgendamentoCreate(AgendamentoBase):
    matricula_usuario: int
    id_sala: int

class AgendamentoResponse(AgendamentoBase):
    id_agendamento: int
    matricula_usuario: int
    id_sala: int

    class Config:
        orm_mode = True

