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
        from_attributes = True



class SalaBase(BaseModel):
    nome_sala: str
    tipo: Optional[str] = None
    capacidade: Optional[int] = None

class SalaResponse(SalaBase):
    id_sala: int

    class Config:
        from_attributes = True

class SalaCreate(SalaBase):
    pass



class AgendamentoBase(BaseModel):
    matricula: int
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
        from_attributes = True



class HorarioDisponibilidade(BaseModel):
    data: date
    hora_inicio: time
    hora_fim: time



class ReservaDetalhada(BaseModel):
    id_agendamento: int
    data: date
    hora_inicio: time
    hora_fim: time
    finalidade: str
    status: str

    nome_sala: str

    matricula: int
    nome_usuario: str

    class Config:
        from_attributes = True



class CancelamentoRequest(BaseModel):
    motivo: str | None = None



class ReservaCreate(BaseModel):
    id_agendamento: int
    id_sala: int
