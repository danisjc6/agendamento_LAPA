from fastapi import APIRouter
from database import get_connection
from schemas import AgendamentoCreate, AgendamentoResponse

router = APIRouter(prefix="/agendamentos", tags=["Agendamentos"])

@router.post("/", response_model=AgendamentoResponse)
def criar_agendamento(ag: AgendamentoCreate):
    conn = get_connection()
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
    conn = get_connection()
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
