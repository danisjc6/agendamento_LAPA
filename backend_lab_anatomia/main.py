from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from database import get_db
from fastapi.responses import StreamingResponse
from routes import usuario, sala, agendamento, reserva, relatorios

import io
import csv



app = FastAPI(
    title="API - Laboratório de Anatomia",
    description="Sistema de gerenciamento de salas e agendamentos",
    version="1.0.0"
)

# =========================
# CORS
# =========================
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # permite o frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# ROUTERS
# =========================

app.include_router(usuario.router)
app.include_router(sala.router)
app.include_router(agendamento.router)
app.include_router(reserva.router)
app.include_router(relatorios.router)


# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {"status": "API do Laboratório de Anatomia rodando"}


# =========================
# RELATÓRIO AGENDAMENTOS
# =========================


@app.get("/relatorios/agendamentos")
def relatorio_agendamentos(db = Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("SELECT * FROM vw_agendamentos_detalhados;")

    colunas = [desc[0] for desc in cursor.description]
    dados = cursor.fetchall()

    resultado = []
    for linha in dados:
        resultado.append(dict(zip(colunas, linha)))

    cursor.close()

    return resultado


@app.get("/relatorios/agendamentos/csv")
def relatorio_csv(db = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM vw_agendamentos_detalhados;")

    colunas = [desc[0] for desc in cursor.description]
    dados = cursor.fetchall()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(colunas)
    writer.writerows(dados)

    output.seek(0)

    cursor.close()

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=relatorio_agendamentos.csv"}
    )

