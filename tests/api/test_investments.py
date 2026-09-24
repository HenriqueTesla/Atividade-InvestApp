import csv
from pathlib import Path
import pytest
import requests


def carregar_dados_investimentos_csv():
    caminho_csv = Path(__file__).resolve().parent.parent / "data" / "dados_investimentos.csv"

    if not caminho_csv.exists():
        raise FileNotFoundError(f"Arquivo de massa CSV não encontrado em: {caminho_csv}")

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


@pytest.mark.parametrize(
    "asset, amount, price, days, planned, status_esperado",
    carregar_dados_investimentos_csv()
)
def test_criar_investimentos_ddt_csv(
    base_url, auth_headers, asset, amount, price, days, planned, status_esperado
):
    payload = {
        "asset_name": asset,
        "amount": amount,
        "purchase_price": price,
        "days_invested": days,
        "planned_days": planned,
    }
    response = requests.post(f"{base_url}/api/investments", json=payload, headers=auth_headers)
    assert response.status_code == status_esperado