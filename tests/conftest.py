import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db

SQLALCHEMY_TEST_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def mock_notifications():
    """Mocka o notification_service para nao enviar emails reais nos testes."""
    with patch("notifications.notification_service") as mock:
        mock.sendWelcome = MagicMock()
        mock.sendPasswordChanged = MagicMock()
        mock.sendPasswordResetRequested = MagicMock()
        yield mock


@pytest.fixture(scope="session", autouse=True)
def setup_db(mock_notifications):
    from main import app  # importa depois do mock
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db():
    session = TestingSession()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture()
def client(db, mock_notifications):
    from main import app
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def cliente_registrado(client):
    payload = {
        "nome": "Israel Teste",
        "telefone": "21999999999",
        "email": "israel@teste.com",
        "senha": "Senha123!"
    }
    client.post("/auth/register", json=payload)
    return payload


@pytest.fixture()
def cliente_token(client, cliente_registrado):
    res = client.post("/auth/login", data={
        "username": cliente_registrado["email"],
        "password": cliente_registrado["senha"]
    })
    token = res.json().get("access_token")
    assert token is not None, f"Login falhou: {res.json()}"
    return token


@pytest.fixture()
def auth_headers(cliente_token):
    return {"Authorization": f"Bearer {cliente_token}"}
