import os
import requests

TEST_USER = os.getenv("TEST_USER")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")


def test_fluxo_geral(base_url):
    payload = {
        "username": TEST_USER,
        "password": TEST_PASSWORD,
    }

    response = requests.post(
        f"{base_url}/api/login",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    token = data["access_token"]

    auth_headers = {
        "Authorization": f"Bearer {token}",
    }

    response = requests.get(
        f"{base_url}/api/assets"
    )

    assert response.status_code == 200

    assets = response.json()

    assert isinstance(assets, list)
    assert len(assets) > 0

    poupanca = None

    for asset in assets:
        if asset["asset_name"] == "Poupança":
            poupanca = asset
            break

    assert poupanca is not None
    assert "asset_name" in poupanca
    assert "annual_rate" in poupanca

    rate_original = poupanca["annual_rate"]

    assert rate_original is not None

    nova_rate = 10.0

    payload = {
        "asset_name": "Poupança",
        "annual_rate": nova_rate,
    }

    response = requests.put(
        f"{base_url}/api/assets",
        json=payload,
        headers=auth_headers,
    )

    assert response.status_code == 200

    response = requests.get(
        f"{base_url}/api/assets"
    )

    assert response.status_code == 200

    assets = response.json()

    assert isinstance(assets, list)

    poupanca_atualizada = None

    for asset in assets:
        if asset["asset_name"] == "Poupança":
            poupanca_atualizada = asset
            break

    assert poupanca_atualizada is not None
    assert poupanca_atualizada["annual_rate"] == nova_rate

    payload = {
        "asset_name": "Poupança",
        "annual_rate": rate_original,
    }

    response = requests.put(
        f"{base_url}/api/assets",
        json=payload,
        headers=auth_headers,
    )

    assert response.status_code == 200

    payload = {
        "asset_name": "Poupança",
        "amount": 1000.00,
        "purchase_price": 1.00,
        "days_invested": 30,
        "planned_days": 365,
    }

    response = requests.post(
        f"{base_url}/api/investments",
        json=payload,
        headers=auth_headers,
    )

    assert response.status_code == 201

    investment = response.json()

    assert isinstance(investment, dict)
    assert "id" in investment

    investment_id = investment["id"]

    assert investment_id is not None
    assert isinstance(investment_id, int)
    assert investment_id > 0

    response = requests.get(
        f"{base_url}/api/investments",
        headers=auth_headers,
    )

    assert response.status_code == 200

    investments = response.json()

    assert isinstance(investments, list)

    created_investment = None

    for item in investments:
        if item["id"] == investment_id:
            created_investment = item
            break

    assert created_investment is not None
    assert created_investment["id"] == investment_id
    assert created_investment["asset_name"] == "Poupança"
    assert created_investment["amount"] == 1000.00

    response = requests.delete(
        f"{base_url}/api/investments/{investment_id}",
        headers=auth_headers,
    )

    assert response.status_code in (200, 204)

    response = requests.get(
        f"{base_url}/api/investments",
        headers=auth_headers,
    )

    assert response.status_code == 200

    investments = response.json()

    assert isinstance(investments, list)

    ids = [item["id"] for item in investments]

    assert investment_id not in ids


def test_criar_investimento_valor_negativo(base_url, auth_headers):
    payload = {
        "asset_name": "CDB",
        "amount": -100.00,
        "purchase_price": 1.00,
        "days_invested": 30,
        "planned_days": 365,
    }

    response = requests.post(
        f"{base_url}/api/investments",
        json=payload,
        headers=auth_headers,
    )

    assert response.status_code == 400
