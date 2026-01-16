from fastapi import FastAPI
from pydantic import BaseModel
import models

app = FastAPI(title="API Anatomia")

# ====== SCHEMAS ======
class Usuario(BaseModel):
    id_usuario: int
    nome: str
    curso: str

class Sala(BaseModel):
    nome_sala: str
    tipo: str
    capacidade: int

class Peca(BaseModel):
    descricao: str
    numero: int
    nome_peca: str
    categoria: str
    estado_conservacao: str
    localizacao: str

# ====== ROTAS ======

@app.get("/usuarios")
def get_usuarios():
    return models.listar_usuarios()

@app.post("/usuarios")
def post_usuario(usuario: Usuario):
    models.inserir_usuario(
        usuario.matricula,
        usuario.nome,
        usuario.email,
        usuario.telefone,
        usuario.curso
    )
    return {"mensagem": "Usuário cadastrado com sucesso"}


@app.get("/salas")
def get_salas():
    return models.listar_salas()

@app.post("/salas")
def post_sala(sala: Sala):
    models.inserir_sala(
        (sala.nome_sala, sala.tipo, sala.capacidade)
    )
    return {"status": "Sala inserida"}


@app.get("/pecas")
def get_pecas():
    return models.listar_pecas()

@app.post("/pecas")
def post_peca(peca: Peca):
    models.inserir_peca(
        (peca.descricao, peca.numero, peca.nome_peca,
         peca.categoria, peca.estado_conservacao, peca.localizacao)
    )
    return {"status": "Peça inserida"}

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # depois restringimos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
