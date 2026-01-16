from database import get_connection

# ---------- USUÁRIOS ----------
def inserir_usuario(matricula, nome, email, telefone, curso):
    conn = conectar()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO Usuario (matricula, nome, email, telefone, curso)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (matricula, nome, email, telefone, curso)
    )

    conn.commit()
    cur.close()
    conn.close()


def listar_usuarios():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Usuario")
    res = cur.fetchall()
    conn.close()
    return res

def inserir_usuario(dados):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Usuario (id_usuario, nome, curso) VALUES (%s,%s,%s)",
        dados
    )
    conn.commit()
    conn.close()


# ---------- SALAS ----------
def listar_salas():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Sala")
    res = cur.fetchall()
    conn.close()
    return res

def inserir_sala(dados):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Sala (nome_sala, tipo, capacidade) VALUES (%s,%s,%s)",
        dados
    )
    conn.commit()
    conn.close()


# ---------- PEÇAS ----------
def listar_pecas():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Peca_Anatomica")
    res = cur.fetchall()
    conn.close()
    return res

def inserir_peca(dados):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO Peca_Anatomica
        (descricao, numero, nome_peca, categoria, estado_conservacao, localizacao)
        VALUES (%s,%s,%s,%s,%s,%s)""",
        dados
    )
    conn.commit()
    conn.close()
