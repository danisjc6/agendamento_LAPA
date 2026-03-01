from fastapi import APIRouter
from database import get_db

router = APIRouter(
    prefix="/relatorios",
    tags=["Relatórios"]
)

@router.get("/relatorios")
def listar_relatorios():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM vw_agendamentos_detalhados
        ORDER BY data DESC, hora_inicio DESC
    """)

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados