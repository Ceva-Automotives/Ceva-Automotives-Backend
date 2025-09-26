'''Importando parâmetros da orm'''

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database import Base

class Carros(Base):
    '''Classe para estabelecer o modelo da tabela na DB'''
    __tablename__ = "carros"

    id: int = Column(Integer, primary_key = True, index = True)
    marca: str = Column(String(100), nullable = False)
    modelo: str = Column(String(100), nullable = False)
    ano: int = Column(Integer, nullable = False)
    cor: str = Column(String(50), nullable = False)
    precoDia: float = Column(Float, nullable = False)
    descricao: str = Column(String(500), nullable = True)
    disponivel: bool = Column(Boolean, nullable = False, default = True)
    destaque: bool = Column(Boolean, nullable = False, default = False)
    criadoEm: DateTime = Column(DateTime, nullable = False, default = datetime.now)
    atualizadoEm: DateTime = Column(DateTime, nullable = False, default = datetime.now, onupdate = datetime.now)
