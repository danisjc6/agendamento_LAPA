from datetime import date, datetime, time, timedelta
from fastapi import APIRouter, Query
from database import get_db
from schemas import HorarioDisponibilidade, SalaBase, SalaResponse, SalaCreate
from datetime import timedelta, datetime, time

router = APIRouter(
    prefix="/salas",
    tags=["Salas"]
)

# =========================
# LISTAR SALAS
# =========================

@router.get("/")
def listar_salas():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM salas")
    salas = cursor.fetchall()

    cursor.close()
    conn.close()

    return salas


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

    # 🔧 Função auxiliar 
    def converter_para_time(valor):
        if isinstance(valor, timedelta):
            total_segundos = int(valor.total_seconds())
            horas = total_segundos // 3600
            minutos = (total_segundos % 3600) // 60
            segundos = total_segundos % 60
            return time(horas, minutos, segundos)
        return valor

    # 🔴 Identificar horários ocupados
    ocupados = set()

    for inicio_bloco, fim_bloco in blocos:
        for r in reservas:
            inicio_reserva = converter_para_time(r["hora_inicio"])
            fim_reserva = converter_para_time(r["hora_fim"])

            # verifica se há sobreposição
            if inicio_bloco < fim_reserva and fim_bloco > inicio_reserva:
                ocupados.add(inicio_bloco)
                break


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