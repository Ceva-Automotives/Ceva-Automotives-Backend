import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..database import Base, get_db
from ..main import app
from ..model.model import Carros

# Configuração do banco de dados de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_carro():
    response = client.post(
        "/carros/",
        json={
            "marca": "Toyota",
            "modelo": "Corolla",
            "ano": 2023,
            "cor": "Branco",
            "precoDia": 150.0,
            "precoSemana": 900.0,
            "precoMes": 3500.0,
            "descricao": "Carro econômico e confiável",
            "disponivel": True,
            "destaque": False
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["marca"] == "Toyota"
    assert data["modelo"] == "Corolla"
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
            "marca": "Honda",
            "modelo": "Civic",
            "ano": 2022,
            "cor": "Preto",
            "precoDia": 180.0,
            "precoSemana": 1100.0,
            "precoMes": 4200.0,
            "descricao": "Carro esportivo",
            "disponivel": True,
            "destaque": True
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
            "marca": "Ford",
            "modelo": "Focus",
            "ano": 2021,
            "cor": "Azul",
            "precoDia": 140.0,
            "precoSemana": 850.0,
            "precoMes": 3200.0,
            "descricao": "Carro compacto",
            "disponivel": True,
            "destaque": False
        },
    )
    carro_id = response.json()["id"]
    
    # Atualizar o carro
    response = client.put(
        f"/carros/{carro_id}",
        json={
            "marca": "Ford",
            "modelo": "Focus",
            "ano": 2021,
            "cor": "Vermelho",
            "precoDia": 160.0,
            "precoSemana": 950.0,
            "precoMes": 3600.0,
            "descricao": "Carro compacto atualizado",
            "disponivel": True,
            "destaque": True
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["cor"] == "Vermelho"
    assert data["destaque"] == True

def test_delete_carro():
    # Primeiro criar um carro
    response = client.post(
        "/carros/",
        json={
            "marca": "Chevrolet",
            "modelo": "Onix",
            "ano": 2023,
            "cor": "Prata",
            "precoDia": 120.0,
            "precoSemana": 720.0,
            "precoMes": 2800.0,
            "descricao": "Carro popular",
            "disponivel": True,
            "destaque": False
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
