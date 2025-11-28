from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..database import Base, get_db
from ..main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_integracao.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def criar_localizacao():
    resp = client.post(
        "/localizacoes/",
        json={"nome": "Agencia Centro", "endereco": "Rua A, 123"},
    )
    assert resp.status_code == 201
    return resp.json()["id"]

def criar_cliente():
    resp = client.post(
        "/clientes/",
        json={
            "nome": "Cliente Teste",
            "email": f"cliente{datetime.now().timestamp()}@teste.com",
            "senha": "senha123",
            "telefone": "61999999999",
            "cnh": f"CNH{int(datetime.now().timestamp())}",
            "cpf": f"{int(datetime.now().timestamp()):011d}",
        },
    )
    assert resp.status_code == 201
    return resp.json()["id"]

def criar_carro(localizacao_id: int):
    resp = client.post(
        "/carros/",
        json={
            "placa": f"{int(datetime.now().timestamp())}ABC",
            "marca": "Toyota",
            "modelo": "Corolla",
            "ano": 2023,
            "cor": "Branco",
            "precoDia": 150.0,
            "categoria": "Sedan",
            "descricao": "Carro econômico",
            "disponivel": True,
            "destaque": False,
            "localizacaoId": localizacao_id,
        },
    )
    assert resp.status_code == 201
    return resp.json()["id"]

def test_fluxo_integrado_reserva():
    loc_retirada = criar_localizacao()
    loc_devolucao = criar_localizacao()
    cliente_id = criar_cliente()
    carro_id = criar_carro(loc_retirada)

    data_retirada = datetime.now()
    data_devolucao = data_retirada + timedelta(days=3)

    resp = client.post(
        "/reservas/",
        json={
            "dataRetirada": data_retirada.isoformat(),
            "dataDevolucao": data_devolucao.isoformat(),
            "clienteId": cliente_id,
            "carroId": carro_id,
            "localizacaoRetiradaId": loc_retirada,
            "localizacaoDevolucaoId": loc_devolucao,
        },
    )
    assert resp.status_code == 201
    reserva = resp.json()
    assert reserva["status"] == "Pendente"
    assert reserva["valorTotal"] == 150.0 * 3

    resp = client.patch(f"/reservas/{reserva['id']}/confirmar")
    assert resp.status_code == 200
    assert resp.json()["status"] == "Confirmada"

    resp = client.patch(f"/reservas/{reserva['id']}/concluir")
    assert resp.status_code == 200
    assert resp.json()["status"] == "Concluida"
