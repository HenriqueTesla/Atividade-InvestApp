import requests


def test_simulacao_rendimento_mensal(base_url, auth_headers):
    payload = {
        "months": 12
    }

    response = requests.post(
        f"{base_url}/api/simulate/yield-monthly",
        json=payload,
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)


def test_simulacao_resgate_otimizacao_fiscal(base_url, auth_headers):
    payload = {
        "target_amount": 1000
    }

    response = requests.post(
        f"{base_url}/api/simulate/tax-withdrawal",
        json=payload,
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    for item in data:
        assert isinstance(item, dict)
        assert "asset_name" in item
        assert "asset_type" in item
        assert "current_val" in item
        assert "tax_due" in item
        assert "effective_tax_rate" in item
        assert "net_amount" in item
        assert "is_exempt" in item
