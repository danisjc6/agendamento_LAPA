from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Reserva, Sala, Agendamento, Usuario
from schemas import ReservaDetalhada
from schemas import ReservaCreate


router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.get("/", response_model=list[ReservaDetalhada])
def listar_reservas(db: Session = Depends(get_db)):
    resultados = (
        db.query(
            Agendamento.id.label("id_agendamento"),
            Agendamento.data,
            Agendamento.hora_inicio,
            Agendamento.hora_fim,
            Agendamento.finalidade,
            Agendamento.status,
            Sala.nome_sala,
            Usuario.matricula,
            Usuario.nome.label("nome_usuario"),
        )
        .join(Reserva, Reserva.id_agendamento == Agendamento.id)
        .join(Sala, Sala.id_sala == Reserva.id_sala)
        .join(Usuario, Usuario.matricula == Agendamento.matricula)
        .order_by(Agendamento.data, Agendamento.hora_inicio)
        .all()
    )

    return resultados

@router.post("/")
def criar_reserva(
    reserva: ReservaCreate,
    db: Session = Depends(get_db)
):
    # 1️⃣ Buscar o agendamento
    agendamento = (
        db.query(Agendamento)
        .filter(Agendamento.id == reserva.id_agendamento)
        .first()
    )

    if not agendamento:
        raise HTTPException(404, "Agendamento não encontrado")

    if agendamento.status != "Ativo":
        raise HTTPException(400, "Não é possível reservar um agendamento cancelado")

    # 2️⃣ Verificar conflito de horário
    conflito = (
        db.query(Reserva)
        .join(Agendamento)
        .filter(
            Reserva.id_sala == reserva.id_sala,
            Agendamento.data == agendamento.data,
            Agendamento.status == "Ativo",
            agendamento.hora_inicio < Agendamento.hora_fim,
            agendamento.hora_fim > Agendamento.hora_inicio,
        )
        .first()
    )

    if conflito:
        raise HTTPException(
            status_code=409,
            detail="Sala já reservada nesse horário"
        )

    # 3️⃣ Criar reserva
    nova_reserva = Reserva(
        id_agendamento=reserva.id_agendamento,
        id_sala=reserva.id_sala
    )

    db.add(nova_reserva)
    db.commit()

    return {"message": "Reserva criada com sucesso"}



from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.reserva import Reserva
from models.agendamento import Agendamento
from schemas import ReservaCreate

router = APIRouter(
    prefix="/reservas",
    tags=["Reservas"]
)

@router.post("/")
def criar_reserva(reserva: ReservaCreate, db: Session = Depends(get_db)):

    # 🔎 Buscar agendamento
    agendamento = db.query(Agendamento).filter(
        Agendamento.id == reserva.id_agendamento
    ).first()

    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    # 🚫 Verificar conflito de horário
    conflito = (
        db.query(Reserva)
        .join(Agendamento, Reserva.id_agendamento == Agendamento.id)
        .filter(
            Reserva.id_sala == reserva.id_sala,
            Agendamento.data == agendamento.data,
            agendamento.hora_inicio < Agendamento.hora_fim,
            agendamento.hora_fim > Agendamento.hora_inicio
        )
        .first()
    )

    if conflito:
        raise HTTPException(
            status_code=409,
            detail="Sala já reservada nesse horário"
        )

    nova_reserva = Reserva(
        id_agendamento=reserva.id_agendamento,
        id_sala=reserva.id_sala
    )

    db.add(nova_reserva)
    db.commit()

    return {"mensagem": "Reserva criada com sucesso"}
