from fastapi import APIRouter
from database import get_db
from schemas import AgendamentoCreate, AgendamentoResponse

router = APIRouter(prefix="/agendamentos", tags=["Agendamentos"])

@router.post("/", response_model=AgendamentoResponse)
def criar_agendamento(ag: AgendamentoCreate):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    query = """
    INSERT INTO Agendamento
    (matricula, id_sala, data, hora_inicio, hora_fim, finalidade, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        ag.matricula,
        ag.id_sala,
        ag.data,
        ag.hora_inicio,
        ag.hora_fim,
        ag.finalidade,
        ag.status
    ))
    conn.commit()

    cursor.execute(
        "SELECT * FROM Agendamento WHERE id = LAST_INSERT_ID()"
    )
    novo_ag = cursor.fetchone()

    cursor.close()
    conn.close()

    return novo_ag



@router.get("/", response_model=list[AgendamentoResponse])
def listar_agendamentos():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT a.*
    FROM Agendamento a
    """
    cursor.execute(query)
    agendamentos = cursor.fetchall()

    cursor.close()
    conn.close()

    return agendamentos


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Agendamento
from schemas import CancelamentoRequest

router = APIRouter(prefix="/agendamentos", tags=["Agendamentos"])


@router.put("/{id_agendamento}/cancelar")
def cancelar_agendamento(
    id_agendamento: int,
    _: CancelamentoRequest,
    db: Session = Depends(get_db)
):
    agendamento = (
        db.query(Agendamento)
        .filter(Agendamento.id == id_agendamento)
        .first()
    )

    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    if agendamento.status == "Cancelado":
        raise HTTPException(
            status_code=400,
            detail="Agendamento já está cancelado"
        )

    agendamento.status = "Cancelado"
    db.commit()

    return {"message": "Reserva cancelada com sucesso"}
