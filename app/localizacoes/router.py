from sqlalchemy.orm import Session
from ..database import get_db as get_database
from fastapi import APIRouter, status, HTTPException, Response, Depends
from ..model.model import Localizacao
from .repository import LocalizacoesRepository
from .schema import LocalizacaoRequest, LocalizacaoResponse

router = APIRouter(
    prefix='/localizacoes',
    tags=['localizacoes'],
    responses={404: {"description": "Not found"}},
)

# CREATE
@router.post("/",
    response_model=LocalizacaoResponse,
    status_code=status.HTTP_201_CREATED
)
def create(request: LocalizacaoRequest, database: Session = Depends(get_database)):
    '''Cria e salva um objeto localização por meio do método POST'''
    localizacao = LocalizacoesRepository.save(database, Localizacao(**request.dict()))
    return localizacao

# READ ALL
@router.get("/", response_model=list[LocalizacaoResponse])
def find_all(database: Session = Depends(get_database)):
    '''Faz uma query de todos os objetos localização na DB (sem paginação)'''
    localizacoes = LocalizacoesRepository.find_all(database)
    return [LocalizacaoResponse.from_orm(localizacao) for localizacao in localizacoes]

# READ BY ID
@router.get("/{id}", response_model=LocalizacaoResponse)
def find_by_id(id: int, database: Session = Depends(get_database)):
    '''Dado o ID como parâmetro, encontra a localização com esse ID'''
    localizacao = LocalizacoesRepository.find_by_id(database, id)
    if not localizacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Localização não encontrada"
        )
    return LocalizacaoResponse.from_orm(localizacao)

# UPDATE BY ID
@router.put("/{id}", response_model=LocalizacaoResponse)
def update(id: int, request: LocalizacaoRequest, database: Session = Depends(get_database)):
    '''Dado o ID da localização, atualiza os dados na DB por meio do método PUT'''
    if not LocalizacoesRepository.exists_by_id(database, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Localização não encontrada"
        )
    
    # Buscar a localização existente
    localizacao_existente = LocalizacoesRepository.find_by_id(database, id)
    
    # Atualizar os campos
    for field, value in request.dict().items():
        setattr(localizacao_existente, field, value)
    
    # Salvar as alterações
    localizacao_atualizada = LocalizacoesRepository.save(database, localizacao_existente)
    return LocalizacaoResponse.from_orm(localizacao_atualizada)

# DELETE BY ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, database: Session = Depends(get_database)):
    '''Dado o ID da localização, deleta o objeto da DB por meio do método DELETE'''
    if not LocalizacoesRepository.exists_by_id(database, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Localização não encontrada"
        )
    LocalizacoesRepository.delete_by_id(database, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# GET COUNT
@router.get("/count/")
def count_all(database: Session = Depends(get_database)):
    '''Faz uma query de contagem de localizações na DB'''
    count = LocalizacoesRepository.count_all(database)
    return {"count": count}

# GET BY NOME
@router.get("/nome/{nome}", response_model=list[LocalizacaoResponse])
def find_by_nome(nome: str, database: Session = Depends(get_database)):
    '''Dado o nome como parâmetro, encontra as localizações com esse nome'''
    localizacoes = LocalizacoesRepository.find_by_nome(database, nome)
    return [LocalizacaoResponse.from_orm(localizacao) for localizacao in localizacoes]
