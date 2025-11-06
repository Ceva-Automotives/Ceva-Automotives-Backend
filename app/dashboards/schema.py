from typing import Union
from pydantic import BaseModel
from datetime import datetime

class DashboardBase(BaseModel):
    '''Classe para definir os modelos recebidos na API'''
    nome: str
    adminId: int

class DashboardRequest(DashboardBase):
    '''Classe para requisições de criação e atualização de dashboards'''
    pass

class DashboardResponse(DashboardBase):
    '''Classe para respostas da API'''
    id: int
    criadoEm: datetime
    atualizadoEm: datetime
    
    class Config:
        from_attributes = True

class DashboardUpdateRequest(BaseModel):
    '''Classe para atualização de dashboards'''
    nome: Union[str, None] = None

class DashboardCountResponse(BaseModel):
    '''Classe para resposta de contagem de dashboards'''
    count: int
    
    class Config:
        from_attributes = True
