from sqlalchemy.orm import Session
from ..database import get_db as get_database
from fastapi import APIRouter, status, HTTPException, Response, Depends
from ..model.model import Dashboard
from .repository import DashboardsRepository
from .schema import DashboardRequest, DashboardResponse, DashboardUpdateRequest
from ..admins.repository import AdminsRepository

router = APIRouter(
    prefix='/dashboards',
    tags=['dashboards'],
    responses={404: {"description": "Not found"}},
)

# CREATE
@router.post("/",
    response_model=DashboardResponse,
    status_code=status.HTTP_201_CREATED
)
def create(request: DashboardRequest, database: Session = Depends(get_database)):
    '''Cria e salva um objeto dashboard por meio do método POST'''
    # Validar se admin existe
    if not AdminsRepository.exists_by_id(database, request.adminId):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin não encontrado"
        )
    
    # Validar se admin já possui dashboard
    if DashboardsRepository.exists_by_admin(database, request.adminId):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin já possui um dashboard"
        )
    
    dashboard = DashboardsRepository.save(database, Dashboard(**request.dict()))
    return dashboard

# READ ALL
@router.get("/", response_model=list[DashboardResponse])
def find_all(database: Session = Depends(get_database)):
    '''Faz uma query de todos os objetos dashboard na DB (sem paginação)'''
    dashboards = DashboardsRepository.find_all(database)
    return [DashboardResponse.from_orm(dashboard) for dashboard in dashboards]

# READ BY ID
@router.get("/{id}", response_model=DashboardResponse)
def find_by_id(id: int, database: Session = Depends(get_database)):
    '''Dado o ID como parâmetro, encontra o dashboard com esse ID'''
    dashboard = DashboardsRepository.find_by_id(database, id)
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Dashboard não encontrado"
        )
    return DashboardResponse.from_orm(dashboard)

# UPDATE BY ID
@router.put("/{id}", response_model=DashboardResponse)
def update(id: int, request: DashboardUpdateRequest, database: Session = Depends(get_database)):
    '''Dado o ID do dashboard, atualiza os dados na DB por meio do método PUT'''
    if not DashboardsRepository.exists_by_id(database, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Dashboard não encontrado"
        )
    
    # Buscar o dashboard existente
    dashboard_existente = DashboardsRepository.find_by_id(database, id)
    
    # Atualizar os campos fornecidos
    update_data = request.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(dashboard_existente, field, value)
    
    # Salvar as alterações
    dashboard_atualizado = DashboardsRepository.save(database, dashboard_existente)
    return DashboardResponse.from_orm(dashboard_atualizado)

# DELETE BY ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, database: Session = Depends(get_database)):
    '''Dado o ID do dashboard, deleta o objeto da DB por meio do método DELETE'''
    if not DashboardsRepository.exists_by_id(database, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Dashboard não encontrado"
        )
    DashboardsRepository.delete_by_id(database, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# GET COUNT
@router.get("/count/")
def count_all(database: Session = Depends(get_database)):
    '''Faz uma query de contagem de dashboards na DB'''
    count = DashboardsRepository.count_all(database)
    return {"count": count}

# GET BY ADMIN
@router.get("/admin/{admin_id}", response_model=DashboardResponse)
def find_by_admin(admin_id: int, database: Session = Depends(get_database)):
    '''Dado o ID do admin, encontra o dashboard desse admin'''
    dashboard = DashboardsRepository.find_by_admin(database, admin_id)
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Dashboard não encontrado para este admin"
        )
    return DashboardResponse.from_orm(dashboard)
