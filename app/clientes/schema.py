from typing import Union, List
from pydantic import BaseModel, EmailStr
from datetime import datetime

class ClienteBase(BaseModel):
    '''Classe para definir os modelos recebidos na API'''
    nome: str
    email: EmailStr
    senha: str
    telefone: Union[str, None] = None
    cnh: str
    cpf: str

class ClienteRequest(ClienteBase):
    '''Classe para requisições de criação e atualização de clientes'''
    pass

class ClienteResponse(BaseModel):
    '''Classe para respostas da API'''
    id: int
    nome: str
    email: str
    telefone: Union[str, None]
    cnh: str
    cpf: str
    dataCadastro: datetime
    criadoEm: datetime
    atualizadoEm: datetime
    
    class Config:
        from_attributes = True

class ClienteLoginRequest(BaseModel):
    '''Classe para requisição de login'''
    email: EmailStr
    senha: str

class ClienteLoginResponse(BaseModel):
    '''Classe para resposta de login'''
    id: int
    nome: str
    email: str
    tipo: str
    message: str

class ClienteUpdateRequest(BaseModel):
    '''Classe para atualização de perfil do cliente'''
    nome: Union[str, None] = None
    telefone: Union[str, None] = None
    senha: Union[str, None] = None
