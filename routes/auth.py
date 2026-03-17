import secrets
import httpx
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models import Cliente, PasswordResetToken
from schemas import (
    ClienteCreate, ClienteUpdate, ClienteResponse,
    TokenResponse, RedefinirSenhaRequest,
    ForgotPasswordRequest, ResetPasswordRequest
)
from auth import hash_senha, verificar_senha, criar_token, get_cliente_atual
from notifications import notification_service
from pydantic import BaseModel

router = APIRouter()

GOOGLE_CLIENT_ID = "601696539112-1sj0k9gffuer3es8jbidtpa8l6dee9jk.apps.googleusercontent.com"


class GoogleLoginRequest(BaseModel):
    credential: str


class GoogleTokenRequest(BaseModel):
    access_token: str
    email: str
    nome: str
    google_id: str


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
    notification_service.sendWelcome(novo)
    return novo


@router.post("/login", response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.email == form.username).first()
    if not cliente or not cliente.senha or not verificar_senha(form.password, cliente.senha):
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


@router.post("/google", response_model=TokenResponse)
def login_google(body: GoogleLoginRequest, db: Session = Depends(get_db)):
    """Valida o id_token Google (fluxo antigo) e retorna JWT da aplicação."""
    try:
        response = httpx.get(
            f"https://oauth2.googleapis.com/tokeninfo?id_token={body.credential}",
            timeout=10
        )
        info = response.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Erro ao validar token Google.")

    if info.get("aud") != GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=401, detail="Token Google inválido.")

    email = info.get("email")
    google_id = info.get("sub")
    nome = info.get("name", email)

    if not email:
        raise HTTPException(status_code=400, detail="Email não retornado pelo Google.")

    cliente = db.query(Cliente).filter(Cliente.email == email).first()
    if cliente:
        if not cliente.google_id:
            cliente.google_id = google_id
            db.commit()
            db.refresh(cliente)
    else:
        cliente = Cliente(
            nome=nome, email=email, telefone="",
            senha=None, google_id=google_id,
            role="cliente", precisa_redefinir=False
        )
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        notification_service.sendWelcome(cliente)

    token = criar_token({"sub": cliente.email})
    return {"access_token": token, "token_type": "bearer", "precisa_redefinir": False}


@router.post("/google-token", response_model=TokenResponse)
def login_google_token(body: GoogleTokenRequest, db: Session = Depends(get_db)):
    """Recebe dados do usuário Google via userinfo e retorna JWT da aplicação."""
    # Valida o access_token com o Google
    try:
        response = httpx.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {body.access_token}"},
            timeout=10
        )
        info = response.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Erro ao validar token Google.")

    if "email" not in info:
        raise HTTPException(status_code=401, detail="Token Google inválido.")

    email = info["email"]
    google_id = info["sub"]
    nome = info.get("name", email)

    cliente = db.query(Cliente).filter(Cliente.email == email).first()
    if cliente:
        if not cliente.google_id:
            cliente.google_id = google_id
            db.commit()
            db.refresh(cliente)
    else:
        cliente = Cliente(
            nome=nome, email=email, telefone="",
            senha=None, google_id=google_id,
            role="cliente", precisa_redefinir=False
        )
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        notification_service.sendWelcome(cliente)

    token = criar_token({"sub": cliente.email})
    return {"access_token": token, "token_type": "bearer", "precisa_redefinir": False}


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
    notification_service.sendPasswordChanged(cliente_atual)
    return cliente_atual


@router.post("/forgot-password")
def forgot_password(body: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Gera token de reset de senha válido por 1h. Sempre retorna 200 (segurança)."""
    cliente = db.query(Cliente).filter(Cliente.email == body.email).first()
    if cliente:
        token_str = secrets.token_urlsafe(32)
        expira = datetime.utcnow() + timedelta(hours=1)
        reset_token = PasswordResetToken(
            cliente_id=cliente.id,
            token=token_str,
            expira_em=expira
        )
        db.add(reset_token)
        db.commit()
        notification_service.sendPasswordResetRequested(cliente, token_str)
    return {"message": "Se o email estiver cadastrado, você receberá as instruções."}


@router.get("/reset-password")
def validar_token_reset(token: str, db: Session = Depends(get_db)):
    """Valida se o token de reset é válido e não expirou."""
    reset = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == token,
        PasswordResetToken.usado == False
    ).first()
    if not reset or reset.expira_em < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token inválido ou expirado.")
    return {"valid": True}


@router.post("/reset-password")
def reset_password(body: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Redefine a senha usando o token de reset."""
    reset = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == body.token,
        PasswordResetToken.usado == False
    ).first()
    if not reset or reset.expira_em < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token inválido ou expirado.")
    cliente = db.query(Cliente).filter(Cliente.id == reset.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    cliente.senha = hash_senha(body.nova_senha)
    cliente.precisa_redefinir = False
    reset.usado = True
    db.commit()
    notification_service.sendPasswordChanged(cliente)
    return {"message": "Senha redefinida com sucesso."}
