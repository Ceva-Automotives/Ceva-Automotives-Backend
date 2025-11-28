from datetime import datetime

from pydantic import BaseModel


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
    dataRetirada: datetime | None = None
    dataDevolucao: datetime | None = None
    status: str | None = None
    localizacaoRetiradaId: int | None = None
    localizacaoDevolucaoId: int | None = None

class ReservaCountResponse(BaseModel):
    '''Classe para resposta de contagem de reservas'''
    count: int
    
    class Config:
        from_attributes = True
