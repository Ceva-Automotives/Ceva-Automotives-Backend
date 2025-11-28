from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from ..database import get_db as get_database
from ..model.model import Cliente
from ..security import get_password_hash
from .repository import ClientesRepository
from .schema import (
    ClienteLoginRequest,
    ClienteLoginResponse,
    ClienteRequest,
    ClienteResponse,
    ClienteUpdateRequest,
)

router = APIRouter(
    prefix='/clientes',
    tags=['clientes'],
    responses={404: {"description": "Not found"}},
)

# CREATE
@router.post("/",
    response_model=ClienteResponse,
    status_code=status.HTTP_201_CREATED
)
def create(request: ClienteRequest, database: Session = Depends(get_database)):
    '''Cria e salva um objeto cliente por meio do método POST'''
    # Verificar se email já existe
    if ClientesRepository.find_by_email(database, request.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    # Verificar se CPF já existe
    if ClientesRepository.find_by_cpf(database, request.cpf):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF já cadastrado"
        )
    
    # Verificar se CNH já existe
    if ClientesRepository.find_by_cnh(database, request.cnh):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CNH já cadastrada"
        )
    
    # Criar cliente com senha hasheada
    cliente_data = request.dict()
    cliente_data['senha'] = get_password_hash(cliente_data['senha'])
    cliente_data['tipo'] = 'cliente'
    
    cliente = ClientesRepository.save(database, Cliente(**cliente_data))
    return cliente

# LOGIN
@router.post("/login",
    response_model=ClienteLoginResponse,
    status_code=status.HTTP_200_OK
)
def login(request: ClienteLoginRequest, database: Session = Depends(get_database)):
    '''Autentica um cliente por meio do método POST'''
    cliente = ClientesRepository.authenticate(database, request.email, request.senha)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    return ClienteLoginResponse(
        id=cliente.id,
        nome=cliente.nome,
        email=cliente.email,
        tipo=cliente.tipo,
        message="Login realizado com sucesso"
    )

# READ ALL
@router.get("/", response_model=list[ClienteResponse])
def find_all(database: Session = Depends(get_database)):
    '''Faz uma query de todos os objetos cliente na DB (sem paginação)'''
    clientes = ClientesRepository.find_all(database)
    return [ClienteResponse.from_orm(cliente) for cliente in clientes]

# READ BY ID
@router.get("/{id}", response_model=ClienteResponse)
def find_by_id(id: int, database: Session = Depends(get_database)):
    '''Dado o ID como parâmetro, encontra o cliente com esse ID'''
    cliente = ClientesRepository.find_by_id(database, id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado"
        )
    return ClienteResponse.from_orm(cliente)

# UPDATE BY ID
@router.put("/{id}", response_model=ClienteResponse)
def update(id: int, request: ClienteUpdateRequest, database: Session = Depends(get_database)):
    '''Dado o ID do cliente, atualiza os dados na DB por meio do método PUT'''
    if not ClientesRepository.exists_by_id(database, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado"
        )
    
    # Buscar o cliente existente
    cliente_existente = ClientesRepository.find_by_id(database, id)
    
    # Atualizar os campos fornecidos
    update_data = request.dict(exclude_unset=True)
    if 'senha' in update_data and update_data['senha']:
        update_data['senha'] = get_password_hash(update_data['senha'])
    
    for field, value in update_data.items():
        setattr(cliente_existente, field, value)
    
    # Salvar as alterações
    cliente_atualizado = ClientesRepository.save(database, cliente_existente)
    return ClienteResponse.from_orm(cliente_atualizado)

# DELETE BY ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, database: Session = Depends(get_database)):
    '''Dado o ID do cliente, deleta o objeto da DB por meio do método DELETE'''
    if not ClientesRepository.exists_by_id(database, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado"
        )
    ClientesRepository.delete_by_id(database, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# GET COUNT
@router.get("/count/")
def count_all(database: Session = Depends(get_database)):
    '''Faz uma query de contagem de clientes na DB'''
    count = ClientesRepository.count_all(database)
    return {"count": count}
