from sqlalchemy.orm import Session
from ..database import get_db as get_database
from fastapi import APIRouter, status, HTTPException, Response, Depends
from ..model.model import Reserva, StatusReserva
from .repository import ReservasRepository
from .schema import ReservaRequest, ReservaResponse, ReservaUpdateRequest
from ..carros.repository import CarrosRepository
from ..clientes.repository import ClientesRepository
from ..localizacoes.repository import LocalizacoesRepository

router = APIRouter(
    prefix='/reservas',
    tags=['reservas'],
    responses={404: {"description": "Not found"}},
)

# CREATE
@router.post("/",
    response_model=ReservaResponse,
    status_code=status.HTTP_201_CREATED
)
def create(request: ReservaRequest, database: Session = Depends(get_database)):
    '''Cria e salva um objeto reserva por meio do método POST'''
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
    
    # Validar se localizações existem
    if not LocalizacoesRepository.exists_by_id(database, request.localizacaoRetiradaId):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Localização de retirada não encontrada"
        )
    
    if not LocalizacoesRepository.exists_by_id(database, request.localizacaoDevolucaoId):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Localização de devolução não encontrada"
        )
    
    # Validar datas
    if request.dataDevolucao <= request.dataRetirada:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data de devolução deve ser posterior à data de retirada"
        )
    
    # Calcular valor total
    valor_total = ReservasRepository.calcular_valor_total(
        database,
        request.carroId,
        request.dataRetirada,
        request.dataDevolucao
    )
    
    # Criar reserva
    reserva_data = request.dict()
    reserva_data['valorTotal'] = valor_total
    reserva_data['status'] = StatusReserva.PENDENTE
    
    reserva = ReservasRepository.save(database, Reserva(**reserva_data))
    return reserva

# READ ALL
@router.get("/", response_model=list[ReservaResponse])
def find_all(database: Session = Depends(get_database)):
    '''Faz uma query de todos os objetos reserva na DB (sem paginação)'''
    reservas = ReservasRepository.find_all(database)
    return [ReservaResponse.from_orm(reserva) for reserva in reservas]

# READ BY ID
@router.get("/{id}", response_model=ReservaResponse)
def find_by_id(id: int, database: Session = Depends(get_database)):
    '''Dado o ID como parâmetro, encontra a reserva com esse ID'''
    reserva = ReservasRepository.find_by_id(database, id)
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reserva não encontrada"
        )
    return ReservaResponse.from_orm(reserva)

# UPDATE BY ID
@router.put("/{id}", response_model=ReservaResponse)
def update(id: int, request: ReservaUpdateRequest, database: Session = Depends(get_database)):
    '''Dado o ID da reserva, atualiza os dados na DB por meio do método PUT'''
    if not ReservasRepository.exists_by_id(database, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reserva não encontrada"
        )
    
    # Buscar a reserva existente
    reserva_existente = ReservasRepository.find_by_id(database, id)
    
    # Atualizar os campos fornecidos
    update_data = request.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(reserva_existente, field, value)
    
    # Salvar as alterações
    reserva_atualizada = ReservasRepository.save(database, reserva_existente)
    return ReservaResponse.from_orm(reserva_atualizada)

# DELETE BY ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, database: Session = Depends(get_database)):
    '''Dado o ID da reserva, deleta o objeto da DB por meio do método DELETE'''
    if not ReservasRepository.exists_by_id(database, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reserva não encontrada"
        )
    ReservasRepository.delete_by_id(database, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# GET COUNT
@router.get("/count/")
def count_all(database: Session = Depends(get_database)):
    '''Faz uma query de contagem de reservas na DB'''
    count = ReservasRepository.count_all(database)
    return {"count": count}

# GET BY CLIENTE
@router.get("/cliente/{cliente_id}", response_model=list[ReservaResponse])
def find_by_cliente(cliente_id: int, database: Session = Depends(get_database)):
    '''Dado o ID do cliente, encontra as reservas desse cliente'''
    reservas = ReservasRepository.find_by_cliente(database, cliente_id)
    return [ReservaResponse.from_orm(reserva) for reserva in reservas]

# GET BY CARRO
@router.get("/carro/{carro_id}", response_model=list[ReservaResponse])
def find_by_carro(carro_id: int, database: Session = Depends(get_database)):
    '''Dado o ID do carro, encontra as reservas desse carro'''
    reservas = ReservasRepository.find_by_carro(database, carro_id)
    return [ReservaResponse.from_orm(reserva) for reserva in reservas]

# GET BY STATUS
@router.get("/status/{status}", response_model=list[ReservaResponse])
def find_by_status(status: str, database: Session = Depends(get_database)):
    '''Dado o status, encontra as reservas com esse status'''
    reservas = ReservasRepository.find_by_status(database, status)
    return [ReservaResponse.from_orm(reserva) for reserva in reservas]

# GET COUNT BY STATUS
@router.get("/count/status/{status}")
def count_by_status(status: str, database: Session = Depends(get_database)):
    '''Faz uma query de contagem de reservas por status na DB'''
    count = ReservasRepository.count_by_status(database, status)
    return {"count": count}

# CONFIRMAR RESERVA
@router.patch("/{id}/confirmar", response_model=ReservaResponse)
def confirmar_reserva(id: int, database: Session = Depends(get_database)):
    '''Confirma uma reserva pendente'''
    reserva = ReservasRepository.find_by_id(database, id)
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reserva não encontrada"
        )
    
    if reserva.status != StatusReserva.PENDENTE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Apenas reservas pendentes podem ser confirmadas"
        )
    
    reserva.status = StatusReserva.CONFIRMADA
    reserva_atualizada = ReservasRepository.save(database, reserva)
    return ReservaResponse.from_orm(reserva_atualizada)

# CANCELAR RESERVA
@router.patch("/{id}/cancelar", response_model=ReservaResponse)
def cancelar_reserva(id: int, database: Session = Depends(get_database)):
    '''Cancela uma reserva'''
    reserva = ReservasRepository.find_by_id(database, id)
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reserva não encontrada"
        )
    
    if reserva.status == StatusReserva.CONCLUIDA:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reservas concluídas não podem ser canceladas"
        )
    
    reserva.status = StatusReserva.CANCELADA
    reserva_atualizada = ReservasRepository.save(database, reserva)
    return ReservaResponse.from_orm(reserva_atualizada)

# CONCLUIR RESERVA
@router.patch("/{id}/concluir", response_model=ReservaResponse)
def concluir_reserva(id: int, database: Session = Depends(get_database)):
    '''Conclui uma reserva confirmada'''
    reserva = ReservasRepository.find_by_id(database, id)
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reserva não encontrada"
        )
    
    if reserva.status != StatusReserva.CONFIRMADA:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Apenas reservas confirmadas podem ser concluídas"
        )
    
    reserva.status = StatusReserva.CONCLUIDA
    reserva_atualizada = ReservasRepository.save(database, reserva)
    return ReservaResponse.from_orm(reserva_atualizada)
