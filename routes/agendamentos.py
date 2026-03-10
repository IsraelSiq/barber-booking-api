from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Agendamento, Cliente
from schemas import AgendamentoCreate, AgendamentoResponse
from auth import get_cliente_atual, require_admin
from datetime import date
from typing import List

router = APIRouter()

HORARIOS = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00", "17:00"]


@router.get("/disponiveis")
def horarios_disponiveis(data: str, db: Session = Depends(get_db)):
    try:
        data_obj = date.fromisoformat(data)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use YYYY-MM-DD.")

    agendados = db.query(Agendamento).filter(
        Agendamento.status == "confirmado"
    ).all()

    horarios_ocupados = [
        a.data_hora.strftime("%H:%M")
        for a in agendados
        if a.data_hora.date() == data_obj
    ]

    disponiveis = [h for h in HORARIOS if h not in horarios_ocupados]
    return {"data": data, "horarios_disponiveis": disponiveis}


@router.post("/", response_model=AgendamentoResponse)
def criar_agendamento(
    agendamento: AgendamentoCreate,
    db: Session = Depends(get_db),
    cliente_atual: Cliente = Depends(get_cliente_atual)
):
    conflito = db.query(Agendamento).filter(
        Agendamento.data_hora == agendamento.data_hora,
        Agendamento.status == "confirmado"
    ).first()
    if conflito:
        raise HTTPException(status_code=400, detail="Horário já ocupado.")

    novo = Agendamento(
        cliente_id=cliente_atual.id,
        data_hora=agendamento.data_hora,
        servico=agendamento.servico
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.get("/meus", response_model=List[AgendamentoResponse])
def meus_agendamentos(
    db: Session = Depends(get_db),
    cliente_atual: Cliente = Depends(get_cliente_atual)
):
    return db.query(Agendamento).filter(
        Agendamento.cliente_id == cliente_atual.id
    ).all()


@router.get("/dia", response_model=List[AgendamentoResponse])
def agendamentos_do_dia(
    data: str,
    db: Session = Depends(get_db),
    admin: Cliente = Depends(require_admin)
):
    """Painel do barbeiro — lista todos os agendamentos de um dia. Requer role admin."""
    try:
        data_obj = date.fromisoformat(data)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use YYYY-MM-DD.")

    agendamentos = db.query(Agendamento).filter(
        Agendamento.status == "confirmado"
    ).all()

    return [
        ag for ag in agendamentos
        if ag.data_hora.date() == data_obj
    ]


@router.get("/{agendamento_id}", response_model=AgendamentoResponse)
def buscar_agendamento(agendamento_id: int, db: Session = Depends(get_db)):
    ag = db.query(Agendamento).filter(Agendamento.id == agendamento_id).first()
    if not ag:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado.")
    return ag


@router.delete("/{agendamento_id}")
def cancelar_agendamento(
    agendamento_id: int,
    db: Session = Depends(get_db),
    cliente_atual: Cliente = Depends(get_cliente_atual)
):
    ag = db.query(Agendamento).filter(
        Agendamento.id == agendamento_id,
        Agendamento.cliente_id == cliente_atual.id
    ).first()
    if not ag:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado ou não pertence a você.")
    ag.status = "cancelado"
    db.commit()
    return {"message": f"Agendamento {agendamento_id} cancelado com sucesso."}
