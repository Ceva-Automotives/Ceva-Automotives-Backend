from sqlalchemy import func
from sqlalchemy.orm import Session

from ..model.model import Avaliacao


class AvaliacoesRepository:
    @staticmethod
    def find_all(database: Session) -> list[Avaliacao]:
        '''Função para fazer uma query de todas as avaliações da DB'''
        return database.query(Avaliacao).all()

    @staticmethod
    def save(database: Session, avaliacao: Avaliacao) -> Avaliacao:
        '''Função para salvar um objeto avaliação na DB'''
        if avaliacao.id:
            database.merge(avaliacao)
        else:
            database.add(avaliacao)
        database.commit()
        database.refresh(avaliacao)
        return avaliacao

    @staticmethod
    def find_by_id(database: Session, id: int) -> Avaliacao:
        '''Função para fazer uma query por ID de um objeto avaliação na DB'''
        return database.query(Avaliacao).filter(Avaliacao.id == id).first()

    @staticmethod
    def exists_by_id(database: Session, id: int) -> bool:
        '''Função que verifica se o ID dado existe na DB'''
        return database.query(Avaliacao).filter(Avaliacao.id == id).first() is not None

    @staticmethod
    def delete_by_id(database: Session, id: int) -> None:
        '''Função para excluir um objeto avaliação da DB dado o ID'''
        avaliacao = database.query(Avaliacao).filter(Avaliacao.id == id).first()
        if avaliacao is not None:
            database.delete(avaliacao)
            database.commit()

    @staticmethod
    def count_all(database: Session) -> int:
        '''Função para fazer uma query de contagem de todas as avaliações da DB'''
        return database.query(Avaliacao).count()

    @staticmethod
    def find_by_cliente(database: Session, cliente_id: int) -> list[Avaliacao]:
        '''Função para fazer uma query por cliente de avaliações na DB'''
        return database.query(Avaliacao).filter(Avaliacao.clienteId == cliente_id).all()

    @staticmethod
    def find_by_carro(database: Session, carro_id: int) -> list[Avaliacao]:
        '''Função para fazer uma query por carro de avaliações na DB'''
        return database.query(Avaliacao).filter(Avaliacao.carroId == carro_id).all()

    @staticmethod
    def calcular_media_carro(database: Session, carro_id: int) -> dict:
        '''Função para calcular a média de avaliações de um carro'''
        result = database.query(
            func.avg(Avaliacao.nota).label('media'),
            func.count(Avaliacao.id).label('total')
        ).filter(Avaliacao.carroId == carro_id).first()
        
        return {
            'media': float(result.media) if result.media else 0.0,
            'total': result.total if result.total else 0
        }

    @staticmethod
    def find_by_nota(database: Session, nota: int) -> list[Avaliacao]:
        '''Função para fazer uma query por nota de avaliações na DB'''
        return database.query(Avaliacao).filter(Avaliacao.nota == nota).all()
