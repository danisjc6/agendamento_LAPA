from fastapi import FastAPI, HTTPException
from typing import List
from routes import usuario, sala, agendamento, reserva
from fastapi.middleware.cors import CORSMiddleware

import models
import schemas

app = FastAPI()

app.include_router(usuario.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(sala.router, prefix="/salas", tags=["Salas"])
app.include_router(agendamento.router, prefix="/agendamentos", tags=["Agendamentos"])
app.include_router(reserva.router, prefix="/reservas", tags=["Reservas"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # depois podemos restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# ROTAS USUÁRIOS
# =========================

@app.post("/usuarios", response_model=schemas.UsuarioResponse)
def criar_usuario(usuario: schemas.UsuarioCreate):
    try:
        novo_usuario = models.inserir_usuario(usuario)
        return novo_usuario
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/usuarios", response_model=List[schemas.UsuarioResponse])
def listar_usuarios():
    return models.listar_usuarios()


@app.get("/usuarios/{matricula}", response_model=schemas.UsuarioResponse)
def pegar_usuario(matricula: int):
    usuario = models.pegar_usuario(matricula)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario


@app.put("/usuarios/{matricula}", response_model=schemas.UsuarioResponse)
def atualizar_usuario(matricula: int, usuario: schemas.UsuarioCreate):
    try:
        atualizado = models.atualizar_usuario(matricula, usuario)
        return atualizado
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/usuarios/{matricula}")
def deletar_usuario(matricula: int):
    try:
        models.deletar_usuario(matricula)
        return {"detail": "Usuário deletado"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# =========================
# ROTAS SALAS
# =========================

@app.post("/salas", response_model=schemas.SalaResponse)
def criar_sala(sala: schemas.SalaCreate):
    try:
        return models.inserir_sala(sala)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/salas", response_model=List[schemas.SalaResponse])
def listar_salas():
    return models.listar_salas()


@app.get("/salas/{id_sala}", response_model=schemas.SalaResponse)
def pegar_sala(id_sala: int):
    sala = models.pegar_sala(id_sala)
    if sala is None:
        raise HTTPException(status_code=404, detail="Sala não encontrada")
    return sala


@app.put("/salas/{id_sala}", response_model=schemas.SalaResponse)
def atualizar_sala(id_sala: int, sala: schemas.SalaCreate):
    try:
        return models.atualizar_sala(id_sala, sala)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/salas/{id_sala}")
def deletar_sala(id_sala: int):
    try:
        models.deletar_sala(id_sala)
        return {"detail": "Sala deletada"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# =========================
# ROTAS AGENDAMENTOS
# =========================

@app.post("/agendamentos", response_model=schemas.AgendamentoResponse)
def criar_agendamento(agendamento: schemas.AgendamentoCreate):
    try:
        return models.inserir_agendamento(agendamento)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/agendamentos", response_model=List[schemas.AgendamentoResponse])
def listar_agendamentos():
    return models.listar_agendamentos()


@app.get("/agendamentos/{id_agendamento}", response_model=schemas.AgendamentoResponse)
def pegar_agendamento(id_agendamento: int):
    agendamento = models.pegar_agendamento(id_agendamento)
    if agendamento is None:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    return agendamento


@app.put("/agendamentos/{id_agendamento}", response_model=schemas.AgendamentoResponse)
def atualizar_agendamento(id_agendamento: int, agendamento: schemas.AgendamentoCreate):
    try:
        return models.atualizar_agendamento(id_agendamento, agendamento)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/agendamentos/{id_agendamento}")
def deletar_agendamento(id_agendamento: int):
    try:
        models.deletar_agendamento(id_agendamento)
        return {"detail": "Agendamento deletado"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
