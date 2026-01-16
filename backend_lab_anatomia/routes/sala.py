from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, time

from database import get_db
from models import Sala, Reserva, Agendamento
from schemas.sala import SalaResponse
from schemas.agendamento import HorarioDisponibilidade

router = APIRouter(prefix="/salas", tags=["Salas"])


@router.post(
    "/disponiveis",
    response_model=list[SalaResponse]
)
def listar_salas_disponiveis(
    dados: HorarioDisponibilidade,
    db: Session = Depends(get_db)
):
    subquery = (
        db.query(Reserva.id_sala)
        .join(Agendamento, Agendamento.id == Reserva.id_agendamento)
        .filter(
            Agendamento.data == dados.data,
            dados.hora_inicio < Agendamento.hora_fim,
            dados.hora_fim > Agendamento.hora_inicio
        )
        .subquery()
    )

    salas = (
        db.query(Sala)
        .filter(Sala.id_sala.notin_(subquery))
        .all()
    )

    return salas
