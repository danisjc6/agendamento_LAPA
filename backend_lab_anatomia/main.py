from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import usuario, sala, agendamento, reserva

app = FastAPI(
    title="API - Laboratório de Anatomia",
    description="Sistema de gerenciamento de salas e agendamentos",
    version="1.0.0"
)

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # depois restringir
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


# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {"status": "API do Laboratório de Anatomia rodando"}
