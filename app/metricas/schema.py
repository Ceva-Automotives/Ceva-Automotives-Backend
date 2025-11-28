from datetime import datetime

from pydantic import BaseModel


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
    nome: str | None = None
    valor: str | None = None
    tipo: str | None = None

class MetricaCountResponse(BaseModel):
    '''Classe para resposta de contagem de métricas'''
    count: int
    
    class Config:
        from_attributes = True
