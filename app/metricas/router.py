from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from ..dashboards.repository import DashboardsRepository
from ..database import get_db as get_database
from ..model.model import Metrica
from .repository import MetricasRepository
from .schema import MetricaRequest, MetricaResponse, MetricaUpdateRequest

router = APIRouter(
    prefix='/metricas',
    tags=['metricas'],
    responses={404: {"description": "Not found"}},
)

# CREATE
@router.post("/",
    response_model=MetricaResponse,
    status_code=status.HTTP_201_CREATED
)
def create(request: MetricaRequest, database: Session = Depends(get_database)):
    '''Cria e salva um objeto métrica por meio do método POST'''
    # Validar se dashboard existe
    if not DashboardsRepository.exists_by_id(database, request.dashboardId):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard não encontrado"
        )
    
    metrica = MetricasRepository.save(database, Metrica(**request.dict()))
    return metrica

# READ ALL
@router.get("/", response_model=list[MetricaResponse])
def find_all(database: Session = Depends(get_database)):
    '''Faz uma query de todos os objetos métrica na DB (sem paginação)'''
    metricas = MetricasRepository.find_all(database)
    return [MetricaResponse.from_orm(metrica) for metrica in metricas]

# READ BY ID
@router.get("/{id}", response_model=MetricaResponse)
def find_by_id(id: int, database: Session = Depends(get_database)):
    '''Dado o ID como parâmetro, encontra a métrica com esse ID'''
    metrica = MetricasRepository.find_by_id(database, id)
    if not metrica:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Métrica não encontrada"
        )
    return MetricaResponse.from_orm(metrica)

# UPDATE BY ID
@router.put("/{id}", response_model=MetricaResponse)
def update(id: int, request: MetricaUpdateRequest, database: Session = Depends(get_database)):
    '''Dado o ID da métrica, atualiza os dados na DB por meio do método PUT'''
    if not MetricasRepository.exists_by_id(database, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Métrica não encontrada"
        )
    
    # Buscar a métrica existente
    metrica_existente = MetricasRepository.find_by_id(database, id)
    
    # Atualizar os campos fornecidos
    update_data = request.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(metrica_existente, field, value)
    
    # Salvar as alterações
    metrica_atualizada = MetricasRepository.save(database, metrica_existente)
    return MetricaResponse.from_orm(metrica_atualizada)

# DELETE BY ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, database: Session = Depends(get_database)):
    '''Dado o ID da métrica, deleta o objeto da DB por meio do método DELETE'''
    if not MetricasRepository.exists_by_id(database, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Métrica não encontrada"
        )
    MetricasRepository.delete_by_id(database, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# GET COUNT
@router.get("/count/")
def count_all(database: Session = Depends(get_database)):
    '''Faz uma query de contagem de métricas na DB'''
    count = MetricasRepository.count_all(database)
    return {"count": count}

# GET BY DASHBOARD
@router.get("/dashboard/{dashboard_id}", response_model=list[MetricaResponse])
def find_by_dashboard(dashboard_id: int, database: Session = Depends(get_database)):
    '''Dado o ID do dashboard, encontra as métricas desse dashboard'''
    metricas = MetricasRepository.find_by_dashboard(database, dashboard_id)
    return [MetricaResponse.from_orm(metrica) for metrica in metricas]

# GET BY TIPO
@router.get("/tipo/{tipo}", response_model=list[MetricaResponse])
def find_by_tipo(tipo: str, database: Session = Depends(get_database)):
    '''Dado o tipo, encontra as métricas com esse tipo'''
    metricas = MetricasRepository.find_by_tipo(database, tipo)
    return [MetricaResponse.from_orm(metrica) for metrica in metricas]

# GET COUNT BY DASHBOARD
@router.get("/count/dashboard/{dashboard_id}")
def count_by_dashboard(dashboard_id: int, database: Session = Depends(get_database)):
    '''Faz uma query de contagem de métricas por dashboard na DB'''
    count = MetricasRepository.count_by_dashboard(database, dashboard_id)
    return {"count": count}
