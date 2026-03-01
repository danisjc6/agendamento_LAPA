from fastapi import APIRouter, HTTPException
from database import get_db
from schemas import AgendamentoCreate, AgendamentoResponse, CancelamentoRequest

router = APIRouter(
    prefix="/agendamentos",
    tags=["Agendamentos"]
)


# =========================
# CRIAR AGENDAMENTO + RESERVA
# =========================
@router.post("/", response_model=AgendamentoResponse)
def criar_agendamento(ag: AgendamentoCreate):

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    try:
        # 🔎 Verificar conflito antes de criar
        query_conflito = """
            SELECT 1
            FROM reservas r
            JOIN agendamentos a
                ON r.id_agendamento = a.id_agendamento
            WHERE r.id_sala = %s
              AND a.data = %s
              AND a.status = 'ativo'
              AND %s < a.hora_fim
              AND %s > a.hora_inicio
        """

        cursor.execute(query_conflito, (
            ag.id_sala,
            ag.data,
            ag.hora_inicio,
            ag.hora_fim
        ))

        if cursor.fetchone():
            raise HTTPException(
                status_code=409,
                detail="Sala já reservada nesse horário"
            )

        # 1️⃣ Inserir agendamento
        cursor.execute("""
            INSERT INTO agendamentos
            (matricula, data, hora_inicio, hora_fim, finalidade, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            ag.matricula,
            ag.data,
            ag.hora_inicio,
            ag.hora_fim,
            ag.finalidade,
            ag.status
        ))

        id_agendamento = cursor.lastrowid

        # 2️⃣ Inserir reserva
        cursor.execute("""
            INSERT INTO reservas (id_agendamento, id_sala)
            VALUES (%s, %s)
        """, (
            id_agendamento,
            ag.id_sala
        ))

        conn.commit()

        # 3️⃣ Retornar criado
        cursor.execute(
            "SELECT * FROM agendamentos WHERE id_agendamento = %s",
            (id_agendamento,)
        )

        return cursor.fetchone()

    except HTTPException:
        conn.rollback()
        raise

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        cursor.close()
        conn.close()


# =========================
# LISTAR AGENDAMENTOS
# =========================
from datetime import timedelta

@router.get("/", response_model=list[AgendamentoResponse])
def listar_agendamentos():

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM agendamentos")
        dados = cursor.fetchall()

        for registro in dados:
            if isinstance(registro["hora_inicio"], timedelta):
                total_segundos = int(registro["hora_inicio"].total_seconds())
                horas = total_segundos // 3600
                minutos = (total_segundos % 3600) // 60
                segundos = total_segundos % 60
                registro["hora_inicio"] = f"{horas:02}:{minutos:02}:{segundos:02}"

            if isinstance(registro["hora_fim"], timedelta):
                total_segundos = int(registro["hora_fim"].total_seconds())
                horas = total_segundos // 3600
                minutos = (total_segundos % 3600) // 60
                segundos = total_segundos % 60
                registro["hora_fim"] = f"{horas:02}:{minutos:02}:{segundos:02}"

        return dados

    finally:
        cursor.close()
        conn.close()

# =========================
# CANCELAR AGENDAMENTO
# =========================
@router.put("/{id_agendamento}/cancelar")
def cancelar_agendamento(
    id_agendamento: int,
    _: CancelamentoRequest
):

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT status FROM agendamentos WHERE id_agendamento = %s",
            (id_agendamento,)
        )

        agendamento = cursor.fetchone()

        if not agendamento:
            raise HTTPException(
                status_code=404,
                detail="Agendamento não encontrado"
            )

        if agendamento["status"] == "cancelado":
            raise HTTPException(
                status_code=400,
                detail="Agendamento já está cancelado"
            )

        cursor.execute(
            "UPDATE agendamentos SET status = 'cancelado' WHERE id_agendamento = %s",
            (id_agendamento,)
        )

        conn.commit()

        return {"message": "Agendamento cancelado com sucesso"}

    finally:
        cursor.close()
        conn.close()


