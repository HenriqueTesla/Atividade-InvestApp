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
