def test_todos_agendamentos_sem_admin(client, auth_headers):
    """Cliente comum nao pode acessar rota de admin."""
    res = client.get("/agendamentos/todos", headers=auth_headers)
    assert res.status_code in [401, 403]


def test_todos_agendamentos_sem_auth(client):
    res = client.get("/agendamentos/todos")
    assert res.status_code in [401, 403]
