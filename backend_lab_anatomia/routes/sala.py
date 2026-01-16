from fastapi import APIRouter
from database import get_connection
from schemas import SalaCreate, SalaResponse

router = APIRouter(prefix="/salas", tags=["Salas"])


@router.post("/", response_model=SalaResponse)
def criar_sala(sala: SalaCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    INSERT INTO Sala (nome_sala, tipo, capacidade)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query, (
        sala.nome_sala,
        sala.tipo,
        sala.capacidade
    ))
    conn.commit()

    cursor.execute(
        "SELECT * FROM Sala WHERE id_sala = LAST_INSERT_ID()"
    )
    nova_sala = cursor.fetchone()

    cursor.close()
    conn.close()

    return nova_sala



@router.get("/", response_model=list[SalaResponse])
def listar_salas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Sala")
    salas = cursor.fetchall()

    cursor.close()
    conn.close()

    return salas
