import requests


def test_listar_ativos_publicos(base_url):
    response = requests.get(f"{base_url}/api/assets")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0