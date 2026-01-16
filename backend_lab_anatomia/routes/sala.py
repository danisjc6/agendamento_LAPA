from datetime import date, datetime, time, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
from models.agendamento import Agendamento
from models.reserva import Reserva
from schemas import HorarioDisponibilidade

router = APIRouter(
    prefix="/salas",
    tags=["Salas"]
)


def gerar_blocos():
    inicio = time(8, 0)
    fim = time(18, 0)

    blocos = []
    atual = datetime.combine(date.today(), inicio)

    while atual.time() < fim:
        proximo = atual + timedelta(hours=1)
        blocos.append((atual.time(), proximo.time()))
        atual = proximo

    return blocos


@router.get(
    "/{id_sala}/disponibilidade",
    response_model=list[HorarioDisponibilidade]
)
def verificar_disponibilidade(
    id_sala: int,
    data: date = Query(...),   # 👈 ISSO É ESSENCIAL
    db: Session = Depends(get_db)
):
    blocos = gerar_blocos()

    reservas = (
        db.query(Reserva)
        .join(Agendamento)
        .filter(
            Reserva.id_sala == id_sala,
            Agendamento.data == data,
            Agendamento.status == "ativo"
        )
        .all()
    )

    ocupados = set()
    for r in reservas:
        ag = r.agendamento
        atual = ag.hora_inicio
        while atual < ag.hora_fim:
            ocupados.add(atual)
            atual = (datetime.combine(date.today(), atual) + timedelta(hours=1)).time()

    disponiveis = []
    for inicio, fim in blocos:
        if inicio not in ocupados:
            disponiveis.append(
                HorarioDisponibilidade(
                    data=data,
                    hora_inicio=inicio,
                    hora_fim=fim
                )
            )

    return disponiveis
