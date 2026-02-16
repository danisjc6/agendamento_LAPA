from fastapi import APIRouter, HTTPException
from typing import List
from database import get_db
from schemas import UsuarioCreate, UsuarioResponse

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


# =========================
# CRIAR USUÁRIO
# =========================
@router.post("/", response_model=UsuarioResponse)
def criar_usuario(usuario: UsuarioCreate):

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    query = """
        INSERT INTO Usuario (matricula, nome, email, tipo)
        VALUES (%s, %s, %s, %s)
    """

    try:
        cursor.execute(query, (
            usuario.matricula,
            usuario.nome,
            usuario.email,
            usuario.tipo
        ))
        conn.commit()

        cursor.execute(
            "SELECT * FROM Usuario WHERE matricula = %s",
            (usuario.matricula,)
        )

        novo_usuario = cursor.fetchone()

        return novo_usuario

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        cursor.close()
        conn.close()


# =========================
# LISTAR USUÁRIOS
# =========================
@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios():

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Usuario")
    usuarios = cursor.fetchall()

    cursor.close()
    conn.close()

    return usuarios


# =========================
# PEGAR USUÁRIO POR MATRÍCULA
# =========================
@router.get("/{matricula}", response_model=UsuarioResponse)
def pegar_usuario(matricula: int):

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM Usuario WHERE matricula = %s",
        (matricula,)
    )

    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return usuario


# =========================
# ATUALIZAR USUÁRIO
# =========================
@router.put("/{matricula}", response_model=UsuarioResponse)
def atualizar_usuario(matricula: int, usuario: UsuarioCreate):

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            UPDATE Usuario
            SET nome = %s,
                email = %s,
                tipo = %s
            WHERE matricula = %s
        """, (
            usuario.nome,
            usuario.email,
            usuario.tipo,
            matricula
        ))

        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        cursor.execute(
            "SELECT * FROM Usuario WHERE matricula = %s",
            (matricula,)
        )

        usuario_atualizado = cursor.fetchone()
        return usuario_atualizado

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        cursor.close()
        conn.close()


# =========================
# DELETAR USUÁRIO
# =========================
@router.delete("/{matricula}")
def deletar_usuario(matricula: int):

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "DELETE FROM Usuario WHERE matricula = %s",
            (matricula,)
        )

        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        return {"detail": "Usuário deletado com sucesso"}

    finally:
        cursor.close()
        conn.close()
