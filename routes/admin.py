from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Agendamento, Cliente, Endereco, BloqueioHorario
from auth import require_admin, hash_senha
from notifications import notification_service
from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()


class CancelamentoAdmin(BaseModel):
    motivo: str


class BloqueioCreate(BaseModel):
    data: str
    horario: str
    motivo: Optional[str] = None


@router.get("/agenda")
def agenda_do_dia(
    data: Optional[str] = None,
    db: Session = Depends(get_db),
    admin: Cliente = Depends(require_admin)
):
    data_obj = date.fromisoformat(data) if data else date.today()
    agendamentos = db.query(Agendamento).filter(
        Agendamento.status == "confirmado"
    ).all()
    resultado = []
    for ag in agendamentos:
        if ag.data_hora.date() != data_obj:
            continue
        cliente = db.query(Cliente).filter(Cliente.id == ag.cliente_id).first()
        endereco = db.query(Endereco).filter(Endereco.id == ag.endereco_id).first()
        resultado.append({
            "id": ag.id,
            "horario": ag.data_hora.strftime("%H:%M"),
            "servico": ag.servico,
            "status": ag.status,
            "cliente": {"nome": cliente.nome, "telefone": cliente.telefone} if cliente else None,
            "endereco": {
                "apelido": endereco.apelido,
                "rua": endereco.rua,
                "numero": endereco.numero,
                "bairro": endereco.bairro,
                "cidade": endereco.cidade,
                "complemento": endereco.complemento,
            } if endereco else None
        })
    resultado.sort(key=lambda x: x["horario"])
    return {"data": str(data_obj), "agendamentos": resultado}


@router.patch("/agendamentos/{agendamento_id}/concluir")
def concluir_agendamento(
    agendamento_id: int,
    db: Session = Depends(get_db),
    admin: Cliente = Depends(require_admin)
):
    ag = db.query(Agendamento).filter(Agendamento.id == agendamento_id).first()
    if not ag:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado.")
    ag.status = "concluido"
    db.commit()
    return {"message": "Agendamento concluído."}


@router.patch("/agendamentos/{agendamento_id}/cancelar")
def cancelar_pelo_barbeiro(
    agendamento_id: int,
    body: CancelamentoAdmin,
    db: Session = Depends(get_db),
    admin: Cliente = Depends(require_admin)
):
    ag = db.query(Agendamento).filter(Agendamento.id == agendamento_id).first()
    if not ag:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado.")
    ag.status = "cancelado_barbeiro"
    ag.motivo_cancelamento = body.motivo
    ag.cancelado_por = "barbeiro"
    db.commit()
    cliente = db.query(Cliente).filter(Cliente.id == ag.cliente_id).first()
    if cliente:
        notification_service.sendAppointmentCancelled(cliente, ag)
    return {"message": "Agendamento cancelado.", "motivo": body.motivo}


@router.get("/clientes")
def listar_clientes(
    db: Session = Depends(get_db),
    admin: Cliente = Depends(require_admin)
):
    clientes = db.query(Cliente).filter(Cliente.role == "cliente").all()
    return [{"id": c.id, "nome": c.nome, "telefone": c.telefone, "email": c.email, "criado_em": c.criado_em, "precisa_redefinir": c.precisa_redefinir} for c in clientes]


@router.post("/clientes/{cliente_id}/reset-senha")
def reset_senha_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    admin: Cliente = Depends(require_admin)
):
    """Admin reseta a senha do cliente para 'teste123' e força redefinição no próximo login."""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id, Cliente.role == "cliente").first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    cliente.senha = hash_senha("teste123")
    cliente.precisa_redefinir = True
    db.commit()
    db.refresh(cliente)
    notification_service.sendAdminPasswordReset(cliente)
    return {"message": f"Senha de {cliente.nome} redefinida. Cliente deverá criar nova senha no próximo login."}


@router.post("/bloqueios")
def bloquear_horario(
    body: BloqueioCreate,
    db: Session = Depends(get_db),
    admin: Cliente = Depends(require_admin)
):
    bloqueio = BloqueioHorario(
        data=date.fromisoformat(body.data),
        horario=body.horario,
        motivo=body.motivo
    )
    db.add(bloqueio)
    db.commit()
    db.refresh(bloqueio)
    return {"message": "Horário bloqueado.", "id": bloqueio.id}


@router.get("/bloqueios")
def listar_bloqueios(
    db: Session = Depends(get_db),
    admin: Cliente = Depends(require_admin)
):
    return db.query(BloqueioHorario).all()


@router.delete("/bloqueios/{bloqueio_id}")
def remover_bloqueio(
    bloqueio_id: int,
    db: Session = Depends(get_db),
    admin: Cliente = Depends(require_admin)
):
    b = db.query(BloqueioHorario).filter(BloqueioHorario.id == bloqueio_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Bloqueio não encontrado.")
    db.delete(b)
    db.commit()
    return {"message": "Bloqueio removido."}
