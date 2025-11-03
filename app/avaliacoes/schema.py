from typing import Union
from pydantic import BaseModel, Field
from datetime import datetime

class AvaliacaoBase(BaseModel):
    '''Classe para definir os modelos recebidos na API'''
    nota: int = Field(..., ge=1, le=5, description="Nota de 1 a 5")
    comentario: Union[str, None] = None
    clienteId: int
    carroId: int

class AvaliacaoRequest(AvaliacaoBase):
    '''Classe para requisições de criação de avaliações'''
    pass

class AvaliacaoResponse(AvaliacaoBase):
    '''Classe para respostas da API'''
    id: int
    data: datetime
    criadoEm: datetime
    atualizadoEm: datetime
    
    class Config:
        from_attributes = True

class AvaliacaoUpdateRequest(BaseModel):
    '''Classe para atualização de avaliações'''
    nota: Union[int, None] = Field(None, ge=1, le=5, description="Nota de 1 a 5")
    comentario: Union[str, None] = None

class AvaliacaoCountResponse(BaseModel):
    '''Classe para resposta de contagem de avaliações'''
    count: int
    
    class Config:
        from_attributes = True

class AvaliacaoMediaResponse(BaseModel):
    '''Classe para resposta de média de avaliações'''
    media: float
    total: int
    
    class Config:
        from_attributes = True
