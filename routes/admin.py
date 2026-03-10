from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Cliente
from pydantic import BaseModel

router = APIRouter()

ADMIN_SECRET = "barber-admin-2026"


class PromoverRequest(BaseModel):
    email: str
    secret: str


@router.post("/promover")
def promover_admin(body: PromoverRequest, db: Session = Depends(get_db)):
    if body.secret != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Senha secreta incorreta.")
    cliente = db.query(Cliente).filter(Cliente.email == body.email).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente n\u00e3o encontrado.")
    cliente.role = "admin"
    db.commit()
    return {"message": f"{cliente.nome} agora \u00e9 admin!"}
