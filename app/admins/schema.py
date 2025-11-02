from typing import Union
from pydantic import BaseModel, EmailStr
from datetime import datetime

class AdminBase(BaseModel):
    '''Classe para definir os modelos recebidos na API'''
    nome: str
    email: EmailStr
    senha: str
    telefone: Union[str, None] = None
    cargo: str

class AdminRequest(AdminBase):
    '''Classe para requisições de criação e atualização de admins'''
    pass

class AdminResponse(BaseModel):
    '''Classe para respostas da API'''
    id: int
    nome: str
    email: str
    telefone: Union[str, None]
    cargo: str
    dataCadastro: datetime
    criadoEm: datetime
    atualizadoEm: datetime
    
    class Config:
        from_attributes = True

class AdminLoginRequest(BaseModel):
    '''Classe para requisição de login'''
    email: EmailStr
    senha: str

class AdminLoginResponse(BaseModel):
    '''Classe para resposta de login'''
    id: int
    nome: str
    email: str
    tipo: str
    cargo: str
    message: str

class AdminUpdateRequest(BaseModel):
    '''Classe para atualização de perfil do admin'''
    nome: Union[str, None] = None
    telefone: Union[str, None] = None
    cargo: Union[str, None] = None
    senha: Union[str, None] = None
