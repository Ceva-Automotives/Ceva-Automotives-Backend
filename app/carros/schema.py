from typing import Union
from pydantic import BaseModel
from datetime import datetime

class CarrosBase(BaseModel):
    '''Classe para definir os modelos recebidos na API'''
    marca: str
    modelo: str
    ano: int
    cor: str
    precoDia: float
    precoSemana: Union[float, None] = None
    precoMes: Union[float, None] = None
    descricao: Union[str, None] = None
    disponivel: bool = True
    destaque: bool = False

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

class CarrosCountResponse(BaseModel):
    '''Classe para resposta de contagem de carros'''
    count: int
    
    class Config:
        from_attributes = True
