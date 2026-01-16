from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.usuario import Usuario
from schemas import UsuarioCreate, UsuarioResponse

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)

# =========================
# Criar usuário
# =========================
@router.post("/", response_model=UsuarioResponse)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):

    usuario_existente = db.query(Usuario).filter(
        Usuario.matricula == usuario.matricula
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="Usuário com essa matrícula já existe"
        )

    novo_usuario = Usuario(
        matricula=usuario.matricula,
        nome=usuario.nome,
        email=usuario.email,
        telefone=usuario.telefone,
        curso=usuario.curso
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario


# =========================
# Listar usuários
# =========================
@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()


# =========================
# Buscar usuário por matrícula
# =========================
@router.get("/{matricula}", response_model=UsuarioResponse)
def buscar_usuario(matricula: int, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(
        Usuario.matricula == matricula
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return usuario
