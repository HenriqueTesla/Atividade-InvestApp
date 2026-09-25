import csv
from pathlib import Path
import pytest
import requests


def carregar_dados_investimentos_csv():
    caminho_csv = (
        Path(__file__).resolve().parent
        / "data"
        / "dados_investimentos.csv"
    )

    if not caminho_csv.exists():
        raise FileNotFoundError(
            f"Arquivo de massa CSV não encontrado em: {caminho_csv}"
        )

    casos = []

    with open(caminho_csv, mode="r", encoding="utf-8") as f:
        leitor = csv.DictReader(f)

        for linha in leitor:
            casos.append(
                (
                    linha["asset_name"],
                    float(linha["amount"]),
                    float(linha["purchase_price"]),
                    int(linha["days_invested"]),
                    int(linha["planned_days"]),
                    int(linha["status_esperado"]),
                )
            )

    return casos


def test_criar_investimento_valido(base_url, auth_headers):
    payload = {
        "asset_name": "CDB",
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

    data = response.json()

    assert isinstance(data, dict)
    assert data["asset_name"] == payload["asset_name"]
    assert data["amount"] == payload["amount"]
    assert data["purchase_price"] == payload["purchase_price"]
    assert data["days_invested"] == payload["days_invested"]
    assert data["planned_days"] == payload["planned_days"]


@pytest.mark.parametrize(
    "asset, amount, price, days, planned, status_esperado",
    carregar_dados_investimentos_csv(),
)
def test_criar_investimentos_ddt_csv(
    base_url,
    auth_headers,
    asset,
    amount,
    price,
    days,
    planned,
    status_esperado,
):
    payload = {
        "asset_name": asset,
        "amount": amount,
        "purchase_price": price,
        "days_invested": days,
        "planned_days": planned,
    }

    response = requests.post(
        f"{base_url}/api/investments",
        json=payload,
        headers=auth_headers,
    )

    assert response.status_code == status_esperado


def test_listar_investimentos(base_url, auth_headers):
    response = requests.get(
        f"{base_url}/api/investments",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_excluir_investimento(base_url, auth_headers):
    payload = {
        "asset_name": "CDB",
        "amount": 1000.00,
        "purchase_price": 1.00,
        "days_invested": 30,
        "planned_days": 365,
    }

    criar = requests.post(
        f"{base_url}/api/investments",
        json=payload,
        headers=auth_headers,
    )

    assert criar.status_code == 201

    investimento = criar.json()

    assert "id" in investimento

    investment_id = investimento["id"]

    response = requests.delete(
        f"{base_url}/api/investments/{investment_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200
