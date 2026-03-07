from fastapi import APIRouter, HTTPException
from database import get_db
from schemas import AgendamentoCreate, AgendamentoResponse, CancelamentoRequest
import mysql.connector
from datetime import timedelta, time

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
        hora_minima = time(8, 0)
        hora_maxima = time(18, 0)

        if ag.hora_inicio < hora_minima or ag.hora_inicio > hora_maxima:
            raise HTTPException(
                status_code=400,
                detail="Hora de início deve estar entre 08:00 e 18:00"
            )

        if ag.hora_fim < hora_minima or ag.hora_fim > hora_maxima:
            raise HTTPException(
                status_code=400,
                detail="Hora de fim deve estar entre 08:00 e 18:00"
            )

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

        # ✅ Inserir agendamento
        cursor.execute("""
            INSERT INTO agendamentos
            (matricula, data, hora_inicio, hora_fim, finalidade)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            ag.matricula,
            ag.data,
            ag.hora_inicio,
            ag.hora_fim,
            ag.finalidade,
        ))

        id_agendamento = cursor.lastrowid

        # ✅ Inserir reserva
        cursor.execute("""
            INSERT INTO reservas (id_agendamento, id_sala)
            VALUES (%s, %s)
        """, (
            id_agendamento,
            ag.id_sala
        ))

        conn.commit()

        # ✅ Buscar registro completo
        cursor.execute("""
            SELECT 
                id_agendamento,
                matricula,
                data,
                hora_inicio,
                hora_fim,
                finalidade,
                status
            FROM agendamentos
            WHERE id_agendamento = %s
        """, (id_agendamento,))

        registro = cursor.fetchone()

        # 🔄 Converter timedelta se necessário
        from datetime import timedelta

        if isinstance(registro["hora_inicio"], timedelta):
            total = int(registro["hora_inicio"].total_seconds())
            h = total // 3600
            m = (total % 3600) // 60
            s = total % 60
            registro["hora_inicio"] = f"{h:02}:{m:02}:{s:02}"

        if isinstance(registro["hora_fim"], timedelta):
            total = int(registro["hora_fim"].total_seconds())
            h = total // 3600
            m = (total % 3600) // 60
            s = total % 60
            registro["hora_fim"] = f"{h:02}:{m:02}:{s:02}"

        return registro

    except HTTPException:
        conn.rollback()
        raise

    except mysql.connector.Error as err:
        conn.rollback()

        if err.sqlstate == '45000':
            raise HTTPException(status_code=400, detail=err.msg)

        raise HTTPException(status_code=500, detail="Erro no banco de dados.")

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
        # 🔄 Atualiza automaticamente os que já passaram
        cursor.execute("""
            UPDATE agendamentos
            SET status = 'finalizado'
            WHERE TIMESTAMP(data, hora_inicio) < NOW()
            AND status = 'ativo'
        """)
        conn.commit()

        # 📋 Buscar agendamentos
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



    
