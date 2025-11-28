import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..database import Base, get_db
from ..main import app

# Configuração do banco de dados de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_carros.db"
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

@pytest.mark.parametrize(
    "payload",
    [
        {
            "placa": "AAA1A11",
            "marca": "Toyota",
            "modelo": "Corolla",
            "ano": 2023,
            "cor": "Branco",
            "precoDia": 150.0,
            "categoria": "Sedan",
            "descricao": "Carro econômico e confiável",
            "disponivel": True,
            "destaque": False,
        },
        {
            "placa": "BBB2B22",
            "marca": "Honda",
            "modelo": "Civic",
            "ano": 2022,
            "cor": "Preto",
            "precoDia": 180.0,
            "categoria": "Sedan",
            "descricao": "Carro esportivo",
            "disponivel": True,
            "destaque": True,
        },
    ],
)
def test_create_carro(payload):
    response = client.post(
        "/carros/",
        json=payload,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["marca"] == payload["marca"]
    assert data["modelo"] == payload["modelo"]
    assert "id" in data

def test_read_carros():
    response = client.get("/carros/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_carro_by_id():
    # Primeiro criar um carro
    response = client.post(
        "/carros/",
        json={
            "placa": "IJK7L89",
            "marca": "Honda",
            "modelo": "Civic",
            "ano": 2022,
            "cor": "Preto",
            "precoDia": 180.0,
            "categoria": "Sedan",
            "descricao": "Carro esportivo",
            "disponivel": True,
            "destaque": True,
        },
    )
    carro_id = response.json()["id"]
    
    # Buscar o carro criado
    response = client.get(f"/carros/{carro_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["marca"] == "Honda"
    assert data["modelo"] == "Civic"

def test_update_carro():
    # Primeiro criar um carro
    response = client.post(
        "/carros/",
        json={
            "placa": "MNO1P23",
            "marca": "Ford",
            "modelo": "Focus",
            "ano": 2021,
            "cor": "Azul",
            "precoDia": 140.0,
            "categoria": "Hatch",
            "descricao": "Carro compacto",
            "disponivel": True,
            "destaque": False,
        },
    )
    carro_id = response.json()["id"]
    
    # Atualizar o carro
    response = client.put(
        f"/carros/{carro_id}",
        json={
            "cor": "Vermelho",
            "precoDia": 160.0,
            "descricao": "Carro compacto atualizado",
            "destaque": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["cor"] == "Vermelho"
    assert data["destaque"] is True

def test_delete_carro():
    # Primeiro criar um carro
    response = client.post(
        "/carros/",
        json={
            "placa": "QRS4T56",
            "marca": "Chevrolet",
            "modelo": "Onix",
            "ano": 2023,
            "cor": "Prata",
            "precoDia": 120.0,
            "categoria": "Hatch",
            "descricao": "Carro popular",
            "disponivel": True,
            "destaque": False,
        },
    )
    carro_id = response.json()["id"]
    
    # Deletar o carro
    response = client.delete(f"/carros/{carro_id}")
    assert response.status_code == 204
    
    # Verificar se foi deletado
    response = client.get(f"/carros/{carro_id}")
    assert response.status_code == 404

def test_count_carros():
    response = client.get("/carros/count/")
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert isinstance(data["count"], int)
