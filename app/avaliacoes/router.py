from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from ..carros.repository import CarrosRepository
from ..clientes.repository import ClientesRepository
from ..database import get_db as get_database
from ..model.model import Avaliacao
from .repository import AvaliacoesRepository
from .schema import (
    AvaliacaoMediaResponse,
    AvaliacaoRequest,
    AvaliacaoResponse,
    AvaliacaoUpdateRequest,
)

router = APIRouter(
    prefix='/avaliacoes',
    tags=['avaliacoes'],
    responses={404: {"description": "Not found"}},
)

# CREATE
@router.post("/",
    response_model=AvaliacaoResponse,
    status_code=status.HTTP_201_CREATED
)
def create(request: AvaliacaoRequest, database: Session = Depends(get_database)):
    '''Cria e salva um objeto avaliação por meio do método POST'''
    # Validar se cliente existe
    if not ClientesRepository.exists_by_id(database, request.clienteId):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    
    # Validar se carro existe
    if not CarrosRepository.exists_by_id(database, request.carroId):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carro não encontrado"
        )
    
    # Validar nota
    if request.nota < 1 or request.nota > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nota deve estar entre 1 e 5"
        )
    
    avaliacao = AvaliacoesRepository.save(database, Avaliacao(**request.dict()))
    return avaliacao

# READ ALL
@router.get("/", response_model=list[AvaliacaoResponse])
def find_all(database: Session = Depends(get_database)):
    '''Faz uma query de todos os objetos avaliação na DB (sem paginação)'''
    avaliacoes = AvaliacoesRepository.find_all(database)
    return [AvaliacaoResponse.from_orm(avaliacao) for avaliacao in avaliacoes]

# READ BY ID
@router.get("/{id}", response_model=AvaliacaoResponse)
def find_by_id(id: int, database: Session = Depends(get_database)):
    '''Dado o ID como parâmetro, encontra a avaliação com esse ID'''
    avaliacao = AvaliacoesRepository.find_by_id(database, id)
    if not avaliacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Avaliação não encontrada"
        )
    return AvaliacaoResponse.from_orm(avaliacao)

# UPDATE BY ID
@router.put("/{id}", response_model=AvaliacaoResponse)
def update(id: int, request: AvaliacaoUpdateRequest, database: Session = Depends(get_database)):
    '''Dado o ID da avaliação, atualiza os dados na DB por meio do método PUT'''
    if not AvaliacoesRepository.exists_by_id(database, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Avaliação não encontrada"
        )
    
    # Buscar a avaliação existente
    avaliacao_existente = AvaliacoesRepository.find_by_id(database, id)
    
    # Atualizar os campos fornecidos
    update_data = request.dict(exclude_unset=True)
    
    # Validar nota se fornecida
    if 'nota' in update_data and update_data['nota']:
        if update_data['nota'] < 1 or update_data['nota'] > 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nota deve estar entre 1 e 5"
            )
    
    for field, value in update_data.items():
        setattr(avaliacao_existente, field, value)
    
    # Salvar as alterações
    avaliacao_atualizada = AvaliacoesRepository.save(database, avaliacao_existente)
    return AvaliacaoResponse.from_orm(avaliacao_atualizada)

# DELETE BY ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, database: Session = Depends(get_database)):
    '''Dado o ID da avaliação, deleta o objeto da DB por meio do método DELETE'''
    if not AvaliacoesRepository.exists_by_id(database, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Avaliação não encontrada"
        )
    AvaliacoesRepository.delete_by_id(database, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# GET COUNT
@router.get("/count/")
def count_all(database: Session = Depends(get_database)):
    '''Faz uma query de contagem de avaliações na DB'''
    count = AvaliacoesRepository.count_all(database)
    return {"count": count}

# GET BY CLIENTE
@router.get("/cliente/{cliente_id}", response_model=list[AvaliacaoResponse])
def find_by_cliente(cliente_id: int, database: Session = Depends(get_database)):
    '''Dado o ID do cliente, encontra as avaliações desse cliente'''
    avaliacoes = AvaliacoesRepository.find_by_cliente(database, cliente_id)
    return [AvaliacaoResponse.from_orm(avaliacao) for avaliacao in avaliacoes]

# GET BY CARRO
@router.get("/carro/{carro_id}", response_model=list[AvaliacaoResponse])
def find_by_carro(carro_id: int, database: Session = Depends(get_database)):
    '''Dado o ID do carro, encontra as avaliações desse carro'''
    avaliacoes = AvaliacoesRepository.find_by_carro(database, carro_id)
    return [AvaliacaoResponse.from_orm(avaliacao) for avaliacao in avaliacoes]

# GET MEDIA BY CARRO
@router.get("/carro/{carro_id}/media", response_model=AvaliacaoMediaResponse)
def calcular_media_carro(carro_id: int, database: Session = Depends(get_database)):
    '''Calcula a média de avaliações de um carro'''
    if not CarrosRepository.exists_by_id(database, carro_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carro não encontrado"
        )
    
    resultado = AvaliacoesRepository.calcular_media_carro(database, carro_id)
    return AvaliacaoMediaResponse(**resultado)

# GET BY NOTA
@router.get("/nota/{nota}", response_model=list[AvaliacaoResponse])
def find_by_nota(nota: int, database: Session = Depends(get_database)):
    '''Dado a nota, encontra as avaliações com essa nota'''
    if nota < 1 or nota > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nota deve estar entre 1 e 5"
        )
    
    avaliacoes = AvaliacoesRepository.find_by_nota(database, nota)
    return [AvaliacaoResponse.from_orm(avaliacao) for avaliacao in avaliacoes]
