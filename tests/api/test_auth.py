import os
import requests

TEST_USER = os.getenv("TEST_USER")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")


def test_login_sucesso(base_url):
    print(
        f"\n[TEST_AUTH] Testando endpoint /api/login "
        f"para o usuário: '{TEST_USER}'"
    )

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
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_credenciais_invalidas(base_url):
    payload = {
        "username": TEST_USER,
        "password": "senha_invalida_xyz",
    }

    response = requests.post(
        f"{base_url}/api/login",
        json=payload,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Usuário ou senha incorretos"
