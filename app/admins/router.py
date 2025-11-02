from sqlalchemy.orm import Session
from ..database import get_db as get_database
from fastapi import APIRouter, status, HTTPException, Response, Depends
from ..model.model import Admin
from .repository import AdminsRepository
from .schema import AdminRequest, AdminResponse, AdminLoginRequest, AdminLoginResponse, AdminUpdateRequest
from ..security import get_password_hash

router = APIRouter(
    prefix='/admins',
    tags=['admins'],
    responses={404: {"description": "Not found"}},
)

# CREATE
@router.post("/",
    response_model=AdminResponse,
    status_code=status.HTTP_201_CREATED
)
def create(request: AdminRequest, database: Session = Depends(get_database)):
    '''Cria e salva um objeto admin por meio do método POST'''
    # Verificar se email já existe
    if AdminsRepository.find_by_email(database, request.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    # Criar admin com senha hasheada
    admin_data = request.dict()
    admin_data['senha'] = get_password_hash(admin_data['senha'])
    admin_data['tipo'] = 'admin'
    
    admin = AdminsRepository.save(database, Admin(**admin_data))
    return admin

# LOGIN
@router.post("/login",
    response_model=AdminLoginResponse,
    status_code=status.HTTP_200_OK
)
def login(request: AdminLoginRequest, database: Session = Depends(get_database)):
    '''Autentica um admin por meio do método POST'''
    admin = AdminsRepository.authenticate(database, request.email, request.senha)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    return AdminLoginResponse(
        id=admin.id,
        nome=admin.nome,
        email=admin.email,
        tipo=admin.tipo,
        cargo=admin.cargo,
        message="Login realizado com sucesso"
    )

# READ ALL
@router.get("/", response_model=list[AdminResponse])
def find_all(database: Session = Depends(get_database)):
    '''Faz uma query de todos os objetos admin na DB (sem paginação)'''
    admins = AdminsRepository.find_all(database)
    return [AdminResponse.from_orm(admin) for admin in admins]

# READ BY ID
@router.get("/{id}", response_model=AdminResponse)
def find_by_id(id: int, database: Session = Depends(get_database)):
    '''Dado o ID como parâmetro, encontra o admin com esse ID'''
    admin = AdminsRepository.find_by_id(database, id)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Admin não encontrado"
        )
    return AdminResponse.from_orm(admin)

# UPDATE BY ID
@router.put("/{id}", response_model=AdminResponse)
def update(id: int, request: AdminUpdateRequest, database: Session = Depends(get_database)):
    '''Dado o ID do admin, atualiza os dados na DB por meio do método PUT'''
    if not AdminsRepository.exists_by_id(database, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Admin não encontrado"
        )
    
    # Buscar o admin existente
    admin_existente = AdminsRepository.find_by_id(database, id)
    
    # Atualizar os campos fornecidos
    update_data = request.dict(exclude_unset=True)
    if 'senha' in update_data and update_data['senha']:
        update_data['senha'] = get_password_hash(update_data['senha'])
    
    for field, value in update_data.items():
        setattr(admin_existente, field, value)
    
    # Salvar as alterações
    admin_atualizado = AdminsRepository.save(database, admin_existente)
    return AdminResponse.from_orm(admin_atualizado)

# DELETE BY ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, database: Session = Depends(get_database)):
    '''Dado o ID do admin, deleta o objeto da DB por meio do método DELETE'''
    if not AdminsRepository.exists_by_id(database, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Admin não encontrado"
        )
    AdminsRepository.delete_by_id(database, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# GET COUNT
@router.get("/count/")
def count_all(database: Session = Depends(get_database)):
    '''Faz uma query de contagem de admins na DB'''
    count = AdminsRepository.count_all(database)
    return {"count": count}

# GET BY CARGO
@router.get("/cargo/{cargo}", response_model=list[AdminResponse])
def find_by_cargo(cargo: str, database: Session = Depends(get_database)):
    '''Dado o cargo como parâmetro, encontra os admins com esse cargo'''
    admins = AdminsRepository.find_by_cargo(database, cargo)
    return [AdminResponse.from_orm(admin) for admin in admins]
