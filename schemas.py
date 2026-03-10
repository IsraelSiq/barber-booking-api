from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# --- Auth ---
class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# --- Clientes ---
class ClienteCreate(BaseModel):
    nome: str
    telefone: str
    email: str
    senha: str
    endereco: Optional[str] = None


class ClienteResponse(BaseModel):
    id: int
    nome: str
    telefone: str
    email: str
    endereco: Optional[str]
    criado_em: datetime

    class Config:
        from_attributes = True


# --- Agendamentos ---
class AgendamentoCreate(BaseModel):
    data_hora: datetime
    servico: Optional[str] = "Corte"


class AgendamentoResponse(BaseModel):
    id: int
    cliente_id: int
    data_hora: datetime
    servico: str
    status: str
    criado_em: datetime

    class Config:
        from_attributes = True
