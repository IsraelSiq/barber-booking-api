from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# --- Auth ---
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    precisa_redefinir: bool = False


# --- Clientes ---
class ClienteCreate(BaseModel):
    nome: str
    telefone: str
    email: str
    senha: str


class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None


class ClienteResponse(BaseModel):
    id: int
    nome: str
    telefone: str
    email: str
    role: str
    precisa_redefinir: bool
    criado_em: datetime

    class Config:
        from_attributes = True


class RedefinirSenhaRequest(BaseModel):
    nova_senha: str


# --- Enderecos ---
class EnderecoCreate(BaseModel):
    apelido: str
    rua: str
    numero: str
    bairro: str
    cidade: str
    complemento: Optional[str] = None


class EnderecoResponse(BaseModel):
    id: int
    cliente_id: int
    apelido: str
    rua: str
    numero: str
    bairro: str
    cidade: str
    complemento: Optional[str]
    criado_em: datetime

    class Config:
        from_attributes = True


# --- Agendamentos ---
class AgendamentoCreate(BaseModel):
    data_hora: datetime
    servico: Optional[str] = "Corte"
    endereco_id: int


class AgendamentoResponse(BaseModel):
    id: int
    cliente_id: int
    endereco_id: Optional[int]
    data_hora: datetime
    servico: str
    status: str
    cancelado_por: Optional[str] = None
    motivo_cancelamento: Optional[str] = None
    criado_em: datetime

    class Config:
        from_attributes = True
