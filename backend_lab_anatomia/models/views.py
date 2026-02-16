from models.base import get_connection


# =========================
# FUNÇÃO AUXILIAR GENÉRICA
# =========================

def executar_query(query, params=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        return resultados
    finally:
        cursor.close()
        conn.close()


# =========================
# VIEW - AGENDAMENTOS
# =========================

def listar_agendamentos_detalhados():
    return executar_query(
        "SELECT * FROM vw_agendamentos_detalhados"
    )


def listar_agendamentos_por_data(data):
    return executar_query(
        "SELECT * FROM vw_agendamentos_detalhados WHERE data = %s",
        (data,)
    )


def listar_agendamentos_ativos(data):
    return executar_query(
        "SELECT * FROM vw_agendamentos_ativos WHERE data = %s",
        (data,)
    )


# =========================
# VIEW - OCUPAÇÃO SALAS
# =========================

def listar_ocupacao_salas():
    return executar_query(
        "SELECT * FROM vw_ocupacao_salas"
    )


def listar_salas_livres():
    return executar_query(
        "SELECT * FROM vw_salas_livres"
    )


def listar_ocupacao_salas_por_data(data):
    return executar_query(
        "SELECT * FROM vw_ocupacao_salas_por_data WHERE data = %s",
        (data,)
    )


# =========================
# VIEW - ESTATÍSTICAS
# =========================

def listar_modelos_mais_utilizados():
    return executar_query(
        "SELECT * FROM vw_modelos_mais_utilizados"
    )


def listar_salas_mais_utilizadas():
    return executar_query(
        "SELECT * FROM vw_salas_mais_utilizadas"
    )
