from typing import Union
from pydantic import BaseModel
from datetime import datetime

class ReservaBase(BaseModel):
    '''Classe para definir os modelos recebidos na API'''
    dataRetirada: datetime
    dataDevolucao: datetime
    valorTotal: float
    status: str
    clienteId: int
    carroId: int
    localizacaoRetiradaId: int
    localizacaoDevolucaoId: int

class ReservaRequest(BaseModel):
    '''Classe para requisições de criação de reservas'''
    dataRetirada: datetime
    dataDevolucao: datetime
    clienteId: int
    carroId: int
    localizacaoRetiradaId: int
    localizacaoDevolucaoId: int

class ReservaResponse(ReservaBase):
    '''Classe para respostas da API'''
    id: int
    criadoEm: datetime
    atualizadoEm: datetime
    
    class Config:
        from_attributes = True

class ReservaUpdateRequest(BaseModel):
    '''Classe para atualização de reservas'''
    dataRetirada: Union[datetime, None] = None
    dataDevolucao: Union[datetime, None] = None
    status: Union[str, None] = None
    localizacaoRetiradaId: Union[int, None] = None
    localizacaoDevolucaoId: Union[int, None] = None

class ReservaCountResponse(BaseModel):
    '''Classe para resposta de contagem de reservas'''
    count: int
    
    class Config:
        from_attributes = True
