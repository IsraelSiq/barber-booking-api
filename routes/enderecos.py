from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Endereco, Cliente
from schemas import EnderecoCreate, EnderecoResponse
from auth import get_cliente_atual
from typing import List

router = APIRouter()


@router.get("/", response_model=List[EnderecoResponse])
def listar_enderecos(
    db: Session = Depends(get_db),
    cliente_atual: Cliente = Depends(get_cliente_atual)
):
    return db.query(Endereco).filter(Endereco.cliente_id == cliente_atual.id).all()


@router.post("/", response_model=EnderecoResponse)
def criar_endereco(
    endereco: EnderecoCreate,
    db: Session = Depends(get_db),
    cliente_atual: Cliente = Depends(get_cliente_atual)
):
    novo = Endereco(cliente_id=cliente_atual.id, **endereco.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.delete("/{endereco_id}")
def deletar_endereco(
    endereco_id: int,
    db: Session = Depends(get_db),
    cliente_atual: Cliente = Depends(get_cliente_atual)
):
    end = db.query(Endereco).filter(
        Endereco.id == endereco_id,
        Endereco.cliente_id == cliente_atual.id
    ).first()
    if not end:
        raise HTTPException(status_code=404, detail="Endereço não encontrado.")
    db.delete(end)
    db.commit()
    return {"message": "Endereço removido com sucesso."}
