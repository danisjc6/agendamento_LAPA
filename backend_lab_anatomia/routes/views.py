from fastapi import APIRouter, Query, HTTPException
from typing import List
from datetime import date

from models.views import (
    listar_agendamentos_detalhados,
    listar_agendamentos_ativos,
    listar_salas_livres,
    listar_ocupacao_salas_por_data,
    listar_salas_mais_utilizadas
)

from schemas import (
    AgendamentoDetalhado,
    OcupacaoSala,
    ModeloMaisUtilizado,
    SalaMaisUtilizada
)

router = APIRouter(prefix="/views", tags=["Views"])


# =========================
# AGENDAMENTOS
# =========================

@router.get("/agendamentos", response_model=List[AgendamentoDetalhado])
def get_agendamentos():
    return listar_agendamentos_detalhados()


@router.get("/agendamentos/ativos", response_model=List[AgendamentoDetalhado])
def get_agendamentos_ativos(data: date = Query(...)):
    return listar_agendamentos_ativos(data)


# =========================
# OCUPAÇÃO SALAS
# =========================


@router.get("/salas-livres")
def get_salas_livres():
    return listar_salas_livres()


@router.get("/ocupacao-salas/por-data", response_model=List[OcupacaoSala])
def get_ocupacao_salas_por_data(data: date = Query(...)):
    return listar_ocupacao_salas_por_data(data)


# =========================
# ESTATÍSTICAS
# =========================


@router.get("/salas-mais-utilizadas", response_model=List[SalaMaisUtilizada])
def get_salas_mais_utilizadas():
    return listar_salas_mais_utilizadas()
