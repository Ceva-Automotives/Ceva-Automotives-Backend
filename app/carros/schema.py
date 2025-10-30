from typing import Union
from pydantic import BaseModel
from datetime import datetime

class CarrosBase(BaseModel):
    '''Classe para definir os modelos recebidos na API'''
    placa: str
    marca: str
    modelo: str
    ano: int
    cor: str
    precoDia: float
    categoria: str
    status: str = "Disponivel"
    descricao: Union[str, None] = None
    disponivel: bool = True
    destaque: bool = False
    localizacaoId: Union[int, None] = None

class CarrosRequest(CarrosBase):
    '''Classe para requisições de criação e atualização de carros'''
    pass

class CarrosResponse(CarrosBase):
    '''Classe para respostas da API'''
    id: int
    criadoEm: datetime
    atualizadoEm: datetime
    
    class Config:
        from_attributes = True

class CarrosUpdateRequest(BaseModel):
    '''Classe para atualização de carros'''
    placa: Union[str, None] = None
    marca: Union[str, None] = None
    modelo: Union[str, None] = None
    ano: Union[int, None] = None
    cor: Union[str, None] = None
    precoDia: Union[float, None] = None
    categoria: Union[str, None] = None
    status: Union[str, None] = None
    descricao: Union[str, None] = None
    disponivel: Union[bool, None] = None
    destaque: Union[bool, None] = None
    localizacaoId: Union[int, None] = None

class CarrosCountResponse(BaseModel):
    '''Classe para resposta de contagem de carros'''
    count: int
    
    class Config:
        from_attributes = True
