import requests


def test_listar_ativos_publicos(base_url):
    response = requests.get(f"{base_url}/api/assets")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_atualizar_taxa_ativo(base_url, auth_headers):
    response = requests.get(f"{base_url}/api/assets")

    assert response.status_code == 200

    assets = response.json()

    assert isinstance(assets, list)
    assert len(assets) > 0

    asset = assets[0]

    asset_name = asset["asset_name"]
    taxa_original = asset["annual_rate"]

    nova_taxa = taxa_original + 1.0

    response = requests.put(
        f"{base_url}/api/assets",
        json={
            "asset_name": asset_name,
            "annual_rate": nova_taxa
        },
        headers=auth_headers
    )

    assert response.status_code == 200

    response = requests.put(
        f"{base_url}/api/assets",
        json={
            "asset_name": asset_name,
            "annual_rate": taxa_original
        },
        headers=auth_headers
    )

    assert response.status_code == 200
