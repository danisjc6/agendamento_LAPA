from fastapi import APIRouter, HTTPException
from database import get_db
from schemas import ReservaCreate, ReservaDetalhada

router = APIRouter(
    prefix="/reservas",
    tags=["Reservas"]
)


# =========================
# LISTAR RESERVAS DETALHADAS
# =========================
@router.get("/", response_model=list[ReservaDetalhada])
def listar_reservas():

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT 
        a.id_agendamento,
        a.data,
        a.hora_inicio,
        a.hora_fim,
        a.finalidade,
        a.status,
        s.nome_sala,
        s.capacidade,
        u.matricula,
        u.email AS email_usuario,
        u.nome AS nome_usuario
    FROM reservas r
    JOIN agendamentos a ON r.id_agendamento = a.id_agendamento
    JOIN salas s ON r.id_sala = s.id_sala
    JOIN usuarios u ON u.matricula = a.matricula
    ORDER BY a.data, a.hora_inicio
    """

    cursor.execute(query)
    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    return resultados


# =========================
# CRIAR RESERVA
# =========================
@router.post("/")
def criar_reserva(reserva: ReservaCreate):

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # 🔎 Verificar se agendamento existe
    cursor.execute(
        "SELECT * FROM agendamentos WHERE id_agendamento = %s",
        (reserva.id_agendamento,)
    )
    agendamento = cursor.fetchone()

    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    if agendamento["status"].lower() != "ativo":
        raise HTTPException(
            status_code=400,
            detail="Não é possível reservar um agendamento cancelado"
        )

    # 🚫 Verificar conflito de horário
    query_conflito = """
    SELECT * FROM reservas r
    JOIN agendamentos a ON r.id_agendamento = a.id_agendamento
    WHERE r.id_sala = %s
      AND a.data = %s
      AND a.status = 'ativo'
      AND a.hora_inicio < %s
      AND a.hora_fim > %s
    """

    cursor.execute(query_conflito, (
        reserva.id_sala,
        agendamento["data"],
        agendamento["hora_fim"],
        agendamento["hora_inicio"]
    ))

    conflito = cursor.fetchone()

    if conflito:
        raise HTTPException(
            status_code=409,
            detail="Sala já reservada nesse horário"
        )

    # ✅ Criar reserva
    cursor.execute(
        "INSERT INTO reservas (id_agendamento, id_sala) VALUES (%s, %s)",
        (reserva.id_agendamento, reserva.id_sala)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {"mensagem": "Reserva criada com sucesso"}
