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


class SalaCreate(SalaBase):
    pass


class SalaResponse(SalaBase):
    id_sala: int

    class Config:
        orm_mode = True



class AgendamentoBase(BaseModel):
    matricula: int
    id_sala: int
    data: date
    hora_inicio: time
    hora_fim: time
    finalidade: Optional[str] = None
    status: Optional[str] = "ativo"


class AgendamentoCreate(AgendamentoBase):
    pass


class AgendamentoResponse(AgendamentoBase):
    id: int

    class Config:
        orm_mode = True


