from sqlalchemy.orm import Session
from ..database import get_db as get_database
from fastapi import APIRouter, status, HTTPException, Response, Depends
from ..model.model import Carros
from .repository import CarrosRepository
from .schema import CarrosCountResponse, CarrosRequest, CarrosResponse

router = APIRouter(
    prefix = '/carros',
    tags = ['carros'],
    responses = {404: {"description": "Not found"}},
)

# CREATE
@router.post("/",
    response_model = CarrosResponse,
    status_code = status.HTTP_201_CREATED
)
def create(request: CarrosRequest, database: Session = Depends(get_database)):
    '''Cria e salva um objeto carro por meio do método POST'''
    carros = CarrosRepository.save(database, Carros(**request.dict()))
    return carros

# READ ALL
@router.get("/", response_model = list[CarrosResponse])
def find_all(database: Session = Depends(get_database)):
    '''Faz uma query de todos os objetos carro na DB (sem paginação)'''
    carros = CarrosRepository.find_all(database)
    return [CarrosResponse.from_orm(carro) for carro in carros]

# READ BY ID
@router.get("/{id}", response_model = CarrosResponse)
def find_by_id(id: int, database: Session = Depends(get_database)):
    '''Dado o ID como parâmetro, encontra o carro com esse ID'''
    carro = CarrosRepository.find_by_id(database, id)
    if not carro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail = "Carro não encontrado"
        )
    return CarrosResponse.from_orm(carro)

# UPDATE BY ID
@router.put("/{id}", response_model = CarrosResponse)
def update(id: int, request: CarrosRequest, database: Session = Depends(get_database)):
    '''Dado o ID do carro, atualiza os dados na DB por meio do método PUT'''
    if not CarrosRepository.exists_by_id(database, id):
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, detail = "Carro não encontrado"
        )
    
    # Buscar o carro existente
    carro_existente = CarrosRepository.find_by_id(database, id)
    
    # Atualizar os campos
    for field, value in request.dict().items():
        setattr(carro_existente, field, value)
    
    # Salvar as alterações
    carro_atualizado = CarrosRepository.save(database, carro_existente)
    return CarrosResponse.from_orm(carro_atualizado)

# DELETE BY ID
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, database: Session = Depends(get_database)):
    '''Dado o ID do carro, deleta o objeto da DB por meio do método DELETE'''
    if not CarrosRepository.exists_by_id(database, id):
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, detail="Carro não encontrado"
        )
    CarrosRepository.delete_by_id(database, id)
    return Response(status_code = status.HTTP_204_NO_CONTENT)

# GET COUNT ALL
@router.get("/count/")
def count_all(database: Session = Depends(get_database)):
    '''Faz uma query de contagem de carros na DB (sem paginação)'''
    count = CarrosRepository.count_all(database)
    return {"count":count}

# GET COUNT DISPONIVEL
@router.get("/count/disponivel")
def count_disponivel(database: Session = Depends(get_database)):
    '''Faz uma query de contagem de carros disponíveis na DB (sem paginação)'''
    count_disponivel = CarrosRepository.count_disponivel(database)
    return {"count":count_disponivel}

# GET COUNT DESTAQUE
@router.get("/count/destaque")
def count_destaque(database: Session = Depends(get_database)):
    '''Faz uma query de contagem de carros em destaque na DB (sem paginação)'''
    count_destaque = CarrosRepository.count_destaque(database)
    return {"count":count_destaque}

# GET BY MARCA
@router.get("/marca/{marca}", response_model = list[CarrosResponse])
def find_by_marca(marca: str, database: Session = Depends(get_database)):
    '''Dado a marca como parâmetro, encontra os carros com essa marca'''
    carros = CarrosRepository.find_by_marca(database, marca)
    return [CarrosResponse.from_orm(carro) for carro in carros]

# GET DISPONIVEL
@router.get("/disponivel/", response_model = list[CarrosResponse])
def find_disponivel(database: Session = Depends(get_database)):
    '''Faz uma query de todos os carros disponíveis na DB'''
    carros = CarrosRepository.find_disponivel(database)
    return [CarrosResponse.from_orm(carro) for carro in carros]

# GET DESTAQUE
@router.get("/destaque/", response_model = list[CarrosResponse])
def find_destaque(database: Session = Depends(get_database)):
    '''Faz uma query de todos os carros em destaque na DB'''
    carros = CarrosRepository.find_destaque(database)
    return [CarrosResponse.from_orm(carro) for carro in carros]
