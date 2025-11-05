from typing import Union
from pydantic import BaseModel
from datetime import datetime

class MetricaBase(BaseModel):
    '''Classe para definir os modelos recebidos na API'''
    nome: str
    valor: str
    tipo: str
    dashboardId: int

class MetricaRequest(MetricaBase):
    '''Classe para requisições de criação e atualização de métricas'''
    pass

class MetricaResponse(MetricaBase):
    '''Classe para respostas da API'''
    id: int
    criadoEm: datetime
    atualizadoEm: datetime
    
    class Config:
        from_attributes = True

class MetricaUpdateRequest(BaseModel):
    '''Classe para atualização de métricas'''
    nome: Union[str, None] = None
    valor: Union[str, None] = None
    tipo: Union[str, None] = None

class MetricaCountResponse(BaseModel):
    '''Classe para resposta de contagem de métricas'''
    count: int
    
    class Config:
        from_attributes = True
