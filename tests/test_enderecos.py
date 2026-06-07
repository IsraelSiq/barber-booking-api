def test_criar_endereco(client, auth_headers):
    res = client.post("/enderecos/", json={
        "apelido": "Trabalho",
        "rua": "Av. Brasil",
        "numero": "100",
        "bairro": "Centro",
        "cidade": "Maricá"
    }, headers=auth_headers)
    assert res.status_code in [200, 201]
    assert res.json()["apelido"] == "Trabalho"


def test_criar_endereco_sem_auth(client):
    res = client.post("/enderecos/", json={
        "apelido": "Casa",
        "rua": "Rua X",
        "numero": "1",
        "bairro": "Bairro Y",
        "cidade": "Cidade Z"
    })
    assert res.status_code in [401, 403]


def test_listar_enderecos(client, auth_headers):
    res = client.get("/enderecos/", headers=auth_headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)
