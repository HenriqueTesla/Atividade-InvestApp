import importlib.util
from pathlib import Path


def carregar_conftest():
    caminho = Path(__file__).parent / "conftest.py"

    spec = importlib.util.spec_from_file_location(
        "conftest_test",
        caminho,
    )

    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)

    return modulo


def test_verificar_variaveis_ambiente_sem_credenciais(
    monkeypatch,
    capsys,
):
    conftest = carregar_conftest()

    monkeypatch.setattr(conftest, "TEST_USER", None)
    monkeypatch.setattr(conftest, "TEST_PASSWORD", None)

    conftest.verificar_variaveis_ambiente()

    captured = capsys.readouterr()

    assert (
        "[AVISO] Algumas variáveis de ambiente não foram configuradas."
        in captured.out
    )

    assert (
        "Os testes continuarão, mas chamadas autenticadas podem falhar."
        in captured.out
    )
