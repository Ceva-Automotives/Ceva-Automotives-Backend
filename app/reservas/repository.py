from sqlalchemy.orm import Session
from ..model.model import Reserva, Carros
from datetime import datetime

class ReservasRepository:
    @staticmethod
    def find_all(database: Session) -> list[Reserva]:
        '''Função para fazer uma query de todas as reservas da DB'''
        return database.query(Reserva).all()

    @staticmethod
    def save(database: Session, reserva: Reserva) -> Reserva:
        '''Função para salvar um objeto reserva na DB'''
        if reserva.id:
            database.merge(reserva)
        else:
            database.add(reserva)
        database.commit()
        database.refresh(reserva)
        return reserva

    @staticmethod
    def find_by_id(database: Session, id: int) -> Reserva:
        '''Função para fazer uma query por ID de um objeto reserva na DB'''
        return database.query(Reserva).filter(Reserva.id == id).first()

    @staticmethod
    def exists_by_id(database: Session, id: int) -> bool:
        '''Função que verifica se o ID dado existe na DB'''
        return database.query(Reserva).filter(Reserva.id == id).first() is not None

    @staticmethod
    def delete_by_id(database: Session, id: int) -> None:
        '''Função para excluir um objeto reserva da DB dado o ID'''
        reserva = database.query(Reserva).filter(Reserva.id == id).first()
        if reserva is not None:
            database.delete(reserva)
            database.commit()

    @staticmethod
    def count_all(database: Session) -> int:
        '''Função para fazer uma query de contagem de todas as reservas da DB'''
        return database.query(Reserva).count()

    @staticmethod
    def find_by_cliente(database: Session, cliente_id: int) -> list[Reserva]:
        '''Função para fazer uma query por cliente de reservas na DB'''
        return database.query(Reserva).filter(Reserva.clienteId == cliente_id).all()

    @staticmethod
    def find_by_carro(database: Session, carro_id: int) -> list[Reserva]:
        '''Função para fazer uma query por carro de reservas na DB'''
        return database.query(Reserva).filter(Reserva.carroId == carro_id).all()

    @staticmethod
    def find_by_status(database: Session, status: str) -> list[Reserva]:
        '''Função para fazer uma query por status de reservas na DB'''
        return database.query(Reserva).filter(Reserva.status == status).all()

    @staticmethod
    def count_by_status(database: Session, status: str) -> int:
        '''Função para fazer uma query de contagem por status de reservas na DB'''
        return database.query(Reserva).filter(Reserva.status == status).count()

    @staticmethod
    def calcular_valor_total(database: Session, carro_id: int, data_retirada: datetime, data_devolucao: datetime) -> float:
        '''Função para calcular o valor total de uma reserva'''
        carro = database.query(Carros).filter(Carros.id == carro_id).first()
        if not carro:
            return 0.0
        
        dias = (data_devolucao - data_retirada).days
        if dias <= 0:
            dias = 1
        
        return carro.precoDia * dias
