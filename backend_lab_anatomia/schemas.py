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



class SalaBase(BaseModel):
    nome_sala: str
    tipo: Optional[str] = None
    capacidade: Optional[int] = None

class SalaResponse(SalaBase):
    id_sala: int


class SalaCreate(SalaBase):
    pass



class AgendamentoBase(BaseModel):
    matricula: int
    id_sala: int
    data: date
    hora_inicio: time
    hora_fim: time
    finalidade: Optional[str] = None
    status: Optional[str] = "ativo"


class AgendamentoCreate(AgendamentoBase):
    matricula: int
    id_sala: int
    data: date
    hora_inicio: time
    hora_fim: time
    finalidade: str
    status: str = "ativo"


class AgendamentoResponse(AgendamentoBase):
    id_agendamento: int


class HorarioDisponibilidade(BaseModel):
    data: date
    hora_inicio: time
    hora_fim: time


class ReservaDetalhada(BaseModel):
    id_agendamento: int
    usuario_nome: str
    email: str
    nome_sala: str
    tipo: str
    capacidade: int
    data: date
    hora_inicio: time
    hora_fim: time
    finalidade: str
    status: str
    

class CancelamentoRequest(BaseModel):
    motivo: str | None = None


class ReservaCreate(BaseModel):
    id_agendamento: int
    id_sala: int


# Views

# =========================
# AGENDAMENTOS
# =========================

class AgendamentoDetalhado(BaseModel):
    id_agendamento: int
    usuario_nome: str
    email: str
    nome_sala: str
    tipo: str
    capacidade: int
    data: date
    hora_inicio: time
    hora_fim: time
    finalidade: str
    status: str
    

# =========================
# OCUPAÇÃO SALAS
# =========================

class OcupacaoSala(BaseModel):
    sala: str
    data_agendamento: date
    total_agendamentos: int


# =========================
# ESTATÍSTICAS
# =========================



class SalaMaisUtilizada(BaseModel):
    nome_sala: str
    total_reservas: int
