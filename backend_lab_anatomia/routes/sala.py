from datetime import date, datetime, time, timedelta
from fastapi import APIRouter, Query
from database import get_db
from schemas import HorarioDisponibilidade

router = APIRouter(
    prefix="/salas",
    tags=["Salas"]
)


# =========================
# GERAR BLOCOS DE 1H
# =========================
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


# =========================
# VERIFICAR DISPONIBILIDADE
# =========================
@router.get(
    "/{id_sala}/disponibilidade",
    response_model=list[HorarioDisponibilidade]
)
def verificar_disponibilidade(
    id_sala: int,
    data: date = Query(...)
):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    blocos = gerar_blocos()

    # 🔎 Buscar reservas ativas da sala na data
    query = """
        SELECT a.hora_inicio, a.hora_fim
        FROM reservas r
        JOIN agendamentos a ON r.id_agendamento = a.id_agendamento
        WHERE r.id_sala = %s
          AND a.data = %s
          AND a.status = 'ativo'
    """

    cursor.execute(query, (id_sala, data))
    reservas = cursor.fetchall()

    cursor.close()
    conn.close()

    # 🔴 Identificar horários ocupados
    ocupados = set()

    for r in reservas:
        atual = r["hora_inicio"]

        while atual < r["hora_fim"]:
            ocupados.add(atual)
            atual = (
                datetime.combine(date.today(), atual) + timedelta(hours=1)
            ).time()

    # 🟢 Gerar lista de disponíveis
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
