from database import get_connection

# =====================================================
# USUÁRIOS
# =====================================================

def inserir_usuario(usuario):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    sql = """
        INSERT INTO Usuario (matricula, nome, email, telefone, curso)
        VALUES (%s, %s, %s, %s, %s)
    """

    cur.execute(sql, (
        usuario.matricula,
        usuario.nome,
        usuario.email,
        usuario.telefone,
        usuario.curso
    ))

    conn.commit()
    cur.close()
    conn.close()

    return usuario


def listar_usuarios():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM Usuario")
    usuarios = cur.fetchall()

    cur.close()
    conn.close()
    return usuarios


def pegar_usuario(matricula):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM Usuario WHERE matricula = %s", (matricula,))
    usuario = cur.fetchone()

    cur.close()
    conn.close()
    return usuario


def atualizar_usuario(matricula, usuario):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    sql = """
        UPDATE Usuario
        SET nome=%s, email=%s, telefone=%s, curso=%s
        WHERE matricula=%s
    """

    cur.execute(sql, (
        usuario.nome,
        usuario.email,
        usuario.telefone,
        usuario.curso,
        matricula
    ))

    conn.commit()
    cur.close()
    conn.close()

    return pegar_usuario(matricula)


def deletar_usuario(matricula):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM Usuario WHERE matricula = %s", (matricula,))

    conn.commit()
    cur.close()
    conn.close()


# =====================================================
# SALAS
# =====================================================

def inserir_sala(sala):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    sql = """
        INSERT INTO Sala (nome_sala, tipo, capacidade)
        VALUES (%s, %s, %s)
    """

    cur.execute(sql, (
        sala.nome_sala,
        sala.tipo,
        sala.capacidade
    ))

    conn.commit()
    id_sala = cur.lastrowid

    cur.close()
    conn.close()

    return pegar_sala(id_sala)


def listar_salas():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM Sala")
    salas = cur.fetchall()

    cur.close()
    conn.close()
    return salas


def pegar_sala(id_sala):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM Sala WHERE id_sala = %s", (id_sala,))
    sala = cur.fetchone()

    cur.close()
    conn.close()
    return sala


def atualizar_sala(id_sala, sala):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    sql = """
        UPDATE Sala
        SET nome_sala=%s, tipo=%s, capacidade=%s
        WHERE id_sala=%s
    """

    cur.execute(sql, (
        sala.nome_sala,
        sala.tipo,
        sala.capacidade,
        id_sala
    ))

    conn.commit()
    cur.close()
    conn.close()

    return pegar_sala(id_sala)


def deletar_sala(id_sala):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM Sala WHERE id_sala = %s", (id_sala,))

    conn.commit()
    cur.close()
    conn.close()


# =====================================================
# AGENDAMENTOS
# =====================================================

def inserir_agendamento(agendamento):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    sql = """
        INSERT INTO Agendamento
        (data, horario_inicio, horario_fim, matricula_usuario, id_sala)
        VALUES (%s, %s, %s, %s, %s)
    """

    cur.execute(sql, (
        agendamento.data,
        agendamento.horario_inicio,
        agendamento.horario_fim,
        agendamento.matricula_usuario,
        agendamento.id_sala
    ))

    conn.commit()
    id_agendamento = cur.lastrowid

    cur.close()
    conn.close()

    return pegar_agendamento(id_agendamento)


def listar_agendamentos():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    sql = """
        SELECT a.*, u.nome AS nome_usuario, s.nome_sala
        FROM Agendamento a
        JOIN Usuario u ON a.matricula_usuario = u.matricula
        JOIN Sala s ON a.id_sala = s.id_sala
    """

    cur.execute(sql)
    agendamentos = cur.fetchall()

    cur.close()
    conn.close()
    return agendamentos


def pegar_agendamento(id_agendamento):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        "SELECT * FROM Agendamento WHERE id_agendamento = %s",
        (id_agendamento,)
    )

    agendamento = cur.fetchone()

    cur.close()
    conn.close()
    return agendamento


def atualizar_agendamento(id_agendamento, agendamento):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    sql = """
        UPDATE Agendamento
        SET data=%s,
            horario_inicio=%s,
            horario_fim=%s,
            matricula_usuario=%s,
            id_sala=%s
        WHERE id_agendamento=%s
    """

    cur.execute(sql, (
        agendamento.data,
        agendamento.horario_inicio,
        agendamento.horario_fim,
        agendamento.matricula_usuario,
        agendamento.id_sala,
        id_agendamento
    ))

    conn.commit()
    cur.close()
    conn.close()

    return pegar_agendamento(id_agendamento)


def deletar_agendamento(id_agendamento):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM Agendamento WHERE id_agendamento = %s",
        (id_agendamento,)
    )

    conn.commit()
    cur.close()
    conn.close()
