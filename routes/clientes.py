from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Cliente
from schemas import ClienteCreate, ClienteResponse
from auth import hash_senha, require_admin, get_cliente_atual
from typing import List

router = APIRouter()


@router.post("/", response_model=ClienteResponse)
def criar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    existente = db.query(Cliente).filter(Cliente.email == cliente.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    novo = Cliente(**cliente.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.get("/", response_model=List[ClienteResponse])
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(Cliente).all()


@router.get("/{cliente_id}", response_model=ClienteResponse)
def buscar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return cliente


@router.post("/{cliente_id}/reset-senha")
def reset_senha_admin(
    cliente_id: int,
    db: Session = Depends(get_db),
    admin: Cliente = Depends(require_admin)
):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    cliente.senha = hash_senha("teste123")
    cliente.precisa_redefinir = True
    db.commit()
    return {"message": f"Senha de {cliente.nome} resetada com sucesso. Ela precisará redefinir no próximo login."}
