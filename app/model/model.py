'''Importando parâmetros da orm'''

import enum
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from ..database import Base


# Enums
class StatusCarro(str, enum.Enum):
    '''Enum para status do carro'''
    DISPONIVEL = "Disponivel"
    ALUGADO = "Alugado"
    MANUTENCAO = "Manutencao"

class StatusReserva(str, enum.Enum):
    '''Enum para status da reserva'''
    PENDENTE = "Pendente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    CONCLUIDA = "Concluida"

# Classe abstrata Usuario
class Usuario(Base):
    '''Classe base abstrata para usuários do sistema'''
    __tablename__ = "usuarios"
    
    id: int = Column(Integer, primary_key=True, index=True)
    nome: str = Column(String(200), nullable=False)
    email: str = Column(String(200), nullable=False, unique=True, index=True)
    senha: str = Column(String(255), nullable=False)
    telefone: str = Column(String(20), nullable=True)
    dataCadastro: DateTime = Column(DateTime, nullable=False, default=datetime.now)
    tipo: str = Column(String(50), nullable=False)  # 'cliente' ou 'admin'
    criadoEm: DateTime = Column(DateTime, nullable=False, default=datetime.now)
    atualizadoEm: DateTime = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    
    __mapper_args__ = {
        'polymorphic_identity': 'usuario',
        'polymorphic_on': tipo
    }

class Cliente(Usuario):
    '''Classe para clientes do sistema'''
    __tablename__ = "clientes"
    
    id: int = Column(Integer, ForeignKey('usuarios.id'), primary_key=True)
    cnh: str = Column(String(20), nullable=False, unique=True)
    cpf: str = Column(String(14), nullable=False, unique=True)
    
    # Relacionamentos
    reservas = relationship("Reserva", back_populates="cliente", cascade="all, delete-orphan")
    avaliacoes = relationship("Avaliacao", back_populates="cliente", cascade="all, delete-orphan")
    
    __mapper_args__ = {
        'polymorphic_identity': 'cliente',
    }

class Admin(Usuario):
    '''Classe para administradores do sistema'''
    __tablename__ = "admins"
    
    id: int = Column(Integer, ForeignKey('usuarios.id'), primary_key=True)
    cargo: str = Column(String(100), nullable=False)
    
    # Relacionamento
    dashboard = relationship("Dashboard", back_populates="admin", uselist=False, cascade="all, delete-orphan")
    
    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

class Localizacao(Base):
    '''Classe para estabelecer o modelo da tabela de localizações na DB'''
    __tablename__ = "localizacoes"
    
    id: int = Column(Integer, primary_key=True, index=True)
    nome: str = Column(String(200), nullable=False)
    endereco: str = Column(String(500), nullable=False)
    criadoEm: DateTime = Column(DateTime, nullable=False, default=datetime.now)
    atualizadoEm: DateTime = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    
    # Relacionamentos
    carros = relationship("Carros", back_populates="localizacao")
    reservas_retirada = relationship("Reserva", foreign_keys="Reserva.localizacaoRetiradaId", back_populates="localizacaoRetirada")
    reservas_devolucao = relationship("Reserva", foreign_keys="Reserva.localizacaoDevolucaoId", back_populates="localizacaoDevolucao")

class Carros(Base):
    '''Classe para estabelecer o modelo da tabela de carros na DB'''
    __tablename__ = "carros"

    id: int = Column(Integer, primary_key=True, index=True)
    placa: str = Column(String(10), nullable=False, unique=True)
    marca: str = Column(String(100), nullable=False)
    modelo: str = Column(String(100), nullable=False)
    ano: int = Column(Integer, nullable=False)
    cor: str = Column(String(50), nullable=False)
    precoDia: float = Column(Float, nullable=False)
    categoria: str = Column(String(100), nullable=False)
    status: str = Column(SQLEnum(StatusCarro), nullable=False, default=StatusCarro.DISPONIVEL)
    descricao: str = Column(String(500), nullable=True)
    disponivel: bool = Column(Boolean, nullable=False, default=True)
    destaque: bool = Column(Boolean, nullable=False, default=False)
    localizacaoId: int = Column(Integer, ForeignKey('localizacoes.id'), nullable=True)
    criadoEm: DateTime = Column(DateTime, nullable=False, default=datetime.now)
    atualizadoEm: DateTime = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    
    # Relacionamentos
    localizacao = relationship("Localizacao", back_populates="carros")
    avaliacoes = relationship("Avaliacao", back_populates="carro", cascade="all, delete-orphan")
    reservas = relationship("Reserva", back_populates="carro")

