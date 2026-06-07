def test_perfil_cliente_autenticado(client, auth_headers):
    res = client.get("/clientes/me", headers=auth_headers)
    assert res.status_code == 200
    assert "email" in res.json()


def test_perfil_sem_auth(client):
    res = client.get("/clientes/me")
    assert res.status_code == 401
