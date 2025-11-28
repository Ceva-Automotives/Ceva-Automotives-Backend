from datetime import datetime

from pydantic import BaseModel


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
    descricao: str | None = None
    disponivel: bool = True
    destaque: bool = False
    localizacaoId: int | None = None

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
    placa: str | None = None
    marca: str | None = None
    modelo: str | None = None
    ano: int | None = None
    cor: str | None = None
    precoDia: float | None = None
    categoria: str | None = None
    status: str | None = None
    descricao: str | None = None
    disponivel: bool | None = None
    destaque: bool | None = None
    localizacaoId: int | None = None

class CarrosCountResponse(BaseModel):
    '''Classe para resposta de contagem de carros'''
    count: int
    
    class Config:
        from_attributes = True