class Reserva(Base):
    '''Classe para estabelecer o modelo da tabela de reservas na DB'''
    __tablename__ = "reservas"
    
    id: int = Column(Integer, primary_key=True, index=True)
    dataRetirada: DateTime = Column(DateTime, nullable=False)
    dataDevolucao: DateTime = Column(DateTime, nullable=False)
    valorTotal: float = Column(Float, nullable=False)
    status: str = Column(SQLEnum(StatusReserva), nullable=False, default=StatusReserva.PENDENTE)
    clienteId: int = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    carroId: int = Column(Integer, ForeignKey('carros.id'), nullable=False)
    localizacaoRetiradaId: int = Column(Integer, ForeignKey('localizacoes.id'), nullable=False)
    localizacaoDevolucaoId: int = Column(Integer, ForeignKey('localizacoes.id'), nullable=False)
    criadoEm: DateTime = Column(DateTime, nullable=False, default=datetime.now)
    atualizadoEm: DateTime = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    
    # Relacionamentos
    cliente = relationship("Cliente", back_populates="reservas")
    carro = relationship("Carros", back_populates="reservas")
    localizacaoRetirada = relationship("Localizacao", foreign_keys=[localizacaoRetiradaId], back_populates="reservas_retirada")
    localizacaoDevolucao = relationship("Localizacao", foreign_keys=[localizacaoDevolucaoId], back_populates="reservas_devolucao")

class Avaliacao(Base):
    '''Classe para estabelecer o modelo da tabela de avaliações na DB'''
    __tablename__ = "avaliacoes"
    
    id: int = Column(Integer, primary_key=True, index=True)
    nota: int = Column(Integer, nullable=False)  # 1-5
    comentario: str = Column(Text, nullable=True)
    data: DateTime = Column(DateTime, nullable=False, default=datetime.now)
    clienteId: int = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    carroId: int = Column(Integer, ForeignKey('carros.id'), nullable=False)
    criadoEm: DateTime = Column(DateTime, nullable=False, default=datetime.now)
    atualizadoEm: DateTime = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    
    # Relacionamentos
    cliente = relationship("Cliente", back_populates="avaliacoes")
    carro = relationship("Carros", back_populates="avaliacoes")

class Dashboard(Base):
    '''Classe para estabelecer o modelo da tabela de dashboards na DB'''
    __tablename__ = "dashboards"
    
    id: int = Column(Integer, primary_key=True, index=True)
    nome: str = Column(String(200), nullable=False)
    adminId: int = Column(Integer, ForeignKey('admins.id'), nullable=False, unique=True)
    criadoEm: DateTime = Column(DateTime, nullable=False, default=datetime.now)
    atualizadoEm: DateTime = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    
    # Relacionamentos
    admin = relationship("Admin", back_populates="dashboard")
    metricas = relationship("Metrica", back_populates="dashboard", cascade="all, delete-orphan")

class Metrica(Base):
    '''Classe para estabelecer o modelo da tabela de métricas na DB'''
    __tablename__ = "metricas"
    
    id: int = Column(Integer, primary_key=True, index=True)
    nome: str = Column(String(200), nullable=False)
    valor: str = Column(String(200), nullable=False)
    tipo: str = Column(String(100), nullable=False)
    dashboardId: int = Column(Integer, ForeignKey('dashboards.id'), nullable=False)
    criadoEm: DateTime = Column(DateTime, nullable=False, default=datetime.now)
    atualizadoEm: DateTime = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    
    # Relacionamento
    dashboard = relationship("Dashboard", back_populates="metricas")
