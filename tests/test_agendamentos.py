import pytest


@pytest.fixture()
def endereco_id(client, auth_headers):
    """Cria um endereço e retorna seu ID."""
    res = client.post("/enderecos/", json={
        "apelido": "Casa",
        "rua": "Rua das Flores",
        "numero": "42",
        "bairro": "Centro",
        "cidade": "Maricá"
    }, headers=auth_headers)
    return res.json()["id"]


def test_horarios_disponiveis(client):
    res = client.get("/agendamentos/disponiveis?data=2026-07-10")
    assert res.status_code == 200
    data = res.json()
    assert "horarios_disponiveis" in data
    assert isinstance(data["horarios_disponiveis"], list)


def test_horarios_data_invalida(client):
    res = client.get("/agendamentos/disponiveis?data=nao-e-data")
    assert res.status_code == 400


def test_criar_agendamento_sucesso(client, auth_headers, endereco_id):
    res = client.post("/agendamentos/", json={
        "data_hora": "2026-07-15T09:00:00",
        "servico": "Corte",
        "endereco_id": endereco_id
    }, headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["status"] == "confirmado"


def test_criar_agendamento_horario_nao_permitido(client, auth_headers, endereco_id):
    res = client.post("/agendamentos/", json={
        "data_hora": "2026-07-15T08:00:00",
        "servico": "Corte",
        "endereco_id": endereco_id
    }, headers=auth_headers)
    assert res.status_code == 400


def test_criar_agendamento_minuto_nao_zero(client, auth_headers, endereco_id):
    res = client.post("/agendamentos/", json={
        "data_hora": "2026-07-15T09:30:00",
        "servico": "Corte",
        "endereco_id": endereco_id
    }, headers=auth_headers)
    assert res.status_code == 400


def test_horario_ja_ocupado(client, auth_headers, endereco_id):
    payload = {
        "data_hora": "2026-07-20T10:00:00",
        "servico": "Corte",
        "endereco_id": endereco_id
    }
    client.post("/agendamentos/", json=payload, headers=auth_headers)
    res = client.post("/agendamentos/", json=payload, headers=auth_headers)
    assert res.status_code == 400
    assert "ocupado" in res.json()["detail"]


def test_criar_agendamento_sem_auth(client, endereco_id):
    res = client.post("/agendamentos/", json={
        "data_hora": "2026-07-16T09:00:00",
        "servico": "Corte",
        "endereco_id": endereco_id
    })
    assert res.status_code == 401


def test_meus_agendamentos(client, auth_headers, endereco_id):
    client.post("/agendamentos/", json={
        "data_hora": "2026-07-17T11:00:00",
        "servico": "Corte",
        "endereco_id": endereco_id
    }, headers=auth_headers)
    res = client.get("/agendamentos/meus", headers=auth_headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_buscar_agendamento_por_id(client, auth_headers, endereco_id):
    ag = client.post("/agendamentos/", json={
        "data_hora": "2026-07-18T14:00:00",
        "servico": "Corte",
        "endereco_id": endereco_id
    }, headers=auth_headers).json()
    res = client.get(f"/agendamentos/{ag['id']}")
    assert res.status_code == 200


def test_buscar_agendamento_inexistente(client):
    res = client.get("/agendamentos/99999")
    assert res.status_code == 404


def test_cancelar_agendamento(client, auth_headers, endereco_id):
    ag = client.post("/agendamentos/", json={
        "data_hora": "2026-07-19T15:00:00",
        "servico": "Corte",
        "endereco_id": endereco_id
    }, headers=auth_headers).json()
    res = client.delete(f"/agendamentos/{ag['id']}", headers=auth_headers)
    assert res.status_code == 200


def test_cancelar_agendamento_inexistente(client, auth_headers):
    res = client.delete("/agendamentos/99999", headers=auth_headers)
    assert res.status_code == 404
