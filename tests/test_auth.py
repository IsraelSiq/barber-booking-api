def test_registro_sucesso(client):
    res = client.post("/auth/register", json={
        "nome": "Novo User",
        "telefone": "21988887777",
        "email": "novo@teste.com",
        "senha": "Senha123!"
    })
    assert res.status_code in [200, 201]
    assert res.json()["email"] == "novo@teste.com"


def test_registro_email_duplicado(client):
    payload = {
        "nome": "Dup",
        "telefone": "21911111111",
        "email": "dup@teste.com",
        "senha": "Senha123!"
    }
    client.post("/auth/register", json=payload)
    res = client.post("/auth/register", json=payload)
    assert res.status_code == 400


def test_login_sucesso(client):
    client.post("/auth/register", json={
        "nome": "Login Test",
        "telefone": "21922223333",
        "email": "login@teste.com",
        "senha": "Senha123!"
    })
    res = client.post("/auth/login", data={
        "username": "login@teste.com",
        "password": "Senha123!"
    })
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_login_senha_errada(client):
    client.post("/auth/register", json={
        "nome": "Wrong Pass",
        "telefone": "21933334444",
        "email": "wrong@teste.com",
        "senha": "Senha123!"
    })
    res = client.post("/auth/login", data={
        "username": "wrong@teste.com",
        "password": "senhaerrada"
    })
    assert res.status_code == 401


def test_login_usuario_inexistente(client):
    res = client.post("/auth/login", data={
        "username": "naoexiste@teste.com",
        "password": "qualquer"
    })
    assert res.status_code == 401


def test_rota_protegida_sem_token(client):
    res = client.get("/agendamentos/meus")
    assert res.status_code in [401, 403]


def test_rota_protegida_token_invalido(client):
    res = client.get("/agendamentos/meus", headers={"Authorization": "Bearer token_invalido"})
    assert res.status_code in [401, 403]


def test_me_autenticado(client, auth_headers):
    res = client.get("/auth/me", headers=auth_headers)
    assert res.status_code == 200
    assert "email" in res.json()


def test_me_sem_auth(client):
    res = client.get("/auth/me")
    assert res.status_code in [401, 403]
