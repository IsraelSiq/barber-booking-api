import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

SQLALCHEMY_TEST_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_db():
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
def client(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def cliente_registrado(client):
    """Registra um cliente e retorna email/senha."""
    payload = {
        "nome": "Israel Teste",
        "email": "israel@teste.com",
        "senha": "Senha123!"
    }
    client.post("/auth/register", json=payload)
    return payload


@pytest.fixture()
def cliente_token(client, cliente_registrado):
    """Faz login e retorna o access_token JWT."""
    res = client.post("/auth/login", data={
        "username": cliente_registrado["email"],
        "password": cliente_registrado["senha"]
    })
    return res.json().get("access_token")


@pytest.fixture()
def auth_headers(cliente_token):
    return {"Authorization": f"Bearer {cliente_token}"}
