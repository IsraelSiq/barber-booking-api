from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models import Cliente
from schemas import ClienteCreate, ClienteUpdate, ClienteResponse, TokenResponse, RedefinirSenhaRequest
from auth import hash_senha, verificar_senha, criar_token, get_cliente_atual

router = APIRouter()


@router.post("/register", response_model=ClienteResponse)
def register(cliente: ClienteCreate, db: Session = Depends(get_db)):
    existente = db.query(Cliente).filter(Cliente.email == cliente.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    dados = cliente.model_dump()
    dados["senha"] = hash_senha(dados["senha"])
    novo = Cliente(**dados)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.post("/login", response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.email == form.username).first()
    if not cliente or not verificar_senha(form.password, cliente.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos."
        )
    token = criar_token({"sub": cliente.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "precisa_redefinir": cliente.precisa_redefinir
    }


@router.get("/me", response_model=ClienteResponse)
def me(cliente_atual: Cliente = Depends(get_cliente_atual)):
    return cliente_atual


@router.put("/me", response_model=ClienteResponse)
def atualizar_me(
    dados: ClienteUpdate,
    db: Session = Depends(get_db),
    cliente_atual: Cliente = Depends(get_cliente_atual)
):
    if dados.nome is not None:
        cliente_atual.nome = dados.nome
    if dados.telefone is not None:
        cliente_atual.telefone = dados.telefone
    db.commit()
    db.refresh(cliente_atual)
    return cliente_atual


@router.post("/redefinir-senha", response_model=ClienteResponse)
def redefinir_senha(
    dados: RedefinirSenhaRequest,
    db: Session = Depends(get_db),
    cliente_atual: Cliente = Depends(get_cliente_atual)
):
    if not cliente_atual.precisa_redefinir:
        raise HTTPException(status_code=400, detail="Redefinição de senha não solicitada.")
    cliente_atual.senha = hash_senha(dados.nova_senha)
    cliente_atual.precisa_redefinir = False
    db.commit()
    db.refresh(cliente_atual)
    return cliente_atual
