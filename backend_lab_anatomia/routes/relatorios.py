import csv
import io
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from database import get_db

router = APIRouter(
    prefix="/relatorios",
    tags=["Relatórios"]
)

VIEWS_MAP = {
    "agendamentos_detalhados": {
        "sql": """
            SELECT *
            FROM vw_agendamentos_detalhados
            ORDER BY data DESC, hora_inicio DESC, id_agendamento DESC
        """,
        "filename": "vw_agendamentos_detalhados.csv"
    },
    "salas_mais_utilizadas": {
        "sql": """
            SELECT *
            FROM vw_salas_mais_utilizadas
            ORDER BY total_reservas DESC, nome_sala ASC
        """,
        "filename": "vw_salas_mais_utilizadas.csv"
    },
    "agendamentos_ativos": {
        "sql": """
            SELECT *
            FROM vw_agendamentos_ativos
            ORDER BY data DESC, hora_inicio DESC, id_agendamento DESC
        """,
        "filename": "vw_agendamentos_ativos.csv"
    },
    "ocupacao_salas_por_data": {
        "sql": """
            SELECT *
            FROM vw_ocupacao_salas_por_data
            ORDER BY data DESC, total_agendamentos DESC, sala ASC
        """,
        "filename": "vw_ocupacao_salas_por_data.csv"
    },
    "salas_livres": {
        "sql": """
            SELECT *
            FROM vw_salas_livres
            ORDER BY nome_sala ASC
        """,
        "filename": "vw_salas_livres.csv"
    }
}


def _obter_view_config(view_nome: str):
    config = VIEWS_MAP.get(view_nome)
    if not config:
        raise HTTPException(status_code=404, detail="View não encontrada")
    return config


@router.get("/views")
def listar_views_disponiveis():
    return [{"id": chave, "arquivo_csv": valor["filename"]} for chave, valor in VIEWS_MAP.items()]


@router.get("/views/{view_nome}")
def listar_view(view_nome: str):
    config = _obter_view_config(view_nome)

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(config["sql"])

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados


@router.get("/views/{view_nome}/csv")
def exportar_view_csv(view_nome: str):
    config = _obter_view_config(view_nome)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(config["sql"])

    colunas = [desc[0] for desc in cursor.description]
    dados = cursor.fetchall()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(colunas)
    writer.writerows(dados)
    output.seek(0)

    cursor.close()
    conn.close()

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={config['filename']}"}
    )
