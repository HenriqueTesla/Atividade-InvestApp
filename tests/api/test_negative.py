import requests


def test_login_credenciais_invalidas(base_url):
    payload = {
        "username": "usuario_inexistente",
        "password": "senha_invalida",
    }

    response = requests.post(
        f"{base_url}/api/login",
        json=payload,
    )

    assert response.status_code == 400

    data = response.json()

    assert "detail" in data


def test_acesso_sem_token(base_url):
    response = requests.get(
        f"{base_url}/api/investments"
    )

    assert response.status_code == 401


def test_criar_investimento_payload_invalido(
    base_url,
    auth_headers,
):
    payload = {
        "asset_name": "CDB",
        "amount": "valor_invalido",
        "purchase_price": 1.0,
        "days_invested": 30,
        "planned_days": 365,
    }

    response = requests.post(
        f"{base_url}/api/investments",
        json=payload,
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_simulacao_mensal_payload_invalido(
    base_url,
    auth_headers,
):
    payload = {
        "months": "valor_invalido"
    }

    response = requests.post(
        f"{base_url}/api/simulate/yield-monthly",
        json=payload,
        headers=auth_headers,
    )

    assert response.status_code == 422
