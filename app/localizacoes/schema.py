from typing import Union
from pydantic import BaseModel
from datetime import datetime

class LocalizacaoBase(BaseModel):
    '''Classe para definir os modelos recebidos na API'''
    nome: str
    endereco: str

class LocalizacaoRequest(LocalizacaoBase):
    '''Classe para requisições de criação e atualização de localizações'''
    pass

class LocalizacaoResponse(LocalizacaoBase):
    '''Classe para respostas da API'''
    id: int
    criadoEm: datetime
    atualizadoEm: datetime
    
    class Config:
        from_attributes = True

class LocalizacaoCountResponse(BaseModel):
    '''Classe para resposta de contagem de localizações'''
    count: int
    
    class Config:
        from_attributes = True
